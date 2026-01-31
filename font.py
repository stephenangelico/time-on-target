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
}

# When descenders get added, adjust the Q.
_alpha = """ABCDEFGHJKLMNOPQRSTUVWXYZ
  X   XXXX   XXX  XXXX  XXXXX XXXXX  XXX  X   X     X X   X X     X   X X   X  XXX  XXXX   XXX  XXXX   XXX  XXXXX X   X X   X X   X X   X X   X XXXXX
 X X  X   X X   X X   X X     X     X   X X   X     X X  X  X     XX XX X   X X   X X   X X   X X   X X   X   X   X   X X   X X   X X   X X   X     X
X   X X   X X     X   X X     X     X     X   X     X X X   X     X X X XX  X X   X X   X X   X X   X X       X   X   X X   X X   X  X X   X X     X 
XXXXX XXXX  X     X   X XXXX  XXXX  X     XXXXX     X XX    X     X   X X X X X   X XXXX  X   X XXXX   XXX    X   X   X X   X X   X   X     X     X  
X   X X   X X     X   X X     X     X  XX X   X     X X X   X     X   X X  XX X   X X     X   X X X       X   X   X   X X   X X X X  X X    X    X   
X   X X   X X   X X   X X     X     X   X X   X X   X X  X  X     X   X X   X X   X X     X X X X  X  X   X   X   X   X  X X   X X  X   X   X   X    
X   X XXXX   XXX  XXXX  XXXXX X      XXX  X   X  XXX  X   X XXXXX X   X X   X  XXX  X      XXXX X   X  XXX    X    XXX    X    X X  X   X   X   XXXXX"""
_letters, *_rows = _alpha.split("\n")
for _i, _ltr in enumerate(_letters):
	FONT[_ltr] = [_row[_i*6:_i*6+5] for _row in _rows]
