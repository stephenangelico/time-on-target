# Time On Target (main)
# TODO:
# Button
# PWM backlight
#
# Tasks that will run:
# GCal sync - done
# Current/imminent alarm
# Display renderer - done
# Button listener (note: use GPIO.PUD_UP)
#
# Renderer draws ticking clock (with seconds and date crammed in) and info lines
# for next alarm time and name
# If alarm is ringing, show current alarm name, and "Hold button to stop"
# Animate exploding chevrons while ringing?

import os
import sys
import time
import selectors
import datetime
import threading
import subprocess
try:
	import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
	print("This program must be run on a Raspberry Pi. Did you mean to run gcal.py?")
	sys.exit(1)
import matrix_lcd
import gcal
import font_small

alarms = []
cancelled_alarms = []
disp_alarm = ""
alarm_active = False
ringer = None
button_down = None
latest_press = ""
disp_r, disp_w = os.pipe() # Signal to update display immediately

# Copied from RPi.GPIO.__init__.py
# Why are we subclassing an internal class in GPIO?
# Because the API does not allow the type of button edge (rising/falling)
# to bubble up to the event detection. This changes that, at cost of
# compatibility - now event callbacks MUST handle the edge type, regardless of
# what type of edge they are detecting.
# The API also does not allow two event detections on the same channel.
# Copyright (c) 2022-2023 Dave Jones <dave@waveform.org.uk>
class _Alert(GPIO._Alert):
	def _call(self, chip, gpio, level, timestamp):
		if level == 2:
			# Watchdog timeout; this *shouldn't* happen as we never use this
			# part of lgpio but if there's something else messing with the API
			# other than this shim it's a possibility
			return
		self._detected = True
		for cb in self.callbacks:
			try:
				cb(GPIO._from_gpio(gpio), level)
			except Exception as exc:
				# Bug compatibility: this is how RPi.GPIO operates
				print(exc, file=sys.stderr)

GPIO._Alert = _Alert

def ring_alarm():
	global ringer
	ringer = subprocess.Popen(["/usr/bin/cvlc", "1.wav"])
	# TODO: Do we need VLC to loop, and if not, what do we do when it terminates?
	global alarm_active
	alarm_active = True

def cal_sync():
	while True:
		t = time.monotonic()
		global alarms
		alarms = gcal.main()
		for alarm in alarms:
			if alarm[0] not in cancelled_alarms:
				if alarm[3].seconds > 1800:
					d = 900
				elif alarm[3].seconds > 900:
					d = 300
				elif alarm[3].seconds > 300:
					d = 60
				elif alarm[3].seconds > 60:
					d = 30
				else:
					d = alarm[3].seconds + 5
					a = threading.Timer(d-5, ring_alarm)
					a.start()
				break
		time.sleep(d - time.monotonic() + t)

def button_held():
	global alarm_active
	if alarm_active:
		ringer.send_signal(2) # Send Ctrl-C to VLC
		alarm_active = False
	else:
		# TODO: Only allow alarms to be cancelled within 1hr of ringing (do nothing otherwise)
		# TODO: Special-case having no alarms
		# TODO: Check in gcal.py if 5 alarms is enough
		if disp_alarm not in cancelled_alarms:
			cancelled_alarms.append(disp_alarm)
			print("Alarm", disp_alarm, "cancelled")
		else:
			cancelled_alarms.remove(disp_alarm)
			# Uncancel, not sure if we need it though - would need to display cancelled alarms

def button_timer():
	global button_down
	global latest_press
	latest_press = "Hold"
	button_held()
	os.write(disp_w, b"u")
	button_down = None

def button_listener(chan, level):
	# We are using the internal pull-up resistor, so the circuit is grounded
	# (ie level=0) when the button is pressed, and the circuit is pulled
	# high (ie level=1) when the button is open/released.
	global button_down
	if level:
		if button_down:
			button_down.cancel()
			global latest_press
			latest_press = "Press"
			os.write(disp_w, b"u")
		button_down = None
	else:
		button_down = threading.Timer(1, button_timer)
		button_down.start()

def button_test(chan, level):
	if level:
		print(time.monotonic(), chan, "released")
	else:
		print(time.monotonic(), chan, "pressed")

def button_setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(17, GPIO.BOTH, button_listener, 5)

def clock_ticker():
	next_time = "00:00 (00h)"
	next_name = "Very long alarm name"
	# Listen for signal to update display immediately
	sel = selectors.DefaultSelector()
	sel.register(disp_r, selectors.EVENT_READ)
	while True:
		t = time.monotonic()
		if alarm_active:
			pass
		# TODO: if alarm_active, do not update to the next alarm - display/animate current alarm
		for alarm in alarms:
			if alarm[0] not in cancelled_alarms:
				global disp_alarm
				disp_alarm = alarm[0]
				next_name = alarm[1]
				alarm_delta = alarm[2] - datetime.datetime.now(tz=datetime.UTC)
				if alarm_delta.total_seconds() >= 86400:
					tag = "%dd" % (alarm_delta.total_seconds() // 86400)
				elif alarm_delta.total_seconds() >= 3600:
					tag = "%dh" % (alarm_delta.total_seconds() // 3600)
				elif alarm_delta.total_seconds() >= 60:
					tag = "%dm" % (alarm_delta.total_seconds() // 60)
				elif alarm_delta.total_seconds() > 0:
					tag = "0m"
				else:
					tag = "NOW"
				next_time = (alarm[2].strftime("%d/%m %H:%M") + " (" + tag + ")")
				break
		matrix_lcd.clear_display()
		first_row = font_small.ASCENDER + font_small.BASE - 1 # Zero-base addressing
		matrix_lcd.draw_text(0, first_row, time.strftime("%H:%M:%S"))
		matrix_lcd.draw_text(0, (first_row + font_small.ADVANCEMENT), next_name)
		matrix_lcd.draw_text(0, (first_row + font_small.ADVANCEMENT * 2), next_time)
		matrix_lcd.draw_text(0, (first_row + font_small.ADVANCEMENT * 3), latest_press) # Demo only, will no longer work when big_font is used
		matrix_lcd.update()
		if sel.select(0.5 - time.monotonic() + t): os.read(disp_r, 1) # Wait either for timeout (0.5sec minus draw time) or a signal

def cleanup():
	matrix_lcd.cleanup() # Includes GPIO cleanup

if __name__ == "__main__":
	try:
		t = threading.Thread(target=cal_sync, daemon=True)
		t.start()
		button_setup()
		matrix_lcd.init()
		clock_ticker()
	except KeyboardInterrupt:
		pass
	finally:
		cleanup()
