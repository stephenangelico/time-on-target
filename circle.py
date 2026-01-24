import time
display = [[0] * 128 for _ in range(64)]
# Draw something. A simple circle for now.
def circle(inner, outer):
	for r, row in enumerate(display):
		for c in range(len(row)):
			d = (r-32) ** 2 + (c/2-32)**2
			row[c] = 700 < d < 800

def line(x1, y1, x2, y2):
	... # TODO

def draw_text(x1, y1, text):
	... # TODO. Need to build a font.

import matrix_lcd
matrix_lcd.init()

def update():
	matrix_lcd.set_y(0) # Allow autoincrement to take us all the way
	for r in range(0, len(display), 8):
		matrix_lcd.set_x(r >> 3) # Assumed to be in cs(3)
		for chip in (1, 2):
			with matrix_lcd.cs(chip):
				base = 64 if chip == 2 else 0
				for c in range(64):
					# Breach encapsulation a bit here
					for i, pin in enumerate(matrix_lcd.data_pins):
						matrix_lcd.GPIO.output(pin, display[r+7-i][base + c])
					matrix_lcd.pulse_enable()

circle(800, 900)
t = time.monotonic()
update()
print("Updated in", time.monotonic() - t)
circle(700, 800)
update()
print("Changed and updated in", time.monotonic() - t)

time.sleep(5)
t = time.monotonic()
matrix_lcd.cls()
print("Cleared in", time.monotonic() - t)
matrix_lcd.GPIO.cleanup()
