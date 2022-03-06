#!/usr/bin/env python3

''' 9 bit 1MBIT DRAM '''

from Chipdesc.chip import Chip

class XDRAM9(Chip):

    ''' 9 bit 1MBIT DRAM '''

    symbol_name = "XDRAM9"

    symbol = '''
      |  |   |
      |  |   |
     1v 2v 22v
   +--o--o---o--+
   | WE CAS RAS |
   |            |
  3|            |13
-->+A0       DQ0+===
  4|            |14
-->+A1       DQ1+===
  5|            |15
-->+A2       DQ2+===
  6|            |16
-->+A3       DQ3+===
  7|            |17
-->+A4       DQ4+===
  8|            |18
-->+A5       DQ5+===
  9|            |19
-->+A6       DQ6+===
 10|            |20
-->+A7       DQ7+===
 11|            |21
-->+A8       DQ8+===
 12|            |
-->+A9          |
   |            |
   |  xnn       |
   |            |
   |  _         |
   +------------+
'''

if __name__ == "__main__":
    XDRAM9().main()
