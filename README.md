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

LCD pins 1-3 and 18 to board JST2 (GND, 5V, VLCD, VREF) - LCD power
LCD pins 4-6 to Pi pins L3-7 (GPIO 2,3,4) - LCD Control 1
LCD pins 7-14 to Pi pins R22-28, L27-33 (GPIO 25,8,7,1, 0,5,6,13) - LCD Data
LCD pins 15-17 to Pi pins R8-14 (GPIO 14,15,18) - LCD Control 2
LCD pins 19-22 to board JST4 (PWMOut, R, G, B) - LCD Backlight
Board JST1 to Pi pins R4-6 (5V, GND) - Board Power
Board JST3 to Pi pins L11-15 (GPIO 17,27,22) - Board Button, Button LED, PWM

TODO: explain PWM booster circuit

Assorted notes:
---------------

Button is on GPIO17. Need to use Pi's internal pull-up resistor:
`GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)`
