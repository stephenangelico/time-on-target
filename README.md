Time On Target
==============

Alarm clock with character LCD status and Google Calendar control

Hardware:
---------

- Raspberry Pi 4B+
- Crytalfontz 128x64 RGB Backlit Matrix LCD
- 400-hole breadboard layout PCB
- PWM booster circuit (parts TODO)
- 10kΩ trimpot (for LCD contrast control)
- Wiring and JST connectors as in Wiring section

Wiring:
-------

TODO: Diagram in Fritzing
LCD pins 1-3 to board JST2 (GND, 5V, VLCD) - LCD power  ** TODO: Switch order to 5V, VLCD, GND **
LCD pins 4-6 to Pi pins L3-7 (GPIO 2,3,4) - LCD Control 1
LCD pins 7-14 to Pi pins R22-28, L27-33 (GPIO 25,8,7,1, 0,5,6,13) - LCD Data
LCD pins 15-18 to Pi pins R8-14 (GPIO 14,15,18, GND) - LCD Control 2
LCD pins 19-22 to board JST4 (PWMOut, R, G, B) - LCD Backlight
Board JST1 to Pi pins R4-6 (5V, GND) - Board Power
Board JST3 to Pi pins L11-15 (GPIO 17,27,22) - Board Button, Button LED, PWM

TODO: explain PWM booster circuit

Next stream: Fritzing part creation
Take a look at all three breadboard views - where should the connectors be?
FritzingCheckPart.py expects terminals to be rectangles - can we use the
rectangles in the centre of each pin?
These are in deeply nested groups which serve an unclear purpose.
Also, the objects currently labelled as the pins and terminals are rendered
underneath the backing while in the same group. This doesn't make sense!
If there is to be a group per pin, keep all of parts (paths and rectangles)
together in it.
Clean up the heavily nested groups and see if behaviour in Fritzing is affected.

Old notes:
Update metadata in stephena-jst3 - DONE
Run FritzingCheckPart.py on stephena-jst2 and stephena-jst4 - DONE
Then edit both first in Inkscape to set layer order and labels - DONE for 2
Then in SciTE to fix object IDs - DONE for 2
Once parts can be imported, ensure pin assignment is correct - DONE for 2
Save parts and bin - DONE for 2
Explore packaging and contributing parts upstream - may need to clean up IDs
Swap JSTs on board for correct versions (inc button non-connector)
Abolish old breadboard and move all wiring of LCD to stripboard
Set wiring of LCD power JST to include Vout (LCD pin 18)

Future stream: soldering
De-solder LCD power JST and replace with 4-pin (should fit right next to PWM JST)
De-solder trimpot wires and redo according to Fritzing diagram
