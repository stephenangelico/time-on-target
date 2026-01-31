display = [[0] * 128 for _ in range(64)]
def update():
	for row in display:
		print("".join("X" if ch else " " for ch in row))
def init(): pass
# If we have the actual LCD, use that.
try: from matrix_lcd import display, update, init
except ImportError: pass

ASCENDER = 3
BASE = 4
DESCENDER = 0 # TODO: 3
LEADING = 1 # Note: This is not how far it leads (pron leed) but how much lead is used (pron ledd).
LINEHEIGHT = ASCENDER + BASE + DESCENDER
ADVANCEMENT = LINEHEIGHT + LEADING
LETTERSPACING = 1 # Pixels between characters horizontally

# NOTE: Any non-space character will make the pixel active. The width of the first row will determine
# the width of the character (others should all match).
from font import FONT

def draw_text(x, y, text):
	"""Draw text with its baseline starting at (x,y)"""
	rows = display[y - ASCENDER - BASE + 1 : y + DESCENDER + 1]
	for char in text:
		try:
			font = FONT[char]
		except KeyError:
			try:
				font = FONT[char.upper()]
			except KeyError:
				font = FONT[" "]
		for row, pixels in zip(rows, font):
			for i, ch in enumerate(pixels):
				row[x + i] = ch != " "
		x += len(font[0]) + LETTERSPACING

init()
draw_text(0, 6, input("Enter some text: "))
draw_text(0, 6 + ADVANCEMENT, input("Enter some text: "))
update()
