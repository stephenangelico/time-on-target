# Broken out into its own file since these will be fairly large

ASCENDER = 6
BASE = 8
DESCENDER = 0 # Not supported on this font
LEADING = 2
LINEHEIGHT = ASCENDER + BASE + DESCENDER
ADVANCEMENT = LINEHEIGHT + LEADING
LETTERSPACING = 1 # Pixels between characters horizontally

# NOTE: Any non-space character will make the pixel active. The width of the first row will determine
# the width of the character (others should all match).

FONT = {
	" ": ["     "] * 14, # Critical - without this for unknown characters, everything will bomb
	":": [ # Slightly narrower than digits
		"        ",
		"        ",
		"  XXXX  ",
		"  XXXX  ",
		"        ",
		"  XXXX  ",
		"  XXXX  ",
	],
}

def _make_font(template):
	letters, *rows = template.split("\n")
	for i, ltr in enumerate(letters):
		FONT[ltr] = [row[i*12:i*12+11] for row in rows]

_make_font("""0123456789
  XXXXXX        XX        XXXXXX      XXXXXX           X    XXXXXXXXXX    XXXXXX    XXXXXXXXXX    XXXXXX      XXXXXX  
 XXXXXXXX      XXX       XXXXXXXX    XXXXXXXX         XX    XXXXXXXXXX   XXXXXXXX   XXXXXXXXXX   XXXXXXXX    XXXXXXXX 
XXX     XX    XXXX      XXX    XXX  XXX    XXX       XXX    XX          XXX    XXX          XX  XXX    XXX  XXX    XXX
XX     XXX   XXXXX      XX      XX  XX      XX      XXXX    XX          XX      XX          XX  XX      XX  XX      XX
XX    XXXX      XX             XX           XX     XX XX    XX          XX                  XX  XX      XX  XX      XX
XX   XXXXX      XX            XX           XXX    XX  XX    XX          XX                 XX   XXX    XXX  XXX     XX
XX  XXX XX      XX           XX       XXXXXXX    XX   XX    XXXXXXXX    XXXXXXX            XX    XXXXXXXX    XXXXXXXXX
XXXXXX  XX      XX          XX        XXXXXXX   XX    XX    XXXXXXXXX   XXXXXXXXX         XX     XXXXXXXX     XXXXXXXX
XXXX    XX      XX         XX              XXX  XXXXXXXXXX         XXX  XX     XXX        XX    XXX    XXX          XX
XXX     XX      XX        XX                XX  XXXXXXXXXX          XX  XX      XX       XX     XX      XX          XX
XX      XX      XX       XX         XX      XX        XX    XX      XX  XX      XX       XX     XX      XX          XX
XX     XXX      XX      XX          XXX    XXX        XX    XXX    XXX  XXX    XXX      XX      XXX    XXX          XX
 XXXXXXXX    XXXXXXX    XXXXXXXXXX   XXXXXXXX         XX     XXXXXXXX    XXXXXXXX       XX       XXXXXXXX           XX
  XXXXXX     XXXXXXX    XXXXXXXXXX    XXXXXX          XX      XXXXXX      XXXXXX        XX        XXXXXX            XX""")
