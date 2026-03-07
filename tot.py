# Time On Target (main)
# TODO:
# Button
# PWM backlight
#
# Tasks that will run:
# GCal sync
# Current/imminent alarm
# Display renderer - done
# Button listener (note: use GPIO.PUD_UP)
#
# Renderer draws ticking clock (with seconds and date crammed in) and info lines
# for next alarm time and name
# If alarm is ringing, show current alarm name, and "Hold button to stop"
# Animate exploding chevrons while ringing?

import time
import threading
import matrix_lcd
import gcal

threads = []

alarms = []
cancelled_alarms = []

def cal_sync():
	while True:
		t = time.monotonic()
		global alarms
		alarms = gcal.main()
		time.sleep(900 - time.monotonic() + t)
		# TODO: sync more frequently as time to next event approaches

def clock_ticker():
	next_time = "00:00 (00h)"
	next_name = "Very long alarm name"
	while True:
		t = time.monotonic()
		for alarm in alarms:
			if alarm[0] not in cancelled_alarms:
				next_name = alarm[1]
				next_time = (alarm[2].strftime("%d/%m %H:%M")) # TODO: Add time delta
				break
		matrix_lcd.draw_text(0, 6, time.strftime("%H:%M:%S"))
		matrix_lcd.draw_text(0, 14, next_name)
		matrix_lcd.draw_text(0, 22, next_time)
		# TODO: Make this count down
		# Row = ASCENDER + BASE -1 (zero-base address)
		matrix_lcd.update()
		time.sleep(0.5 - time.monotonic() + t)

def cleanup():
	matrix_lcd.cleanup()

if __name__ == "__main__":
	try:
		matrix_lcd.init()
		clock_ticker()
	except KeyboardInterrupt:
		pass
	finally:
		cleanup()
