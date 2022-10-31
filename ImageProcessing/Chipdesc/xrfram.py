#!/usr/bin/env python3

''' 1024x64 SRAM '''

from Chipdesc.chip import Chip, ChipSig, FChip

class XRFRAM(Chip):

    ''' 1024x64 SRAM '''

    symbol_name = "XRFRAM"

    symbol = '''
       |    |
       |    |
      %v   %v
   +---o----o---+
   |   WE   CS  |
   |            |
  %|            |%
-->+A0       DQ0+<->
  %|            |%
-->+A1       DQ1+<->
  %|            |%
-->+A2       DQ2+<->
  %|            |%
-->+A3       DQ3+<->
  %|            |%
-->+A4       DQ4+<->
  %|            |%
-->+A5       DQ5+<->
  %|            |%
-->+A6       DQ6+<->
  %|            |%
-->+A7       DQ7+<->
  %|            |%
-->+A8       DQ8+<->
  %|            |%
-->+A9       DQ9+<->
   |            |%
   |        DQ10+<->
   |            |%
   |        DQ11+<->
   |            |%
   |        DQ12+<->
   |            |%
   |        DQ13+<->
   |            |%
   |        DQ14+<->
   |            |%
   |        DQ15+<->
   |            |%
   |        DQ16+<->
   |            |%
   |        DQ17+<->
   |            |%
   |        DQ18+<->
   |            |%
   |        DQ19+<->
   |            |%
   |        DQ20+<->
   |            |%
   |        DQ21+<->
   |            |%
   |        DQ22+<->
   |            |%
   |        DQ23+<->
   |            |%
   |        DQ24+<->
   |            |%
   |        DQ25+<->
   |            |%
   |        DQ26+<->
   |            |%
   |        DQ27+<->
   |            |%
   |        DQ28+<->
   |            |%
   |        DQ29+<->
   |            |%
   |        DQ30+<->
   |            |%
   |        DQ31+<->
   |            |%
   |        DQ32+<->
   |            |%
   |        DQ33+<->
   |            |%
   |        DQ34+<->
   |            |%
   |        DQ35+<->
   |            |%
   |        DQ36+<->
   |            |%
   |        DQ37+<->
   |            |%
   |        DQ38+<->
   |            |%
   |        DQ39+<->
   |            |%
   |        DQ40+<->
   |            |%
   |        DQ41+<->
   |            |%
   |        DQ42+<->
   |            |%
   |        DQ43+<->
   |            |%
   |        DQ44+<->
   |            |%
   |        DQ45+<->
   |            |%
   |        DQ46+<->
   |            |%
   |        DQ47+<->
   |            |%
   |        DQ48+<->
   |            |%
   |        DQ49+<->
   |            |%
   |        DQ50+<->
   |            |%
   |        DQ51+<->
   |            |%
   |        DQ52+<->
   |            |%
   |        DQ53+<->
   |            |%
   |        DQ54+<->
   |            |%
   |        DQ55+<->
   |            |%
   |        DQ56+<->
   |            |%
   |        DQ57+<->
   |            |%
   |        DQ58+<->
   |            |%
   |        DQ59+<->
   |            |%
   |        DQ60+<->
   |            |%
   |        DQ61+<->
   |  xnn       |%
   |        DQ62+<->
   |            |%
   |        DQ63+<->
   |            |
   |  _         |
   +------------+
'''

