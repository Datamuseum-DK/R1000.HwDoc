#!/usr/bin/env python3

''' Dual-port 256x8 Static RAM '''

from Chipdesc.chip import Chip, Pin

class FIFORAM(Chip):

    ''' Dual-port 256x8 Static RAM '''

    symbol_name = "FIFORAM"

    symbol = '''
        ^
        |
       %|
   +----o----+
   |   EQ    |
   |         |
  %|         |
-->+I0       |
  %|         |
-->+I1       |
  %|         |%
-->+I2    AW0+<--
  %|         |%
-->+I3    AW1+<--
  %|         |%
-->+I4    AW2+<--
  %|         |%
-->+I5    AW3+<--
  %|         |%
-->+I6    AW4+<--
  %|         |%
-->+I7    AW5+<--
  %|         |%
-->+I8    AW6+<--
  %|         |%
-->+I9    AW7+<--
  %|         |
-->+I10      |
  %|         |
-->+I11      |
  %|         |%
-->+I12    WEo<--
  %|         |
-->+I13      |
  %|         |
-->+I14      |
  %|         |
-->+I15      |
   |         |
   |         |
   |         |
   |         |
   |         |
   |         |%
   |       Y0+-->
   |         |%
   |       Y1+-->
  %|         |%
-->+RA0    Y2+-->
  %|         |%
-->+RA1    Y3+-->
  %|         |%
-->+RA2    Y4+-->
  %|         |%
-->+RA3    Y5+-->
  %|         |%
-->+RA4    Y6+-->
  %|         |%
-->+RA5    Y7+-->
  %|         |%
-->+RA6    Y8+-->
  %|         |%
-->+RA7    Y9+-->
   |         |%
   |      Y10+-->
   |         |%
   |      Y11+-->
   |         |%
   |      Y12+-->
   |         |%
   |      Y13+-->
   |         |%
   |      Y14+-->
   | xnn     |%
   |      Y15+-->
   |         |
   |  _      |
   |         |
   +---------+
'''

if __name__ == "__main__":
    FIFORAM(__file__).main()
