# Matrix LCD brightness test via PWM
import time
import RPi.GPIO as GPIO

PIN_PWM = 22 # Physical pin 15
FREQ = 50

def test_backlight():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(PIN_PWM, GPIO.OUT)
	pwm = GPIO.PWM(PIN_PWM, FREQ)
	pwm.start(0)
	for n in range(100, step=10):
		print("Brightness level:", n)
		pwm.ChangeDutyCycle(n)
		time.sleep(1)

if __name__ == "__main__":
	test_backlight()
