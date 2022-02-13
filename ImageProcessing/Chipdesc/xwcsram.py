#!/usr/bin/env python3

''' WCS RAM 16384x8 '''

from Chipdesc.chip import Chip

class XWCSRAM(Chip):

    ''' WCS RAM 16384x8 '''

    symbol_name = "XWCSRAM"

    symbol = '''
        |
        |
      31v
   +----o---+
   |   WE   |
  1|        |2
-->+D0    Q0+-->
  3|        |4
-->+D1    Q1+-->
  5|        |6
-->+D2    Q2+-->
  7|        |8
-->+D3    Q3+-->
  9|        |10
-->+D4    Q4+-->
 11|        |12
-->+D5    Q5+-->
 13|        |14
-->+D6    Q6+-->
 15|        |16
-->+D7    Q7+-->
   |        |
 17|        |
-->+A0      |
 18|        |
-->+A1      |
 19|        |
-->+A2      |
 20|        |
-->+A3      |
 21|        |
-->+A4      |
 22|        |
-->+A5      |
 23|        |
-->+A6      |
 24|        |
-->+A7      |
 25|        |
-->+A8      |
 26|        |
-->+A9      |
 27|        |
-->+A10     |
 28|        |
-->+A11     |
 29|        |
-->+A12     |
 30|        |
-->+A13     |
   |        |
   |  xnn   |
   |  _     |
   +--------+
'''

if __name__ == "__main__":
    XWCSRAM(__file__).main()