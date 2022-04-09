#!/usr/bin/env python3

''' XMUX16_1 - 16-Line to 1-Line Data Selector / Multiplexer '''

from Chipdesc.chip import Chip

class XMUX16_1(Chip):

    ''' XMUX16_1 - 16-Line to 1-Line Data Selector / Multiplexer '''

    symbol_name = "XMUX16_1"

    symbol = '''
     |  |  |  |
     |  |  |  |
    %v %v %v %v
   +-+--+--+--+-+
   |            |
   | S0 S1 S2 S3|
  %|            |
-->+I0          |
  %|            |
-->+I1          |
  %|            |
-->+I2          |
  %|            |5
-->+I3         Y+-->
  %|            |6
-->+I4        Y~o-->
  %|            |
-->+I5          |
  %|            |
-->+I6          |
  %|            |
-->+I7          |
  %|            |
-->+I8          |
  %|            |
-->+I9          |
  %|            |
-->+I10         |
  %|            |
-->+I11         |
  %|            |
-->+I12         |
  %|            |
-->+I13         |
  %|            |
-->+I14         |
  %|    xnn     |
-->+I15         |
   |            |
   |  _         |
   +------------+
'''

if __name__ == "__main__":
    XMUX16_1().main()
