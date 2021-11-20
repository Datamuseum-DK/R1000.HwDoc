#!/usr/bin/env python3

''' EC² TTLDM-35 - TTL Military Logic Delay Module '''

from Chipdesc.chip import Chip

class TTLDM35(Chip):

    ''' EC² TTLDM-35 - TTL Military Logic Delay Module '''

    symbol_name = "DLY_35"

    checked = "MEM32 0029"

    symbol = '''
   +--------+
   |        |
   | xnn    |12
   |     7NS+-->
   |        |4
   |    14NS+-->
  1|        |10
-->+IN  21NS+-->
   |        |6
   |    28NS+-->
   |        |8
   |    35NS+-->
   |        |
   | _      |
   +--------+
'''

if __name__ == "__main__":
    TTLDM35(__file__).main()
