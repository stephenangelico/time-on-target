# Matrix LCD brightness test via PWM
import time
import RPi.GPIO as GPIO

PIN_PWM = 22 # Physical pin 15
FREQ = 50
pwm = None

def test_backlight():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(PIN_PWM, GPIO.OUT)
	global pwm
	pwm = GPIO.PWM(PIN_PWM, FREQ)
	pwm.start(0)
	for n in range(0, 101, 10):
		print("Brightness level:", n)
		pwm.ChangeDutyCycle(n)
		time.sleep(1)

def cleanup():
	global pwm
	pwm.ChangeDutyCycle(0)
	pwm.stop()
	pwm = None # Must be *before* cleanup due to bug in lgpio
	GPIO.cleanup()

if __name__ == "__main__":
	test_backlight()
	cleanup()
