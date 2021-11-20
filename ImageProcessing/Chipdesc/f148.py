#!/usr/bin/env python3

''' 74x148 - 8-Line to 3-Line Priority Encoder '''

from Chipdesc.chip import Chip

class F148(Chip):

    ''' 74x148 - 8-Line to 3-Line Priority Encoder '''

    symbol_name = "F148"

    checked = "VAL 0019"

    symbol = '''
       |
       |
      5v
   +---o---+
   |       |
   |   E   |
  4|       |14
-->oI0   GSo-->
  3|       |15
-->oI1   EZo-->
  2|       |
-->oI2     |
  1|       |6
-->oI3   Y0+-->
 13|       |7
-->oI4   Y1+-->
 12|       |9
-->oI5   Y2+-->
 11|       |
-->oI6     |
 10|       |
-->oI7 xnn |
   |       |
   | _     |
   +-------+

'''

if __name__ == "__main__":
    F148().main()
