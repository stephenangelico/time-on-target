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
	":": [ # Looks better without the leading spaces - much more even between numbers
		"      ",
		"      ",
		"      ",
		"      ",
		"      ",
		" XX   ",
		"XXXX  ",
		"XXXX  ",
		" XX   ",
		"      ",
		"      ",
		"      ",
		"      ",
		" XX   ",
		"XXXX  ",
		"XXXX  ",
		" XX   ",
		"      ",
		"      ",
		"      ",
		"      ",
	],
}

def _make_font(n, template):
	letters, *rows = template.split("\n")
	for i, ltr in enumerate(letters):
		FONT[ltr] = [row[i*n:i*n+n-1] for row in rows]
# NOTE: Keep the digits all at max width, even if they don't all use it. This
# keeps the display stable during ticking.
_make_font(18, """0123456789
   XXXXXXXXX             XX            XXXXXXXXX         XXXXXXXXX                XX      XXXXXXXXXXXXXXX      XXXXXXXXX      XXXXXXXXXXXXXXX      XXXXXXXXX         XXXXXXXXX      
 XXXXXXXXXXXXX          XXX          XXXXXXXXXXXXX     XXXXXXXXXXXXX             XXX      XXXXXXXXXXXXXXX    XXXXXXXXXXXXX    XXXXXXXXXXXXXXX    XXXXXXXXXXXXX     XXXXXXXXXXXXX    
 XXXXXXXXXXXXX         XXXX          XXXXXXXXXXXXX     XXXXXXXXXXXXX            XXXX      XXXXXXXXXXXXXXX    XXXXXXXXXXXXX    XXXXXXXXXXXXXXX    XXXXXXXXXXXXX     XXXXXXXXXXXXX    
XXXX        XXX       XXXXX         XXX        XXXX   XXXX       XXXX          XXXXX      XXX               XXXX       XXXX               XXX   XXXX       XXXX   XXXX       XXXX   
XXX        XXXX      XXXXXX         XXX        XXXX   XXX         XXX         XXXXXX      XXX               XXX         XXX               XXX   XXX         XXX   XXX         XXX   
XXX       XXXXX      XXXXXX         XXX       XXXXX   XXX         XXX        XXXXXXX      XXX               XXX         XXX               XXX   XXX         XXX   XXX         XXX   
XXX      XXXXXX         XXX                  XXXXX                XXX       XXX  XXX      XXX               XXX                          XXX    XXX         XXX   XXX         XXX   
XXX     XXXXXXX         XXX                 XXXXX                XXXX      XXX   XXX      XXX               XXX                          XXX    XXX         XXX   XXX         XXX   
XXX    XXXX XXX         XXX                XXXXX                XXXX      XXX    XXX      XXX               XXX                         XXX     XXXX        XXX   XXXX       XXXX   
XXX   XXXX  XXX         XXX               XXXXX          XXXXXXXXXX      XXX     XXX      XXXXXXXXXXXX      XXXXXXXXXXXX                XXX      XXXXXXXXXXXXX     XXXXXXXXXXXXXX   
XXX  XXXX   XXX         XXX              XXXXX           XXXXXXXXX      XXX      XXX      XXXXXXXXXXXXXX    XXXXXXXXXXXXXX             XXX         XXXXXXXXX       XXXXXXXXXXXXXX   
XXX XXXX    XXX         XXX             XXXXX            XXXXXXXXXX     XXX      XXX      XXXXXXXXXXXXXX    XXXXXXXXXXXXXX             XXX       XXXXXXXXXXXXX       XXXXXXXXXXXX   
XXXXXXX     XXX         XXX            XXXXX                    XXXX    XXXXXXXXXXXXXXX              XXXX   XXX        XXXX           XXX       XXXX       XXXX               XXX   
XXXXXX      XXX         XXX           XXXXX                      XXXX   XXXXXXXXXXXXXXX               XXX   XXX         XXX           XXX       XXX         XXX               XXX   
XXXXX       XXX         XXX          XXXXX                        XXX   XXXXXXXXXXXXXXX               XXX   XXX         XXX          XXX        XXX         XXX               XXX   
XXXX        XXX         XXX         XXXXX             XXX         XXX            XXX      XXX         XXX   XXX         XXX          XXX        XXX         XXX               XXX   
XXX         XXX         XXX         XXXX              XXX         XXX            XXX      XXX         XXX   XXX         XXX         XXX         XXX         XXX               XXX   
XXX        XXXX        XXXXX        XXXX              XXXX        XXX            XXX      XXXX       XXXX   XXXX        XXX         XXX         XXX         XXX               XXX   
 XXXXXXXXXXXXX        XXXXXXX       XXXXXXXXXXXXXXX    XXXXXXXXXXXXX             XXX       XXXXXXXXXXXXX     XXXXXXXXXXXXX         XXX           XXXXXXXXXXXXX                XXX   
 XXXXXXXXXXXXX       XXXXXXXXX      XXXXXXXXXXXXXXX    XXXXXXXXXXXXX             XXX       XXXXXXXXXXXXX     XXXXXXXXXXXXX         XXX           XXXXXXXXXXXXX                XXX   
   XXXXXXXXX         XXXXXXXXX      XXXXXXXXXXXXXXX      XXXXXXXXX               XXX         XXXXXXXXX         XXXXXXXXX           XXX             XXXXXXXXX                  XXX   """)
