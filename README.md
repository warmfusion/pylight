# The PyLight

## Circuit Diagram

The wiring diagram for this circuit is very easy as we simply use the SPI pins from the Raspberry Pi and an additional 5v supply for the LED Strip, ensuring ground is shared.

![Wiring_diagram][1]

## Code

The [clockface.py](clockface.py) script is adapted from a script found on [falldeaf/cloud_lamp][3]'s which provided a great starting point for sending data to the strip.

I'd suggest having a read of the source code to understand a bit more about the specific implentation, however, the high-level approach is:

1. Work out where our virtual hands would be pointing as a ratio between 0 and 1 (where 1=full circle)
2. For each LED in the circle calculate its colour components by
    1. Work out how close the led is to the 'target' pixel
    2. The closer it is, the brighter, and reach 0 when you're 'spread_pixel' distance away.


## Running

Heres a fairly rough and ready implementation stuck to a cork board untill I find a better mounting...

![CorkClock][4]


[1]: https://learn.adafruit.com/system/assets/assets/000/001/589/medium640/raspberry_pi_diagram.png?1396774138 'CC from Adafruit[2]'
[2]: https://learn.adafruit.com/light-painting-with-raspberry-pi/hardware'
[3]: https://github.com/falldeaf/Cloud_Lamp/blob/master/test_scripts/adafruit_ledpixels.py
[4]: assets/clock-face.jpg