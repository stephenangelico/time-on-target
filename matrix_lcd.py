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

def set_di(mode):
	if mode == "data":
		GPIO.output(Pin.RS, 1)
	elif mode == "inst":
		GPIO.output(Pin.RS, 0)

def set_rw(mode):
	if mode == "read":
		GPIO.output(Pin.RW, 1)
		for pin in data_pins:
			GPIO.setup(pin, GPIO.IN)
	elif mode == "write":
		GPIO.output(Pin.RW, 0)
		for pin in data_pins:
			GPIO.setup(pin, GPIO.OUT)

def set_cs(chip):
	GPIO.output(Pin.CS1, chip == 1 or chip == 3)
	GPIO.output(Pin.CS2, chip == 2 or chip == 3)
	pulse_enable()

# Pixels are addressed in vertical segments of 8 pixels.

def set_x(addr):
	# Incrementing X address moves down the display by 8 pixels
	if addr < 0 or addr > 7: raise ValueError("X address must be between 0 and 7 (binary 000 to 111)")
	set_di("inst")
	send_byte(0b10111000 + addr)
	set_di("data")

def set_y(addr):
	# Incrementing Y address moves left by 1 pixel
	if addr < 0 or addr > 63: raise ValueError("Y address must be between 0 and 63 (binary 000000 to 111111)")
	set_di("inst")
	send_byte(0b01000000 + addr)
	set_di("data")

def set_z(addr):
	# Incrementing Z address shifts the entire display up by 1 pixel (with wraparound)
	if addr < 0 or addr > 63: raise ValueError("Z address must be between 0 and 63 (binary 000000 to 111111)")
	set_di("inst")
	send_byte(0b11000000 + addr)
	set_di("data")

def status_read():
	set_di("inst")
	set_rw("read")
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
	set_rw("write")
	busy = busy1 or busy2
	display = display1 or display2
	# display will return 0 if on, therefore if either display is off, it will be 1
	# This will signal that one or both displays need to be turned on
	resetting = resetting1 or resetting2
	return busy, display, resetting

def send_byte(databyte):
	# Send a byte of data/instruction to the display, pulse_enable and wait until no longer busy
	# Note that you must set register select, R/W and column select BEFORE using this function.
	for pin, state in zip(data_pins, f"{databyte:08b}"):
		GPIO.output(pin, state == "1")
		# Byte must be given in binary. Bits are stringified and zipped with data pins
		# For any pin, if state is the string "0", comparing against the string "1"
		# will be false and thus set the pin state to low.
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
	set_di("inst")
	set_cs(3)
	set_rw("write")
	send_byte(0b00111111) # Display on
	set_y(0)
	set_x(0)
	set_z(0)
