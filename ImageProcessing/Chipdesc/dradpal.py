#!/usr/bin/env python3

''' PAL22V10 - Programmable Logic Device '''

# XXX: Different I/R0 markings on outputs

from Chipdesc.chip import Chip

class DRADPAL(Chip):

    ''' PAL22V10 - Programmable Logic Device '''

    symbol_name = "DRADPAL"

    checked = "MEM32 28"

    symbol = '''
   +----------+
  1|          |
-->+I0/CLK    |
  2|          |23
-->+I1   R0 D0+-->
  3|          |22
-->+I2   R0 D1+-->
  4|          |21
-->+I3   RO D2+-->
  5|          |20
-->+I4   RO D3+-->
  6|          |19
-->+I5   RO D4+-->
  7|          |18
-->+I6   RO D5+-->
  8|          |17
-->+I7    I D6+<--
  9|          |16
-->+I8    I D7+<--
 10|          |15
-->+I9    I D8+<--
 11|          |14
-->+I10   I D9+<--
 13|          |
-->+I11  xnn  |
   |          |
   | _        |
   +----------+
'''

if __name__ == "__main__":
    DRADPAL().main()
