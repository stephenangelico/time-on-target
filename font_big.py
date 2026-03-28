# Broken out into its own file since these will be fairly large

ASCENDER = 12
BASE = 16
DESCENDER = 0
LEADING = 0 # Note: This is not how far it leads (pron leed) but how much lead is used (pron ledd).
LINEHEIGHT = ASCENDER + BASE + DESCENDER
ADVANCEMENT = LINEHEIGHT + LEADING
LETTERSPACING = 4 # Pixels between characters horizontally

FONT = {
	" ": [" " * 24] * 28, # Critical - without this for unknown characters, everything will bomb
	":": [ # TODO
		"  ",
	],
}

def _make_font(n, template):
	letters, *rows = template.split("\n")
	for i, ltr in enumerate(letters):
		FONT[ltr] = [row[i*n:i*n+n-1] for row in rows]
# NOTE: Keep the digits all at max width, even if they don't all use it. This
# keeps the display stable during ticking.
_make_font(24, """0123456789
    XXXXXXXXXXXX                XXXX                XXXXXXXXXXXX            XXXXXXXXXXXX                    XXXX        XXXXXXXXXXXXXXXXXXXX        XXXXXXXXXXXX        XXXXXXXXXXXXXXXXXXXX        XXXXXXXXXXXX            XXXXXXXXXXXX        
    XXXXXXXXXXXX                XXXX                XXXXXXXXXXXX            XXXXXXXXXXXX                    XXXX        XXXXXXXXXXXXXXXXXXXX        XXXXXXXXXXXX        XXXXXXXXXXXXXXXXXXXX        XXXXXXXXXXXX            XXXXXXXXXXXX        
    XXXXXXXXXXXX                XXXX                XXXXXXXXXXXX            XXXXXXXXXXXX                    XXXX        XXXXXXXXXXXXXXXXXXXX        XXXXXXXXXXXX        XXXXXXXXXXXXXXXXXXXX        XXXXXXXXXXXX            XXXXXXXXXXXX        
    XXXXXXXXXXXX                XXXX                XXXXXXXXXXXX            XXXXXXXXXXXX                    XXXX        XXXXXXXXXXXXXXXXXXXX        XXXXXXXXXXXX        XXXXXXXXXXXXXXXXXXXX        XXXXXXXXXXXX            XXXXXXXXXXXX        
XXXX            XXXX        XXXXXXXX            XXXX            XXXX    XXXX            XXXX            XXXXXXXX        XXXX                    XXXX            XXXX                    XXXX    XXXX            XXXX    XXXX            XXXX    
XXXX            XXXX        XXXXXXXX            XXXX            XXXX    XXXX            XXXX            XXXXXXXX        XXXX                    XXXX            XXXX                    XXXX    XXXX            XXXX    XXXX            XXXX    
XXXX            XXXX        XXXXXXXX            XXXX            XXXX    XXXX            XXXX            XXXXXXXX        XXXX                    XXXX            XXXX                    XXXX    XXXX            XXXX    XXXX            XXXX    
XXXX            XXXX        XXXXXXXX            XXXX            XXXX    XXXX            XXXX            XXXXXXXX        XXXX                    XXXX            XXXX                    XXXX    XXXX            XXXX    XXXX            XXXX    
XXXX        XXXXXXXX            XXXX                        XXXX                        XXXX        XXXX    XXXX        XXXX                    XXXX                                    XXXX    XXXX            XXXX    XXXX            XXXX    
XXXX        XXXXXXXX            XXXX                        XXXX                        XXXX        XXXX    XXXX        XXXX                    XXXX                                    XXXX    XXXX            XXXX    XXXX            XXXX    
XXXX        XXXXXXXX            XXXX                        XXXX                        XXXX        XXXX    XXXX        XXXX                    XXXX                                    XXXX    XXXX            XXXX    XXXX            XXXX    
XXXX        XXXXXXXX            XXXX                        XXXX                        XXXX        XXXX    XXXX        XXXX                    XXXX                                    XXXX    XXXX            XXXX    XXXX            XXXX    
XXXX    XXXX    XXXX            XXXX                    XXXX                XXXXXXXXXXXX        XXXX        XXXX        XXXXXXXXXXXXXXXX        XXXXXXXXXXXXXXXX                    XXXX            XXXXXXXXXXXX            XXXXXXXXXXXXXXXX    
XXXX    XXXX    XXXX            XXXX                    XXXX                XXXXXXXXXXXX        XXXX        XXXX        XXXXXXXXXXXXXXXX        XXXXXXXXXXXXXXXX                    XXXX            XXXXXXXXXXXX            XXXXXXXXXXXXXXXX    
XXXX    XXXX    XXXX            XXXX                    XXXX                XXXXXXXXXXXX        XXXX        XXXX        XXXXXXXXXXXXXXXX        XXXXXXXXXXXXXXXX                    XXXX            XXXXXXXXXXXX            XXXXXXXXXXXXXXXX    
XXXX    XXXX    XXXX            XXXX                    XXXX                XXXXXXXXXXXX        XXXX        XXXX        XXXXXXXXXXXXXXXX        XXXXXXXXXXXXXXXX                    XXXX            XXXXXXXXXXXX            XXXXXXXXXXXXXXXX    
XXXXXXXX        XXXX            XXXX                XXXX                                XXXX    XXXXXXXXXXXXXXXXXXXX                    XXXX    XXXX            XXXX                XXXX        XXXX            XXXX                    XXXX    
XXXXXXXX        XXXX            XXXX                XXXX                                XXXX    XXXXXXXXXXXXXXXXXXXX                    XXXX    XXXX            XXXX                XXXX        XXXX            XXXX                    XXXX    
XXXXXXXX        XXXX            XXXX                XXXX                                XXXX    XXXXXXXXXXXXXXXXXXXX                    XXXX    XXXX            XXXX                XXXX        XXXX            XXXX                    XXXX    
XXXXXXXX        XXXX            XXXX                XXXX                                XXXX    XXXXXXXXXXXXXXXXXXXX                    XXXX    XXXX            XXXX                XXXX        XXXX            XXXX                    XXXX    
XXXX            XXXX            XXXX            XXXX                    XXXX            XXXX                XXXX        XXXX            XXXX    XXXX            XXXX            XXXX            XXXX            XXXX                    XXXX    
XXXX            XXXX            XXXX            XXXX                    XXXX            XXXX                XXXX        XXXX            XXXX    XXXX            XXXX            XXXX            XXXX            XXXX                    XXXX    
XXXX            XXXX            XXXX            XXXX                    XXXX            XXXX                XXXX        XXXX            XXXX    XXXX            XXXX            XXXX            XXXX            XXXX                    XXXX    
XXXX            XXXX            XXXX            XXXX                    XXXX            XXXX                XXXX        XXXX            XXXX    XXXX            XXXX            XXXX            XXXX            XXXX                    XXXX    
    XXXXXXXXXXXX            XXXXXXXXXXXX        XXXXXXXXXXXXXXXXXXXX        XXXXXXXXXXXX                    XXXX            XXXXXXXXXXXX            XXXXXXXXXXXX                XXXX                XXXXXXXXXXXX                        XXXX    
    XXXXXXXXXXXX            XXXXXXXXXXXX        XXXXXXXXXXXXXXXXXXXX        XXXXXXXXXXXX                    XXXX            XXXXXXXXXXXX            XXXXXXXXXXXX                XXXX                XXXXXXXXXXXX                        XXXX    
    XXXXXXXXXXXX            XXXXXXXXXXXX        XXXXXXXXXXXXXXXXXXXX        XXXXXXXXXXXX                    XXXX            XXXXXXXXXXXX            XXXXXXXXXXXX                XXXX                XXXXXXXXXXXX                        XXXX    
    XXXXXXXXXXXX            XXXXXXXXXXXX        XXXXXXXXXXXXXXXXXXXX        XXXXXXXXXXXX                    XXXX            XXXXXXXXXXXX            XXXXXXXXXXXX                XXXX                XXXXXXXXXXXX                        XXXX    """)
