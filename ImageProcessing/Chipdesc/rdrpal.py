#!/usr/bin/env python3

''' PAL16R8 - Programmable Logic Device '''

from Chipdesc.chip import Chip

class RDRPAL(Chip):

    ''' PAL16R8 - Programmable Logic Device '''

    symbol_name = "RDRPAL"

    checked = "MEM32 0018"

    symbol = '''
      |  |
      |  |
     1v11v
   +--+--o--+
   |  v     |
   | CLK OE |
  2|        |19
-->+I0    Q0+-->
  3|        |18
-->+I1    Q1+-->
  4|        |17
-->+I2    Q2+-->
  5|        |16
-->+I3    Q3+-->
  6|        |15
-->+I4    Q4+-->
  7|        |14
-->+I5    Q5+-->
  8|        |13
-->+I6    Q6+-->
  9|   xnn  |12
-->+I7    Q7+-->
   |        |
   | _      |
   +--------+
'''

if __name__ == "__main__":
    RDRPAL().main()
