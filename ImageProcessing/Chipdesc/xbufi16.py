#!/usr/bin/env python3

''' 16 bit inverting buffers '''

from Chipdesc.chip import Chip

class XBUFI16(Chip):

    ''' 16 bit inverting buffer '''

    symbol_name = "XBUFI16"

    symbol = '''
         |
         |
        1v
   +-----o-----+
   |    OE     |
  2|           |18
-->+I0       Y0o===
  3|           |19
-->+I1       Y1o===
  4|           |20
-->+I2       Y2o===
  5|           |21
-->+I3       Y3o===
  6|           |22
-->+I4       Y4o===
  7|           |23
-->+I5       Y5o===
  8|           |24
-->+I6       Y6o===
  9|           |25
-->+I7       Y7o===
 10|           |26
-->+I8       Y8o===
 11|           |27
-->+I9       Y9o===
 12|           |28
-->+I10     Y10o===
 13|           |29
-->+I11     Y11o===
 14|           |30
-->+I12     Y12o===
 15|           |31
-->+I13     Y13o===
 16|           |32
-->+I14     Y14o===
 17|           |33
-->+I15     Y15o===
   |           |
   |    xnn    |
   |           |
   | _         |
   +-----------+
'''

if __name__ == "__main__":
    XBUFI16().main()
