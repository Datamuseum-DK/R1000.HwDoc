#!/usr/bin/env python3

''' National DS8641 - Quad Unified Bus Tranceiver '''

from Chipdesc.chip import Chip

class DS8641(Chip):

    ''' National DS8641 - Quad Unified Bus Tranceiver '''

    symbol_name = "8641"

    checked = "RESHA 0002"

    symbol = '''
      |  |  |  |
      |  |  |  |
    15v12v 1v 4v
   +--o--o--o--o--+
   |              |
   | B0 B1 B2 B3  |
 14|              |13
-->+IN0       OUT0+-->
 11|              |10
-->+IN1       OUT1+-->
  2|              |3
-->+IN2       OUT2+-->
  5|              |6
-->+IN3       OUT3+-->
   |              |
   |              |
  7|              |
-->oEN0           |
  9|     xnn      |
-->oEN1           |
   |     _        |
   |              |
   +--------------+
'''

if __name__ == "__main__":
    DS8641(__file__).main()
