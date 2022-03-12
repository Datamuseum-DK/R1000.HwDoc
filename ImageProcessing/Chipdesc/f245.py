#!/usr/bin/env python3

''' 74x245 - Octal Bus Transceiver, Non-Inverting Outputs '''

from Chipdesc.chip import Chip, Pin

class F245(Chip):

    ''' 74x245 - Octal Bus Transceiver, Non-Inverting Outputs '''

    symbol_name = "F245"

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


if __name__ == "__main__":
    F245(__file__).main()
