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
import signal
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
import font_large
import font_big

alarms = []
cancelled_alarms = []
next_alarm = None
disp_alarm = ""
current_alarm = None
ringer = None
anim_chevron_time = 0
button_down = None
latest_press = ""
cal_status = "Connecting to GCal..." # None if all is well, error message otherwise
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

def stop_alarm(s, f):
	global ringer
	if ringer and ringer.poll() is not None:
		global current_alarm
		current_alarm = None
		ringer = None
		global anim_chevron_time
		anim_chevron_time = 0

signal.signal(signal.SIGCHLD, stop_alarm)

def ring_alarm(alarm):
	global ringer
	ringer = subprocess.Popen(["/usr/bin/cvlc", "1.wav", "--play-and-exit"])
	# Play once and exit. If you want to loop, adjust the command.
	# Once VLC quits, the alarm will be cancelled automatically.
	global current_alarm
	current_alarm = alarm
	global anim_chevron_time
	anim_chevron_time = time.monotonic()

def cal_sync():
	while True:
		try:
			t = time.monotonic()
			d = 900 # Don't spam Google servers if there are no alarms
			global alarms
			global cal_status
			alarms = gcal.main()
			if not alarms:
				cal_status = "No alarms set"
				global disp_alarm
				disp_alarm = ""
				global next_alarm
				next_alarm = None
			else:
				for alarm in alarms:
					if alarm[0] not in cancelled_alarms:
						next_alarm = alarm
						# Graduated re-check times in case of last minute changes
						if alarm[3].seconds > 1800:
							d = 900
							# Every 15 minutes if more than 30 min out
						elif alarm[3].seconds > 900:
							d = 300
							# Every 5 minutes if 15-30 min out
						elif alarm[3].seconds > 300:
							d = 60
							# Every minute if 5-15 min out
						elif alarm[3].seconds > 60:
							d = 30
							# Every 30 sec if 1-5 min out
						else:
							d = alarm[3].seconds + 5
							# Exact time remaining if less than a minute out
							a = threading.Timer(d-5, ring_alarm, args=(alarm,))
							a.start()
						break
				cal_status = None
		except Exception as e:
			cal_status = "Error: " + str(e)
			d = 60 # Try again soon but not immediately
		time.sleep(d - time.monotonic() + t)

def button_held():
	global current_alarm
	if current_alarm:
		ringer.send_signal(2) # Send Ctrl-C to VLC
		current_alarm = None
	else:
		# TODO: Only allow alarms to be cancelled within 1hr of ringing (do nothing otherwise)
		if disp_alarm not in cancelled_alarms:
			cancelled_alarms.append(disp_alarm)
			print("Alarm", disp_alarm, "cancelled")
		else:
			cancelled_alarms.remove(disp_alarm)
			# Uncancel, not sure if we need it though - would need to display cancelled alarms

def button_timer():
	global latest_press
	latest_press = "Hold"
	button_held()
	os.write(disp_w, b"u")
	global button_down
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
	# Listen for signal to update display immediately
	sel = selectors.DefaultSelector()
	sel.register(disp_r, selectors.EVENT_READ)
	while True:
		t = time.monotonic()
		refresh_time = 0.5 # 2FPS when idle
		if current_alarm:
			line1 = "ALARM!".center(21)
			# Display is approx. 21 characters wide
			line2 = current_alarm[1].center(21)
		else:
			if cal_status:
				if len(cal_status) > 21:
					cut = cal_status.rfind(" ", 10, 20)
					if cut == -1: cut = 20
					line1 = cal_status[:cut]
					line2 = cal_status[cut+1:]
				else:
					line1 = cal_status
					line2 = ""
			else:
				for alarm in alarms:
					if alarm[0] not in cancelled_alarms:
						global disp_alarm
						disp_alarm = alarm[0]
						# TODO: use button press to cycle through alarms
						line1 = "Next: " + alarm[1]
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
						line2 = (alarm[2].strftime("%d/%m %H:%M") + " (" + tag + ")")
						break
		matrix_lcd.clear_display()
		first_row = font_big.ASCENDER + font_big.BASE - 1 # Zero-base addressing
		# TODO: Use either font_large or font_big here - CHECK matrix_lcd.py
		second_row = first_row + font_small.ADVANCEMENT
		third_row = first_row + font_small.ADVANCEMENT * 2
		matrix_lcd.draw_text(0, first_row, time.strftime("%H:%M:%S"), font=font_big)
		matrix_lcd.draw_text(0, second_row, line1)
		matrix_lcd.draw_text(0, third_row, line2)
		if anim_chevron_time:
			refresh_time = min(refresh_time, 0.25) # 4FPS
			frame = int((time.monotonic() - anim_chevron_time) / 0.025) # Frames since alarm animation started
			# Animation speed is 1 frame every x seconds, where x is the divisor
			phase = frame % 60 # Animation position based on frame number
			# Position is started in the middle +4/-4, so 60 frames reaches the edge
			# TODO: Flash button LED in time with animation
			chevron_scale = 4 # Chevron height is 2 * chevron_scale - 1
			chevron_width = 2
			anim_row2 = second_row - chevron_scale + 1
			anim_row3 = third_row - chevron_scale + 1
			for i in range(chevron_scale):
				for j in range (i and -2, chevron_width + 2):
					matrix_lcd.set_pixel(anim_row2 - i, 60 + j + i - phase, 0 <= j < chevron_width)
					matrix_lcd.set_pixel(anim_row2 + i, 60 + j + i - phase, 0 <= j < chevron_width)
					matrix_lcd.set_pixel(anim_row2 - i, 68 - j - i + phase, 0 <= j < chevron_width)
					matrix_lcd.set_pixel(anim_row2 + i, 68 - j - i + phase, 0 <= j < chevron_width)
					matrix_lcd.set_pixel(anim_row3 - i, 60 + j + i - phase, 0 <= j < chevron_width)
					matrix_lcd.set_pixel(anim_row3 + i, 60 + j + i - phase, 0 <= j < chevron_width)
					matrix_lcd.set_pixel(anim_row3 - i, 68 - j - i + phase, 0 <= j < chevron_width)
					matrix_lcd.set_pixel(anim_row3 + i, 68 - j - i + phase, 0 <= j < chevron_width)
		matrix_lcd.update()
		#print(time.monotonic() - t)
		if sel.select(refresh_time - time.monotonic() + t): os.read(disp_r, 1) # Wait either for timeout or a signal

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
