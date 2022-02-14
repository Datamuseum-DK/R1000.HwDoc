#!/usr/bin/env python3

''' 16 bit '374-style register '''

from Chipdesc.chip import Chip

class XREG16(Chip):

    ''' 16 bit '374-style register '''

    symbol_name = "XREG16"

    symbol = '''
      |     |
      |     |
     1v    2v
   +--+-----o--+
   |  CLK   OE |
   |           |
  3|           |19
-->+I0       Y0+===
  4|           |20
-->+I1       Y1+===
  5|           |21
-->+I2       Y2+===
  6|           |22
-->+I3       Y3+===
  7|           |23
-->+I4       Y4+===
  8|           |24
-->+I5       Y5+===
  9|           |25
-->+I6       Y6+===
 10|           |26
-->+I7       Y7+===
 11|           |27
-->+I8       Y8+===
 12|           |28
-->+I9       Y9+===
 13|           |29
-->+I10     Y10+===
 14|           |30
-->+I11     Y11+===
 15|           |31
-->+I12     Y12+===
 16|           |32
-->+I13     Y13+===
 17|           |33
-->+I14     Y14+===
 18|           |34
-->+I15     Y15+===
   |           |
   |   xnn     |
   |           |
   | _         |
   +-----------+
'''

if __name__ == "__main__":
    XREG16().main()
