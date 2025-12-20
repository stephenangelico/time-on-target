# Matrix LCD test/library
import RPi.GPIO as GPIO

# Pin GPIO numbers
PIN_RS = 2 # Register Select or Data/Instruction
PIN_RW = 3 # Read/Write
PIN_EN = 4 # Enable (pulsed only)
PIN_DB0 = 25 # Data bit 0
PIN_DB1 = 8  # Data bit 1
PIN_DB2 = 7  # Data bit 2
PIN_DB3 = 1  # Data bit 3
PIN_DB4 = 0  # Data bit 4
PIN_DB5 = 5  # Data bit 5
PIN_DB6 = 6  # Data bit 6
PIN_DB7 = 13 # Data bit 7
PIN_CS1 = 14 # Column Select 1 (columns 1-64)
PIN_CS2 = 15 # Column Select 2 (columns 65-128)
PIN_RST = 18 # Reset

def init():
	GPIO.setmode(BCM)
	GPIO.setwarnings(False)
	# TODO: Figure out the init process
	# Do we need to first pulse the reset line? What (if anything) can we read?
	# Refer to https://github.com/crystalfontz/Neotec-NT7108/blob/main/NT7108/NT7108.ino
	# (Arduino code) for examples - written in C++ so needs to be converted
