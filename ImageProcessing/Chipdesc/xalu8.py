#!/usr/bin/env python3

''' two 74x181 - Arithmetic Logic Unit '''

from Chipdesc.chip import Chip, Pin

class XALU8(Chip):

    ''' two 74x181 - Arithmetic Logic Unit '''

    symbol_name = "XALU8"

    checked = "VAL 0040"

    symbol = '''
   +--------------+
   |              |26
   |            C0o-->
   |              |27
  1|           A=B+-->
-->+A0            |
  2|              |28
-->+A1           M+<---
  3|              |29
-->+A2          S0+<---
  4|              |30
-->+A3          S1+<---
  5|              |31
-->+A4          S2+<---
  6|              |32
-->+A5          S3+<---
  7|              |
-->+A6            |17
  8|            Y0+-->
-->+A7            |18
   |            Y1+-->
  9|              |19
-->+B0          Y2+-->
 10|              |20
-->+B1          Y3+-->
 11|              |21
-->+B2          Y4+-->
 12|              |22
-->+B3          Y5+-->
 13|              |23
-->+B4          Y6+-->
 14|              |24
-->+B5          Y7+-->
 15|              |
-->+B6            |
 16|     xnn      |25
-->+B7          CIo<--
   |              |
   |    _         |
   +--------------+
'''

if __name__ == "__main__":
    XALU8().main()
