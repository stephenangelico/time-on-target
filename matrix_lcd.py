# Matrix LCD test/library
import time
from enum import IntEnum
import RPi.GPIO as GPIO

# Pin GPIO numbers
class Pin(IntEnum):
	RS = 2 # Register Select or Data/Instruction
	RW = 3 # Read/Write
	EN = 4 # Enable (pulsed only)
	DB0 = 25 # Data bit 0
	DB1 = 8  # Data bit 1
	DB2 = 7  # Data bit 2
	DB3 = 1  # Data bit 3
	DB4 = 0  # Data bit 4
	DB5 = 5  # Data bit 5
	DB6 = 6  # Data bit 6
	DB7 = 13 # Data bit 7
	CS1 = 14 # Column Select 1 (columns 1-64)
	CS2 = 15 # Column Select 2 (columns 65-128)
	RST = 18 # Reset

data_pins = (Pin.DB7, Pin.DB6, Pin.DB5, Pin.DB4, Pin.DB3, Pin.DB2, Pin.DB1, Pin.DB0)

def pulse_enable():
	GPIO.output(Pin.EN, 1)
	time.sleep(0.000001)
	GPIO.output(Pin.EN, 0)

def set_rw_read():
	GPIO.output(Pin.RW, 1)
	for pin in data_pins:
		GPIO.setup(pin, GPIO.IN)

def set_rw_write():
	GPIO.output(Pin.RW, 0)
	for pin in data_pins:
		GPIO.setup(pin, GPIO.OUT)
	# TODO: Merge these functions

def set_cs(chip):
	GPIO.output(Pin.CS1, chip == 1 or chip == 3)
	GPIO.output(Pin.CS2, chip == 2 or chip == 3)
	
def status_read():
	GPIO.output(Pin.RS, 0)
	set_rw_read()
	# Check each segment controller one at a time
	set_cs(1)
	pulse_enable()
	busy1 = GPIO.input(Pin.DB7)
	display1 = GPIO.input(Pin.DB5)
	resetting1 = GPIO.input(Pin.DB4)
	set_cs(2)
	pulse_enable()
	busy2 = GPIO.input(Pin.DB7)
	display2 = GPIO.input(Pin.DB5)
	resetting2 = GPIO.input(Pin.DB4)
	set_rw_write()
	if busy1 or busy2: busy = 1; else busy = 0
	if display1 or display2: display = 1; else display = 0
	# display will return 0 if on, therefore if either display is off, it will be 1
	# This will signal that one or both displays need to be turned on
	if resetting1 or resetting2: resetting = 1; else resetting = 0
	return busy, display, resetting

def set_data_bits(databyte):
	for pin, state in zip(data_pins, "%08b" % databyte):
		GPIO.output(pin, state == "1")
		# Byte must be given in binary. Bits are stringified and zipped with data pins
		# For any pin, if state is the string "0", comparing against the string "1"
		# will be false and thus set the pin state to low.

def send_byte(databyte):
	set_data_bits(databyte)
	pulse_enable()
	while "busy":
		busy_state = status_read()
		if not busy_state[0]:
			break
		else:
			time.sleep(0.0001) # 100usec, well over the 60usec max busy time

def init():
	# Refer to https://github.com/crystalfontz/Neotec-NT7108/blob/main/NT7108/NT7108.ino
	# (Arduino code) for examples - written in C++ so needs to be converted
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	for pin in Pin:
		GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
	GPIO.output(Pin.RST, 1)
	# Loop below is same as in send_byte() except reading third state instead of first
	while "still booting":
		ready_state = status_read()
		if not ready_state[2]:
			break
		else:
			time.sleep(0.0001)
	GPIO.output(Pin.RS, 0)
	set_cs(3)
	set_rw_write()
	send_byte(0b00111111) # Display on
	send_byte(0b01000000) # Y addr 0
	send_byte(0b10111000) # X addr (page) 0
	send_byte(0b11000000) # Z addr (display start line)
