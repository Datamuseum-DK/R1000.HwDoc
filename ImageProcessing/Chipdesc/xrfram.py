#!/usr/bin/env python3

''' 1024x64 SRAM '''

from Chipdesc.chip import Chip

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

class ChipSig():

    def __init__(self, arrow, name, low = None, high = None, bus=False):
        self.arrow = arrow
        self.name = name
        self.low = low
        self.high = high
        self.bus = bus

    def __iter__(self):
        if self.low is None and self.high is None:
            yield self.name, self.arrow
        elif self.bus:
            yield self.name + "%d" % self.low, self.arrow
            yield self.name + "%d" % self.high, self.arrow
        else:
            for pin in range(self.low, self.high + 1):
                yield self.name + "%d" % pin, self.arrow

    def spacing(self, really):
        if really:
            yield ""
            yield ""
            if 0 and self.high:
                yield ""
                yield ""

class FChip(Chip):

    def __init__(self):
        self.sig_l = []
        self.sig_r = []

    def sig_left(self, signal):
        self.sig_l.append(signal)

    def sig_right(self, signal):
        self.sig_r.append(signal)

    def finish(self, width = 0):
        self.symbol = ''

        left = []
        space = False
        for sig in self.sig_l:
            for _i in sig.spacing(space):
                left.append('   |')
            for nm, arrow in sig:
                left.append('  %|')
                if sig.bus:
                    left.append(arrow + '=' + nm)
                else:
                    left.append(arrow + nm)
 
            space = True

        right = []
        space = False
        for sig in self.sig_r:
            for _i in sig.spacing(space):
                left.append('   |   ')
            for nm, arrow in sig:
                right.append('|%  ')
                if sig.bus:
                    right.append(nm + '=' + arrow)
                else:
                    right.append(nm + arrow)
            space = True

        minwidth = max(len(x) for x in left) + max(len(x) for x in right) + 2
        print("W", width, "MW", minwidth)
        if width == 0:
            width = minwidth
        else:
            assert width >= minwidth

        top_bot = '   +' + '-' * (width - 8) + '+\n'
        spacer = '   |' + ' ' * (width - 8) + '|\n'

        self.symbol += top_bot
        self.symbol += spacer
        self.symbol += spacer.replace('|    ', '| xnn')
        self.symbol += spacer

        while len(left) < len(right):
            left.append('   |')
        while len(right) < len(left):
            right.append('|   ')
        for l, r in zip(left, right):
            pad = " " * (width - (len(l) + len(r)))
            self.symbol += l + pad + r.rstrip() + "\n"

        self.symbol += spacer
        self.symbol += spacer
        self.symbol += spacer.replace('|  ', '| _')
        self.symbol += top_bot

        super().__init__()

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
        self.sig_left(ChipSig("-->+", "TYP", 0, 63, True))
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
        self.sig_left(ChipSig("-->o", "VALOE"))
        self.sig_left(ChipSig("-->+", "VAL", 0, 63, True))
        self.sig_right(ChipSig("+-->", "Q", 0, 63))
        self.finish(24)

if __name__ == "__main__":
    XRFVB().main()
    XRFTB().main()
    XRFRAM().main()
    XRFRAMD().main()
