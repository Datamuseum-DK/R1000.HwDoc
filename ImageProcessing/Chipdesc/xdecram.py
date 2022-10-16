#!/usr/bin/env python3

''' Decode RAM '''

from Chipdesc.chip import Chip

class XDECRAM(Chip):

    ''' Decode RAM '''

    def __init__(self, npins):

        self.symbol_name = "XDECRAM%d" % npins

        self.symbol = []

        self.symbol.append('        |')
        self.symbol.append('        |')
        self.symbol.append('       %v')
        self.symbol.append('   +----o----+')
        self.symbol.append('   |   CS    |')
        self.symbol.append('   |         |')
        for i in range(16):
            if i < npins:
                self.symbol.append('  %|         |%')
                self.symbol.append('-->+%-3s   %3s+-->' % ("A%d" % i, "Q%d" % i))
            else:
                self.symbol.append('  %|         |')
                self.symbol.append('-->+%-3s      |' % ("A%d" % i))
        self.symbol.append('   |         |')
        self.symbol.append('   |   xnn   |')
        self.symbol.append('   |         |')
        self.symbol.append('   | _       |')
        self.symbol.append('   +---------+')
        self.symbol = "\n".join(self.symbol)
        super().__init__()

if __name__ == "__main__":
    XDECRAM(4).main()
    XDECRAM(8).main()
    XDECRAM(16).main()
