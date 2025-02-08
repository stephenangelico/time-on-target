# Time On Target (main)
# TODO:
# Eventually buttons will be needed - how many and what for?
# Pull in Google Calendar integration from Rosuav/LetMeKnow (reimplement - old code with Py2 compat)
#
# Tasks that will run:
# GCal sync
# Current/imminent alarm
# Display renderer - done
# Button listener
#
# Renderer draws ticking clock (3 lines) and 1 info line updated by the button,
# switching between info modes (timeout to default ie date)
# Cycle between date, next alarm time, next alarm name and others as available
# If alarm is ringing, show current alarm name, cycle to "Hold button to stop")

import RPi.GPIO as GPIO
import board
import digitalio
import pwmio
import adafruit_character_lcd.character_lcd as character_lcd
import time
import traceback
import queue
import threading
import asyncio
# Yes, this uses both threading and asyncio, because AdafruitCharLCD uses synchronous time.sleep internally.

lcd_mgr = queue.Queue()

FONT = {
	"0": ("000", "0 0", "000"),
	"1": (" 1 ", " 1 ", " 1 "),
	"2": ("22 ", " 2 ", "222"),
	"3": ("333", " 33", "333"),
	"4": ("4 4", "444", " 4 "),
	"5": (" 55", " 5 ", "555"),
	"6": (" 66", "6  ", "666"),
	"7": ("777", " 7 ", "7  "),
	"8": ("888", " 8 ", "888"),
	"9": (" 99", "99 ", "  9"),
	":": ("   ", " \xA5 ", " \xA5 "),
}

marquee_idx = 0
next_time = "00:00 (00h)"
next_name = "Very long alarm name"

def export(f):
	setattr(builtins, f.__name__, f)
	return f

def report(msg):
	print(time.time(), msg)

def handle_errors(task):
	try:
		exc = task.exception() # Also marks that the exception has been handled
		if exc: traceback.print_exception(type(exc), exc, exc.__traceback__)
	except asyncio.exceptions.CancelledError:
		pass

all_tasks = [] # kinda like threading.all_threads()

def task_done(task):
	all_tasks.remove(task)
	handle_errors(task)

def spawn(awaitable):
	"""Spawn an awaitable as a stand-alone task"""
	task = asyncio.create_task(awaitable)
	all_tasks.append(task)
	task.add_done_callback(task_done)
	return task

def init_lcd():
	lcd_rs = digitalio.DigitalInOut(board.D2) # Physical pin 3
	# LCD RW (pin 5) is pulled to ground as we never need to read from the display
	lcd_en = digitalio.DigitalInOut(board.D4) # Physical pin 7
	lcd_d4 = digitalio.DigitalInOut(board.D27) # Physical pin 13
	lcd_d5 = digitalio.DigitalInOut(board.D22) # Physical pin 15
	lcd_d6 = digitalio.DigitalInOut(board.D23) # Physical pin 16
	lcd_d7 = digitalio.DigitalInOut(board.D24) # Physical pin 18
	lcd_columns = 20
	lcd_rows = 4
	# Backlight managed manually with PWM - mono backlight control on Character_LCD_Mono is boolean,
	# and Character_LCD_RGB assumes inverted wiring and requires all three colours to be set on pins
	# (even as dummies)
	lcd_backlight = 3 # Physical pin 5
	pwm_freq = 50
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(lcd_backlight, GPIO.OUT)
	global pwm
	pwm = GPIO.PWM(lcd_backlight, pwm_freq)
	pwm.start(0)
	global lcd
	lcd = character_lcd.Character_LCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
	lcd.blink = False
	lcd.clear()

async def test_message():
	lcd_mgr.put(["duty_cycle", 100])
	while True:
		line_render("date")
		await asyncio.sleep(0.5)

def line_render(mode):
	"""Render the time and 4th line and send to LCD"""
	cur_time = time.strftime("%H:%M:%S")
	# Font gives each digit in a tuple of three 3-character strings.
	# Renderer builds each line by taking appropriate line of each digit in cur_time
	time_3line = "\n".join(
		FONT[cur_time[0]][line] + " " + FONT[cur_time[1]][line] +
		FONT[":"][line] +
		FONT[cur_time[3]][line] + " " + FONT[cur_time[4]][line]
		for line in range(3)
	) + " " + cur_time[6:] + "\n"
	global marquee_idx
	if mode == "date":
		fourth_line = time.strftime("%a, %d %b %Y")
	elif mode == "next_time":
		fourth_line = "Next: " + next_time
	elif mode == "next_name":
		fourth_line = "Next: " + next_name
	elif mode == "cur_name":
		fourth_line = next_name
	# TODO: Missed alarm mode if there is one, and/or a last alarm mode?
	# TODO: Refactor so modes are data (which may or may not be available)
	if len(fourth_line) <= 20:
		fourth_line = fourth_line.center(20)
	else:
		fourth_line += " "
		marquee_idx += 1 # TODO: reset on button press
		fourth_line = (fourth_line * 2)[marquee_idx % len(fourth_line):][:20]
		# TODO: Marquee only name
		# TODO: Pause marquee (~2sec) after full loop
		# TODO: Marquee faster
		# Possibly see-saw marquee instead of loop?
	lcd_mgr.put(["message", time_3line + fourth_line])

async def console_time():
	while True:
		print(time.strftime("%H:%M:%S"), end="\r")
		await asyncio.sleep(0.5)

def cleanup():
	lcd.clear()
	pwm.ChangeDutyCycle(0)
	GPIO.cleanup()
	# TODO: On exit, with PWM gone, the backlight turns on again and the characters fill with blocks. Can we keep the backlight off on exit?

def lcd_handler():
	try:
		init_lcd()
		while (msg := lcd_mgr.get()) != ("shutdown",):
			match msg:
				case ["message", msg]: lcd.message = msg
				case ["duty_cycle", duty]: pwm.ChangeDutyCycle(duty)
				case unk: print("Unknown message", unk)
	finally:
		cleanup()

async def main():
	lcd_thread = threading.Thread(target=lcd_handler)
	lcd_thread.start()
	try:
		spawn(test_message())
		#spawn(console_time())
		await asyncio.Future()
	finally:
		lcd_mgr.put(("shutdown",))
		lcd_thread.join()

if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		pass
