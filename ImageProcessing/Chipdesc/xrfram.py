#!/usr/bin/env python3

''' 1024x64 SRAM '''

from Chipdesc.chip import Chip, FChip, ChipSig

class XRFRAM(Chip):

    ''' 1024x64 SRAM '''

    symbol_name = "XRFRAM"

    symbol = '''
       |    |
       |    |
      1v   2v
   +---o----o---+
   |   WE   CS  |
   |            |
  3|            |13
-->+A0       DQ0+<->
  4|            |14
-->+A1       DQ1+<->
  5|            |15
-->+A2       DQ2+<->
  6|            |16
-->+A3       DQ3+<->
  7|            |17
-->+A4       DQ4+<->
  8|            |18
-->+A5       DQ5+<->
  9|            |19
-->+A6       DQ6+<->
 10|            |20
-->+A7       DQ7+<->
 11|            |21
-->+A8       DQ8+<->
 12|            |22
-->+A9       DQ9+<->
   |            |23
   |        DQ10+<->
   |            |24
   |        DQ11+<->
   |            |25
   |        DQ12+<->
   |            |26
   |        DQ13+<->
   |            |27
   |        DQ14+<->
   |            |28
   |        DQ15+<->
   |            |29
   |        DQ16+<->
   |            |30
   |        DQ17+<->
   |            |31
   |        DQ18+<->
   |            |32
   |        DQ19+<->
   |            |33
   |        DQ20+<->
   |            |34
   |        DQ21+<->
   |            |35
   |        DQ22+<->
   |            |36
   |        DQ23+<->
   |            |37
   |        DQ24+<->
   |            |38
   |        DQ25+<->
   |            |39
   |        DQ26+<->
   |            |40
   |        DQ27+<->
   |            |41
   |        DQ28+<->
   |            |42
   |        DQ29+<->
   |            |43
   |        DQ30+<->
   |            |44
   |        DQ31+<->
   |            |45
   |        DQ32+<->
   |            |46
   |        DQ33+<->
   |            |47
   |        DQ34+<->
   |            |48
   |        DQ35+<->
   |            |49
   |        DQ36+<->
   |            |50
   |        DQ37+<->
   |            |51
   |        DQ38+<->
   |            |52
   |        DQ39+<->
   |            |53
   |        DQ40+<->
   |            |54
   |        DQ41+<->
   |            |55
   |        DQ42+<->
   |            |56
   |        DQ43+<->
   |            |57
   |        DQ44+<->
   |            |58
   |        DQ45+<->
   |            |59
   |        DQ46+<->
   |            |60
   |        DQ47+<->
   |            |61
   |        DQ48+<->
   |            |62
   |        DQ49+<->
   |            |63
   |        DQ50+<->
   |            |64
   |        DQ51+<->
   |            |65
   |        DQ52+<->
   |            |66
   |        DQ53+<->
   |            |67
   |        DQ54+<->
   |            |68
   |        DQ55+<->
   |            |69
   |        DQ56+<->
   |            |70
   |        DQ57+<->
   |            |71
   |        DQ58+<->
   |            |72
   |        DQ59+<->
   |            |73
   |        DQ60+<->
   |            |74
   |        DQ61+<->
   |  xnn       |75
   |        DQ62+<->
   |            |76
   |        DQ63+<->
   |            |
   |  _         |
   +------------+
'''

from Chipdesc.chip import Chip, FChip, ChipSig

class XRFRAMD(FChip):

    ''' 1024x64 ram with separate in/out '''

    symbol_name = "XRFRAMD"

    def __init__(self):
        super().__init__()

        self.sig_left(ChipSig("-->+", "D", 0, 63))
        self.sig_right(ChipSig("+===", "Q", 0, 63))
        self.sig_left(ChipSig("-->+", "WE"))
        self.sig_left(ChipSig("-->+", "A", 0, 9))
        self.sig_right(ChipSig("+<--", "OE"))

        self.finish()

if __name__ == "__main__":
    XRFRAM().main()
    XRFRAMD().main()