class XRFRAMD(Chip):

    ''' 1024x64 SRAM '''

    symbol_name = "XRFRAMD"

    symbol = '''
       |    |
       |    |
      %v   %v
   +---o----o---+
   |   WE   CS  |
   |            |
  %|            |%
-->+AR0      DQ0+<->
  %|            |%
-->+AR1      DQ1+<->
  %|            |%
-->+AR2      DQ2+<->
  %|            |%
-->+AR3      DQ3+<->
  %|            |%
-->+AR4      DQ4+<->
  %|            |%
-->+AR5      DQ5+<->
  %|            |%
-->+AR6      DQ6+<->
  %|            |%
-->+AR7      DQ7+<->
  %|            |%
-->+AR8      DQ8+<->
  %|            |%
-->+AR9      DQ9+<->
   |            |%
   |        DQ10+<->
   |            |%
   |        DQ11+<->
   |            |%
   |        DQ12+<->
   |            |%
   |        DQ13+<->
  %|            |%
-->+AW0     DQ14+<->
  %|            |%
-->+AW1     DQ15+<->
  %|            |%
-->+AW2     DQ16+<->
  %|            |%
-->+AW3     DQ17+<->
  %|            |%
-->+AW4     DQ18+<->
  %|            |%
-->+AW5     DQ19+<->
  %|            |%
-->+AW6     DQ20+<->
  %|            |%
-->+AW7     DQ21+<->
  %|            |%
-->+AW8     DQ22+<->
  %|            |%
-->+AW9     DQ23+<->
   |            |%
   |        DQ24+<->
   |            |%
   |        DQ25+<->
   |            |%
   |        DQ26+<->
   |            |%
   |        DQ27+<->
   |            |%
   |        DQ28+<->
   |            |%
   |        DQ29+<->
   |            |%
   |        DQ30+<->
   |            |%
   |        DQ31+<->
   |            |%
   |        DQ32+<->
   |            |%
   |        DQ33+<->
   |            |%
   |        DQ34+<->
   |            |%
   |        DQ35+<->
   |            |%
   |        DQ36+<->
   |            |%
   |        DQ37+<->
   |            |%
   |        DQ38+<->
   |            |%
   |        DQ39+<->
   |            |%
   |        DQ40+<->
   |            |%
   |        DQ41+<->
   |            |%
   |        DQ42+<->
   |            |%
   |        DQ43+<->
   |            |%
   |        DQ44+<->
   |            |%
   |        DQ45+<->
   |            |%
   |        DQ46+<->
   |            |%
   |        DQ47+<->
   |            |%
   |        DQ48+<->
   |            |%
   |        DQ49+<->
   |            |%
   |        DQ50+<->
   |            |%
   |        DQ51+<->
   |            |%
   |        DQ52+<->
   |            |%
   |        DQ53+<->
   |            |%
   |        DQ54+<->
   |            |%
   |        DQ55+<->
   |            |%
   |        DQ56+<->
   |            |%
   |        DQ57+<->
   |            |%
   |        DQ58+<->
   |            |%
   |        DQ59+<->
   |            |%
   |        DQ60+<->
   |            |%
   |        DQ61+<->
   |  xnn       |%
   |        DQ62+<->
   |            |%
   |        DQ63+<->
   |            |
   |  _         |
   +------------+
'''

class XRFTA(FChip):

    ''' TYP RF A '''

    symbol_name = "XRFTA"

    def __init__(self):
        super().__init__()
        self.sig_left(ChipSig("-->o", "WE"))
        self.sig_left(ChipSig("-->o", "CS"))
        self.sig_left(ChipSig("-->+", "AW", 0, 9))
        self.sig_left(ChipSig("-->+", "D", 0, 63, True))
        self.sig_left(ChipSig("-->+", "RD"))
        self.sig_left(ChipSig("-->+", "A", 0, 5))
        self.sig_left(ChipSig("-->+", "CNT", 0, 9))
        self.sig_left(ChipSig("-->+", "FRM", 0, 4))
        self.sig_left(ChipSig("-->+", "TOS", 0, 3))
        self.sig_right(ChipSig("+===", "Q", 0, 63))
        self.finish(24)

class XRFTB(FChip):

    ''' TYP RF B '''

    symbol_name = "XRFTB"

    def __init__(self):
        super().__init__()
        self.sig_left(ChipSig("-->o", "WE"))
        self.sig_left(ChipSig("-->o", "CS"))
        self.sig_left(ChipSig("-->+", "AW", 0, 9))
        self.sig_left(ChipSig("-->+", "D", 0, 63, True))
        self.sig_left(ChipSig("-->+", "RD"))
        self.sig_left(ChipSig("-->+", "B", 0, 5))
        self.sig_left(ChipSig("-->+", "CNT", 0, 9))
        self.sig_left(ChipSig("-->+", "FRM", 0, 4))
        self.sig_left(ChipSig("-->+", "CSA", 0, 3))
        self.sig_left(ChipSig("-->+", "TOS", 0, 3))
        self.sig_left(ChipSig("-->+", "TRCV"))
        self.sig_left(ChipSig("-->o", "TYP", 0, 63, True))
        self.sig_right(ChipSig("+-->", "Q", 0, 63))
        self.finish(24)


class XRFVB(FChip):

    ''' VAL RF B '''

    symbol_name = "XRFVB"

    def __init__(self):
        super().__init__()
        self.sig_left(ChipSig("-->o", "WE"))
        self.sig_left(ChipSig("-->o", "CS"))
        self.sig_left(ChipSig("-->+", "AW", 0, 9))
        self.sig_left(ChipSig("-->+", "D", 0, 63, True))
        self.sig_left(ChipSig("-->+", "RD"))
        self.sig_left(ChipSig("-->+", "B", 0, 5))
        self.sig_left(ChipSig("-->+", "CNT", 0, 9))
        self.sig_left(ChipSig("-->+", "FRM", 0, 4))
        self.sig_left(ChipSig("-->+", "CSA", 0, 3))
        self.sig_left(ChipSig("-->+", "TOS", 0, 3))
        self.sig_left(ChipSig("-->o", "GETLIT"))
        self.sig_left(ChipSig("-->o", "LHIT"))
        self.sig_left(ChipSig("-->o", "VALDRV"))
        self.sig_left(ChipSig("-->o", "VAL", 0, 63, True))
        self.sig_right(ChipSig("+-->", "Q", 0, 63))
        self.finish(24)

if __name__ == "__main__":
    XRFTA().main()
    XRFTB().main()
    XRFVB().main()
    XRFRAM().main()
    XRFRAMD().main()
