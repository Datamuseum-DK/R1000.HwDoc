#!/usr/bin/env python3

''' 9 bit '652 bus tranceiver '''

from Chipdesc.chip import Chip

class XXCV9(Chip):

    ''' 9 bit '652 bus tranceiver '''

    symbol_name = "XXCV9"

    symbol = '''
   +-----------+
 19|           |22
-->+OEA     OEB+<--
 20|           |23
-->+CBA     CAB+<--
 21|           |24
-->+SBA     SAB+<--
   |           |
  1|           |10
===+A0       B0+===
  2|           |11
===+A1       B1+===
  3|           |12
===+A2       B2+===
  4|           |13
===+A3       B3+===
  5|           |14
===+A4       B4+===
  6|           |15
===+A5       B5+===
  7|           |16
===+A6       B6+===
  8|           |17
===+A7       B7+===
  9|    xnn    |18
===+A8       B8+===
   |           |
   | _         |
   +-----------+
'''

if __name__ == "__main__":
    XXCV9().main()
