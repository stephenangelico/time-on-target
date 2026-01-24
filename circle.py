import time
display = [[0] * 128 for _ in range(64)]
# Draw something. A simple circle for now.
for r, row in enumerate(display):
	for c in range(len(row)):
		d = (r-32) ** 2 + (c/2-32)**2
		if 800 < d < 900: row[c] = 1

import matrix_lcd
matrix_lcd.init()
for r in range(0, len(display), 8):
	matrix_lcd.set_x(r >> 3) # Assumed to be in cs(3)
	for c in range(128):
		with matrix_lcd.cs((c >= 64) + 1):
			matrix_lcd.set_y(c & 63)
			# Breach encapsulation a bit here
			for i, pin in enumerate(matrix_lcd.data_pins):
				matrix_lcd.GPIO.output(pin, display[r+7-i][c])
			matrix_lcd.pulse_enable()

time.sleep(5)
matrix_lcd.cls()
matrix_lcd.GPIO.cleanup()
