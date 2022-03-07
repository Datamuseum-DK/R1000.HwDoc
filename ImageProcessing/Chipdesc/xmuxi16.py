#!/usr/bin/env python3

''' 16 + 16 => 16 inverting mux '''

from Chipdesc.chip import Chip

class XMUXI16(Chip):

    ''' 16 + 16 => 16 inverting mux '''

    symbol_name = "XMUXI16"

    symbol = '''
       |   |
       |   |
      1v  2v
   +---+---o---+
   |   S  OE   |
   |           |
  3|           |35
-->+A0       Y0o===
  4|           |36
-->+A1       Y1o===
  5|           |37
-->+A2       Y2o===
  6|           |38
-->+A3       Y3o===
  7|           |39
-->+A4       Y4o===
  8|           |40
-->+A5       Y5o===
  9|           |41
-->+A6       Y6o===
 10|           |42
-->+A7       Y7o===
 11|           |43
-->+A8       Y8o===
 12|           |44
-->+A9       Y9o===
 13|           |45
-->+A10     Y10o===
 14|           |46
-->+A11     Y11o===
 15|           |47
-->+A12     Y12o===
 16|           |48
-->+A13     Y13o===
 17|           |49
-->+A14     Y14o===
 18|           |50
-->+A15     Y15o===
   |           |
   |           |
 19|           |
-->+B0         |
 20|           |
-->+B1         |
 21|           |
-->+B2         |
 22|           |
-->+B3         |
 23|           |
-->+B4         |
 24|           |
-->+B5         |
 25|           |
-->+B6         |
 26|           |
-->+B7         |
 27|           |
-->+B8         |
 28|           |
-->+B9         |
 29|           |
-->+B10        |
 30|           |
-->+B11        |
 31|           |
-->+B12        |
 32|           |
-->+B13        |
 33|           |
-->+B14        |
 34|           |
-->+B15        |
   |           |
   |    xnn    |
   |           |
   | _         |
   +-----------+
'''

if __name__ == "__main__":
    XMUXI16().main()
