#!/usr/bin/env python3

''' WCS RAM 16384x8 '''

from Chipdesc.chip import Chip, FChip, ChipSig

class XWCSRAM2(FChip):

    ''' Writeable Control Store '''

    def __init__(self, width):
        self.symbol_name = "XWCSRAM%d" % width
        super().__init__()

        self.sig_left(ChipSig("-->+", "D", 0, width - 1))
        self.sig_left(ChipSig("-->+", "PIN"))
        self.sig_left(ChipSig("-->+", "A", 0, 15))

        self.sig_right(ChipSig("+-->", "Q", 0, width - 1))
        self.sig_right(ChipSig("+-->", "POUT"))
        self.sig_right(ChipSig("o<--", "WE"))
        self.sig_right(ChipSig("o-->", "APERR"))

        self.finish()

class XWCSRAM(Chip):

    ''' WCS RAM 16384x8 '''

    def __init__(self, width):

        self.symbol_name = "XWCSRAM"
        if width != 8:
            self.symbol_name += "%d" % width

        self.symbol = '''
        |
        |
       %v
   +----o---+
   |   WE   |
'''

        for i in range(width):
            self.symbol += "  %|        |%\n"
            self.symbol += "-->+D%-2d  %3s+-->\n" % (i, "Q%d" % i)

        self.symbol += '''   |        |
  %|        |
-->+A0      |
  %|        |
-->+A1      |
  %|        |
-->+A2      |
  %|        |
-->+A3      |
  %|        |
-->+A4      |
  %|        |
-->+A5      |
  %|        |
-->+A6      |
  %|        |
-->+A7      |
  %|        |
-->+A8      |
  %|        |
-->+A9      |
  %|        |
-->+A10     |
  %|        |
-->+A11     |
  %|        |
-->+A12     |
  %|        |
-->+A13     |
   |        |
   |  xnn   |
   |  _     |
   +--------+
'''

        super().__init__()

if __name__ == "__main__":
    XWCSRAM(8).main()
    XWCSRAM(16).main()
    XWCSRAM2(39).main()
    XWCSRAM(40).main()
    XWCSRAM(42).main()
    XWCSRAM(47).main()
