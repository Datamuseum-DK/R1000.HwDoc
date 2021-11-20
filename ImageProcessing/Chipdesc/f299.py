#!/usr/bin/env python3

''' 74x299 - 8-Bit Bidirectional Universal Shift Register '''

from Chipdesc.chip import Chip

class F299(Chip):

    ''' 74x299 - 8-Bit Bidirectional Universal Shift Register '''

    symbol_name = "F299"

    checked = "IOC 0050"

    symbol = '''
      |  |
      |  |
    12v 9v
   +--+--o--+
   |  v     |
   | CLK CLR|
 11|        |
-->+RSI     |
  7|        |2
===+DQ0   G1o<--
 13|        |3
===+DQ1   G2o<--
  6|        |
===+DQ2     |
 14|        |
===+DQ3     |
  5|        |
===+DQ4     |
 15|        |
===+DQ5     |
  4|        |8
===+DQ6   Q0+-->
 16|        |17
===+DQ7   Q7+-->
 18|        |
-->+LSI     |
   |        |
   |        |
 19|        |
-->+S0      |
  1|        |
-->+S1 xnn  |
   |        |
   |  _     |
   +--------+
'''

if __name__ == "__main__":
    F299().main()
