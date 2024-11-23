# Time On Target (main)
# TODO:
# First, test LCD
# Switch backlight input to GPIO12 (PWM)?
# Can only use 4-bit mode with Adafruit library - any benefit in re-implementing in 8-bit?
# Then get a working desk clock
# Eventually buttons will be needed - how many and what for?
# Pull in Google Calendar integration from Rosuav/LetMeKnow (reimplement - old code with Py2 compat)

import RPi.GPIO as GPIO
import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
import time

# Init LCD
lcd_rs = digitalio.DigitalInOut(board.D2)
lcd_rw = 3
lcd_en = digitalio.DigitalInOut(board.D4)
lcd_d4 = digitalio.DigitalInOut(board.D27)
lcd_d5 = digitalio.DigitalInOut(board.D22)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D24)
lcd_columns = 20
lcd_rows = 4
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(lcd_rw, GPIO.OUT, initial=GPIO.LOW)
#lcd_backlight = digitalio.DigitalInOut(board.D21) # Works but doesn't supply enough power
lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
lcd.backlight = True
lcd.blink = False

lcd.message("Hello world!")
time.sleep(3)
lcd.clear()
GPIO.cleanup()
