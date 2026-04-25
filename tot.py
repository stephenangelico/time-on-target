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

import sys
import time
import datetime
import threading
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

# Copied from RPi.GPIO.__init__.py
# Why are we subclassing an internal class in GPIO?
# Because the API does not allow the type of button edge (rising/falling)
# to bubble up to the event detection. This changes that, at cost of
# compatibility - now event callbacks MUST handle the edge type, regardless of
# what type of edge they are detecting.
# The API also does not allow two event detections on the same channel.
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

def cal_sync():
	while True:
		t = time.monotonic()
		global alarms
		alarms = gcal.main()
		time.sleep(900 - time.monotonic() + t)
		# TODO: sync more frequently as time to next event approaches

def alarm_ringer():
	pass
	# TODO

def button_listener():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(17, GPIO.BOTH, button_pressed, 50)
	# TODO: this is a stub

def button_pressed(chan, level):
	if level:
		print(chan, "released")
	else:
		print(chan, "pressed")

def clock_ticker():
	next_time = "00:00 (00h)"
	next_name = "Very long alarm name"
	while True:
		t = time.monotonic()
		for alarm in alarms:
			if alarm[0] not in cancelled_alarms:
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
		matrix_lcd.update()
		time.sleep(0.5 - time.monotonic() + t)

def cleanup():
	matrix_lcd.cleanup() # Includes GPIO cleanup

if __name__ == "__main__":
	try:
		t = threading.Thread(target=cal_sync, daemon=True)
		t.start()
		matrix_lcd.init()
		clock_ticker()
	except KeyboardInterrupt:
		pass
	finally:
		cleanup()
