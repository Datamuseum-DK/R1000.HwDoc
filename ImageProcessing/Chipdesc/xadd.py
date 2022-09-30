#!/usr/bin/env python3

''' N bit two input mux with common select '''

from chip import Chip

class XADD(Chip):

    ''' N bit two input mux with common select '''

    def __init__(self, npins):
        self.xreg_npins = npins
        self.symbol_name = "XADD%d" % npins
        self.symbol = ''
        self.symbol += '   +--------+\n'
        self.symbol += '  %|        |%\n'
        self.symbol += '-->+CI    CO+-->\n'
        self.symbol += '   |        |\n'

        for i in range(npins):
            self.symbol += '  %|        |\n'
            self.symbol += '-->+%-4s    |\n' % ("A%d" % i)
        self.symbol += '   |        |\n'
        for i in range(npins):
            if i == npins - 1:
                self.symbol += '  %|  xnn   |%\n'
            else:
                self.symbol += '  %|        |%\n'
            self.symbol += '-->+%-3s  %3s+-->\n' % (("B%d" % i), ("Y%d" % i))
        self.symbol += '   |  _     |\n'
        self.symbol += '   +--------+\n'
        super().__init__()

if __name__ == "__main__":
    XADD(8).main()
    XADD(14).main()
