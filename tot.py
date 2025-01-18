# Time On Target (main)
# TODO:
# Get a working desk clock
# Eventually buttons will be needed - how many and what for?
# Pull in Google Calendar integration from Rosuav/LetMeKnow (reimplement - old code with Py2 compat)

import RPi.GPIO as GPIO
import board
import digitalio
import pwmio
import adafruit_character_lcd.character_lcd as character_lcd
import time

def init_lcd():
	lcd_rs = digitalio.DigitalInOut(board.D2)
	# LCD RW (pin 5) is pulled to ground as we never need to read from the display
	lcd_en = digitalio.DigitalInOut(board.D4)
	lcd_d4 = digitalio.DigitalInOut(board.D27)
	lcd_d5 = digitalio.DigitalInOut(board.D22)
	lcd_d6 = digitalio.DigitalInOut(board.D23)
	lcd_d7 = digitalio.DigitalInOut(board.D24)
	lcd_red = pwmio.PWMOut(board.D3) # The only one that matters - green and blue are dummies
	lcd_green = digitalio.DigitalInOut(board.D14)
	lcd_blue = digitalio.DigitalInOut(board.D15)
	lcd_columns = 20
	lcd_rows = 4
	# Backlight managed manually with PWM - mono backlight control on Character_LCD_Mono is boolean
	#lcd_backlight = 3
	#pwm_freq = 50
	#GPIO.setmode(GPIO.BCM)
	#GPIO.setwarnings(False)
	#GPIO.setup(lcd_backlight, GPIO.OUT)
	#global pwm
	#pwm = GPIO.PWM(lcd_backlight, pwm_freq)
	#pwm.start(0)
	lcd = character_lcd.Character_LCD_RGB(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_red, lcd_green, lcd_blue)
	lcd.blink = False
	lcd.clear()

def test_message():
	lcd.message = "Hello world!"
	lcd.color = [100,0,0]
	time.sleep(10)

def cleanup():
	lcd.clear()
	lcd.color = [0,0,0]
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		init_lcd()
		test_message()
	finally:
		cleanup()
