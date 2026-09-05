# Broken out into its own file since these will be fairly large

ASCENDER = 9
BASE = 12
DESCENDER = 0
LEADING = 0 # Note: This is not how far it leads (pron leed) but how much lead is used (pron ledd).
LINEHEIGHT = ASCENDER + BASE + DESCENDER
ADVANCEMENT = LINEHEIGHT + LEADING
LETTERSPACING = 3 # Pixels between characters horizontally

FONT = {
	" ": [" " * 18] * 21, # Critical - without this for unknown characters, everything will bomb
	":": [ # TODO
		"        ",
		"        ",
		"        ",
		"        ",
		"  XXXX  ",
		"  XXXX  ",
		"  XXXX  ",
		"  XXXX  ",
		"  XXXX  ",
		"        ",
		"        ",
		"        ",
		"  XXXX  ",
		"  XXXX  ",
		"  XXXX  ",
		"  XXXX  ",
		"  XXXX  ",
		"        ",
		"        ",
		"        ",
		"        ",
	],
}

def _make_font(n, template):
	letters, *rows = template.split("\n")
	for i, ltr in enumerate(letters):
		FONT[ltr] = [row[i*n:i*n+n-1] for row in rows]
# NOTE: Keep the digits all at max width, even if they don't all use it. This
# keeps the display stable during ticking.
_make_font(24, """0123456789
   XXXXXXXXX            XXX            XXXXXXXXX         XXXXXXXXX               XXX      XXXXXXXXXXXXXXX      XXXXXXXXX      XXXXXXXXXXXXXXX      XXXXXXXXX         XXXXXXXXX      
   XXXXXXXXX            XXX            XXXXXXXXX         XXXXXXXXX               XXX      XXXXXXXXXXXXXXX      XXXXXXXXX      XXXXXXXXXXXXXXX      XXXXXXXXX         XXXXXXXXX      
   XXXXXXXXX            XXX            XXXXXXXXX         XXXXXXXXX               XXX      XXXXXXXXXXXXXXX      XXXXXXXXX      XXXXXXXXXXXXXXX      XXXXXXXXX         XXXXXXXXX      
XXX         XXX      XXXXXX         XXX         XXX   XXX         XXX         XXXXXX      XXX               XXX         XXX               XXX   XXX         XXX   XXX         XXX   
XXX         XXX      XXXXXX         XXX         XXX   XXX         XXX         XXXXXX      XXX               XXX         XXX               XXX   XXX         XXX   XXX         XXX   
XXX         XXX      XXXXXX         XXX         XXX   XXX         XXX         XXXXXX      XXX               XXX         XXX               XXX   XXX         XXX   XXX         XXX   
XXX      XXXXXX         XXX                  XXX                  XXX      XXX   XXX      XXX               XXX                           XXX   XXX         XXX   XXX         XXX   
XXX      XXXXXX         XXX                  XXX                  XXX      XXX   XXX      XXX               XXX                           XXX   XXX         XXX   XXX         XXX   
XXX      XXXXXX         XXX                  XXX                  XXX      XXX   XXX      XXX               XXX                           XXX   XXX         XXX   XXX         XXX   
XXX   XXX   XXX         XXX               XXX            XXXXXXXXX      XXX      XXX      XXXXXXXXXXXX      XXXXXXXXXXXX               XXX         XXXXXXXXX         XXXXXXXXXXXX   
XXX   XXX   XXX         XXX               XXX            XXXXXXXXX      XXX      XXX      XXXXXXXXXXXX      XXXXXXXXXXXX               XXX         XXXXXXXXX         XXXXXXXXXXXX   
XXX   XXX   XXX         XXX               XXX            XXXXXXXXX      XXX      XXX      XXXXXXXXXXXX      XXXXXXXXXXXX               XXX         XXXXXXXXX         XXXXXXXXXXXX   
XXXXXX      XXX         XXX            XXX                        XXX   XXXXXXXXXXXXXXX               XXX   XXX         XXX            XXX      XXX         XXX               XXX   
XXXXXX      XXX         XXX            XXX                        XXX   XXXXXXXXXXXXXXX               XXX   XXX         XXX            XXX      XXX         XXX               XXX   
XXXXXX      XXX         XXX            XXX                        XXX   XXXXXXXXXXXXXXX               XXX   XXX         XXX            XXX      XXX         XXX               XXX   
XXX         XXX         XXX         XXX               XXX         XXX            XXX      XXX         XXX   XXX         XXX         XXX         XXX         XXX               XXX   
XXX         XXX         XXX         XXX               XXX         XXX            XXX      XXX         XXX   XXX         XXX         XXX         XXX         XXX               XXX   
XXX         XXX         XXX         XXX               XXX         XXX            XXX      XXX         XXX   XXX         XXX         XXX         XXX         XXX               XXX   
   XXXXXXXXX         XXXXXXXXX      XXXXXXXXXXXXXXX      XXXXXXXXX               XXX         XXXXXXXXX         XXXXXXXXX            XXX            XXXXXXXXX                  XXX   
   XXXXXXXXX         XXXXXXXXX      XXXXXXXXXXXXXXX      XXXXXXXXX               XXX         XXXXXXXXX         XXXXXXXXX            XXX            XXXXXXXXX                  XXX   
   XXXXXXXXX         XXXXXXXXX      XXXXXXXXXXXXXXX      XXXXXXXXX               XXX         XXXXXXXXX         XXXXXXXXX            XXX            XXXXXXXXX                  XXX   """)
