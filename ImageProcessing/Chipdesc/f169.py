#!/usr/bin/env python3

''' 74x169 - Synchronous 4-Bit Bidirectional Counters '''

from Chipdesc.chip import Chip

class F169(Chip):

    ''' 74x169 - Synchronous 4-Bit Bidirectional Counters '''

    symbol_name = "F169"

    checked = "TYP 0018"

    symbol = '''
      |  |  |
      |  |  |
     2v 9v 1v
   +--+--o--+--+
   |  v        |
   | CLK LD UP |
   |           |15
   |         COo-->
  6|           |11
-->+D0       Q0+-->
  5|           |12
-->+D1       Q1+-->
  4|           |13
-->+D2       Q2+-->
  3|           |14
-->+D3       Q3+-->
  7|           |
-->oENP        |
 10|           |
-->oENT xnn    |
   |           |
   |    _      |
   +-----------+
'''

if __name__ == "__main__":
    F169().main()
