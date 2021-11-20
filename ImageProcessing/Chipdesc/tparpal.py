#!/usr/bin/env python3

''' PAL16L8 - Programmable Logic Device '''

from Chipdesc.chip import Chip

class TPARPAL(Chip):

    ''' PAL16L8 - Programmable Logic Device '''

    symbol_name = "TPARPAL"

    symbol = '''
   +--------+
  1|        |
-->+I0      |
  2|        |19
-->+I1    O0+-->
  3|        |12
-->+I2    O1+-->
  4|        |18
-->+I3    D0+-->
  5|        |17
-->+I4      |   
  6|        |16
-->+I5    D2+-->
  7|        |15
-->+I6    D3+-->
  8|        |14
-->+I7    D4+-->
  9|        |13
-->+I8    D5+-->
 11|        |
-->+I9 xnn  |
   |        |
   | _      |
   +--------+
'''

if __name__ == "__main__":
    TPARPAL().main()
