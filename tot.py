# Time On Target (main)
# TODO:
# Get a working desk clock
# Implement modeswitch/interrupt for a display mode which is regularly updating (such as a clock)
# Eventually buttons will be needed - how many and what for?
# Pull in Google Calendar integration from Rosuav/LetMeKnow (reimplement - old code with Py2 compat)

import RPi.GPIO as GPIO
import board
import digitalio
import pwmio
import adafruit_character_lcd.character_lcd as character_lcd
import time

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

def test_message():
	pwm.ChangeDutyCycle(100)
	t = 0
	while t <= 20:
		lcd.message = time.strftime("%H:%M:%S")
		time.sleep(0.5)
		t += 1
	#time.sleep(10)

def cleanup():
	lcd.clear()
	pwm.ChangeDutyCycle(0)
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		init_lcd()
		test_message()
	finally:
		cleanup()
