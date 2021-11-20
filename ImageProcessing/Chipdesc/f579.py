#!/usr/bin/env python3

''' 74x579 - 8-Bit Bidirectional Counter '''

from Chipdesc.chip import Chip

class F579(Chip):

    ''' 74x579 - 8-Bit Bidirectional Counter '''

    symbol_name = "F579"

    checked = "IOC 0064"

    symbol = '''
      |  |  |
      |  |  |
     1v12v11v
   +--+--o--o--+
   |  v        |
   | CLK CS OE |
   |           |15
 20|        C0 o-->
-->oMR         |
 19|           |10
-->oSR      IO0+===
   |           |9
   |        IO1+===
   |           |8
   |        IO2+===
 14|           |7
-->+U/B~    IO3+===
 13|           |5
-->oLD      IO4+===
   |           |4
   |        IO5+===
 18|           |3
-->oCEP     IO6+===
 17|           |2
-->oCET xnn IO7+===
   |           |
   |   _       |
   |           |
   +-----------+
'''

if __name__ == "__main__":
    F579().main()
