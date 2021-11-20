#!/usr/bin/env python3

''' S400ID - see comments on schematic '''

from Chipdesc.chip import Chip

class S400ID(Chip):

    ''' S400ID - see comments on schematic '''

    symbol_name = "S400ID"

    symbol = '''
   +--------+
   |        |
  1|        |
<->+A  _    |
   |        |
   |        |
 15|        |
<->+B       |
   |   xnn  |
   | SPAR16 |
   +--------+
'''

if __name__ == "__main__":
    S400ID().main()
