#!/usr/bin/env python3

''' 74x163 - Synchronous 4-Bit Binary Counters '''

from Chipdesc.chip import Chip

class F163(Chip):

    ''' 74x163 - Synchronous 4-Bit Binary Counters '''

    symbol_name = "F163"

    checked = "IOC 0064"

    symbol = '''
      |  |  |
      |  |  |
     2v 9v 1v
   +--+--o--o--+
   |  v        |
   | CLK LD CLR|
   |           |15
   |         C0+-->
  6|           |11
-->+D0       Q0+-->
  5|           |12
-->+D1       Q1+-->
  4|           |13
-->+D2       Q2+-->
  3|           |14
-->+D3       Q3+-->
  7|           |
-->+ENP        |
 10|           |
-->+ENT xnn    |
   |           |
   |    _      |
   +-----------+
'''

if __name__ == "__main__":
    F163().main()
