# Broken out into its own file since these will be fairly large
FONT = {
	" ": ["     "] * 7,
	# "A": [
		# "  X  ",
		# " X X ",
		# "X   X",
		# "XXXXX",
		# "X   X",
		# "X   X",
		# "X   X",
	# ],
	"I": ["X"] * 7, # Special case: Narrow the I. If you don't want this, make it "  X  " instead.
	":": [ # Slightly narrower than digits
		"    ",
		"    ",
		" XX ",
		" XX ",
		"    ",
		" XX ",
		" XX ",
	],
}

def _make_font(template):
	letters, *rows = template.split("\n")
	for i, ltr in enumerate(letters):
		FONT[ltr] = [row[i*6:i*6+5] for row in rows]
# When descenders get added, adjust the Q.
_make_font("""ABCDEFGHJKLMNOPQRSTUVWXYZ
  X   XXXX   XXX  XXXX  XXXXX XXXXX  XXX  X   X     X X   X X     X   X X   X  XXX  XXXX   XXX  XXXX   XXX  XXXXX X   X X   X X   X X   X X   X XXXXX
 X X  X   X X   X X   X X     X     X   X X   X     X X  X  X     XX XX X   X X   X X   X X   X X   X X   X   X   X   X X   X X   X X   X X   X     X
X   X X   X X     X   X X     X     X     X   X     X X X   X     X X X XX  X X   X X   X X   X X   X X       X   X   X X   X X   X  X X   X X     X 
XXXXX XXXX  X     X   X XXXX  XXXX  X     XXXXX     X XX    X     X   X X X X X   X XXXX  X   X XXXX   XXX    X   X   X X   X X   X   X     X     X  
X   X X   X X     X   X X     X     X  XX X   X     X X X   X     X   X X  XX X   X X     X   X X X       X   X   X   X X   X X X X  X X    X    X   
X   X X   X X   X X   X X     X     X   X X   X X   X X  X  X     X   X X   X X   X X     X X X X  X  X   X   X   X   X  X X   X X  X   X   X   X    
X   X XXXX   XXX  XXXX  XXXXX X      XXX  X   X  XXX  X   X XXXXX X   X X   X  XXX  X      XXXX X   X  XXX    X    XXX    X    X X  X   X   X   XXXXX""")
# NOTE: Keep the digits all at max width, even if they don't all use it. This
# keeps the display stable during ticking.
_make_font("""0123456789
 XXX    X    XXX   XXX     X  XXXXX  XXX  XXXXX  XXX   XXX 
X   X  XX   X   X X   X   XX  X     X   X     X X   X X   X
X  XX   X      X      X  X X  X     X         X X   X X   X
X X X   X     X    XXX  X  X  XXXX  XXXX     X   XXX   XXXX
XX  X   X    X        X XXXXX     X X   X    X  X   X     X
X   X   X   X     X   X    X  X   X X   X   X   X   X     X
 XXX   XXX  XXXXX  XXX     X   XXX   XXX    X    XXX      X""")
