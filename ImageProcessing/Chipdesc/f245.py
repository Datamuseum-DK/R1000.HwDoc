#!/usr/bin/env python3

''' 74x245 - Octal Bus Transceiver, Non-Inverting Outputs '''

from Chipdesc.chip import Chip, Pin

class F245_AB(Chip):

    ''' 74x245 - Octal Bus Transceiver, Non-Inverting Outputs '''

    symbol_name = "F245AB"

    checked = "VAL 0069"

    symbol = '''
      |  |
      |  |
     1v19v
   +--+--o--+
   |        |
   | DIR OE |
  2|        |18
===+A0    B0+===
  3|        |17
===+A1    B1+===
  4|        |16
===+A2    B2+===
  5|        |15
===+A3    B3+===
  6|        |14
===+A4    B4+===
  7|        |13
===+A5    B5+===
  8|        |12
===+A6    B6+===
  9|  xnn   |11
===+A7    B7+===
   |        |
   | _      |
   +--------+
'''

class F245_BA(Chip):

    ''' 74x245 - Octal Bus Transceiver, Non-Inverting Outputs '''

    symbol_name = "F245BA"

    checked = "MEM32 0010"

    symbol = '''
      |  |
      |  |
      v19v1
   +--o--+--+
   |        |
   | OE DIR |
 18|   0→   |2
===+B0 ←1 A0+===
 17|        |3
===+B1    A1+===
 16|        |4
===+B2    A2+===
 15|        |5
===+B3    A3+===
 14|        |6
===+B4    A4+===
 13|        |7
===+B5    A5+===
 12|        |8
===+B6    A6+===
 11|  xnn   |9
===+B7    A7+===
   |        |
   | _      |
   +--------+
'''

if __name__ == "__main__":
    F245_AB(__file__).main()
    F245_BA(__file__).main()
