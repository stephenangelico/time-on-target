# Time On Target (main)
# TODO:
# Use software PWM to set brightness level for backlight
# Wire PWM pin to small capacitor and NPN transistor to switch 3.3V GPIO to 5V rail
# Get a working desk clock
# Eventually buttons will be needed - how many and what for?
# Pull in Google Calendar integration from Rosuav/LetMeKnow (reimplement - old code with Py2 compat)

import RPi.GPIO as GPIO
import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
import time

# Init LCD
lcd_rs = digitalio.DigitalInOut(board.D2)
# LCD RW (pin 5) is pulled to ground as we never need to read from the display
lcd_en = digitalio.DigitalInOut(board.D4)
lcd_d4 = digitalio.DigitalInOut(board.D27)
lcd_d5 = digitalio.DigitalInOut(board.D22)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D24)
lcd_columns = 20
lcd_rows = 4
lcd_backlight = 3
pwm_freq = 50
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(lcd_backlight, GPIO.OUT)
global pwm
pwm = GPIO.PWM(lcd_backlight, pwm_freq)
pwm.start(0)
lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
lcd.blink = False

lcd.clear()
lcd.message = "Hello world!"
pwm.ChangeDutyCycle(50)
time.sleep(30)
lcd.clear()
pwm.ChangeDutyCycle(0)
GPIO.cleanup()
