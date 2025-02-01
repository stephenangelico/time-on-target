# Time On Target (main)
# TODO:
# Get a working desk clock (more than just a limited test)
# Implement modeswitch/interrupt for a display mode which is regularly updating (such as a clock)
# Eventually buttons will be needed - how many and what for?
# Pull in Google Calendar integration from Rosuav/LetMeKnow (reimplement - old code with Py2 compat)
#
# Tasks that will run:
# Clock ticker
# GCal sync
# Current/imminent alarm
# Display renderer
# Button listener
#
# Possibly have renderer which shows ticking clock (3 lines) and 1 info line
# This would be updated by the button, switching between info lines (timeout to default ie date)
# Cycle between date, next alarm time, next alarm name (if ringing show current alarm, cycle to button cue)

import RPi.GPIO as GPIO
import board
import digitalio
import pwmio
import adafruit_character_lcd.character_lcd as character_lcd
import time
import asyncio

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

async def init_lcd():
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
	pwm.ChangeDutyCycle(100)
	while True:
		lcd_render("date")
		await asyncio.sleep(0.5)

def lcd_render(mode):
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
	if mode == "date":
		fourth_line = time.strftime("%a, %d %b %Y")
	lcd.message = time_3line + fourth_line

async def console_time():
	while True:
		print(time.strftime("%H:%M:%S"), end="\r")
		await asyncio.sleep(0.5)

async def cleanup():
	lcd.clear()
	pwm.ChangeDutyCycle(0)
	GPIO.cleanup()
	# TODO: On exit, with PWM gone, the backlight turns on again and the characters fill with blocks. Can we keep the backlight off on exit?

async def main():
	try:
		await init_lcd()
		spawn(test_message())
		spawn(console_time())
		await asyncio.Future()
	finally:
		await cleanup()

if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		pass
