#!/usr/bin/env python3

''' Magic MEM board ident '''

from Chipdesc.chip import Chip

class XMEMID(Chip):

    ''' Magic MEM board ident '''

    symbol_name = "XMEMID"

    symbol = '''
   +-------+
   |       |1
   |    ID0+-->
   |       |2
   |    ID1+-->
   |       |
   |   xnn |
   |  _    |
   +-------+
'''

if __name__ == "__main__":
    XMEMID().main()
