#!/usr/bin/env python3

''' N bit '244-style buffer '''

from chip import Chip

class XBUF(Chip):

    ''' N bit '244-style register '''

    def __init__(self, npins):
        self.xreg_npins = npins
        self.symbol_name = "XBUF%d" % npins
        self.symbol = ''
        self.symbol += '      |   |\n'
        self.symbol += '      |   |\n'
        self.symbol += '     %v  %v\n'
        self.symbol += '   +--o---o--+\n'
        self.symbol += '   | INV  OE |\n'
        self.symbol += '   |         |\n'

        for i in range(1, npins + 1):
            if i == npins:
                self.symbol += '  %|   xnn   |%\n'
            else:
                self.symbol += '  %|         |%\n'
            self.symbol += '-->+%-4s %4s+===\n' % ("I%d" % (i-1), "Y%d" % (i-1))
        self.symbol += '   |  _      |\n'
        self.symbol += '   +---------+\n'
        super().__init__()


class BUF(Chip):

    ''' N bit '244-style register '''

    def __init__(self, npins):
        self.xreg_npins = npins
        self.symbol_name = "BUF%d" % npins
        self.symbol = ''
        self.symbol += '      |   |\n'
        self.symbol += '      |   |\n'
        self.symbol += '     %v  %v\n'
        self.symbol += '   +--o---o--+\n'
        self.symbol += '   | INV  OE |\n'
        self.symbol += '   |         |\n'
        self.symbol += '   |         |\n'
        self.symbol += '  %|         |%\n'
        self.symbol += '-->+=I0   Y0=+===\n'
        self.symbol += '  %|         |%\n'
        self.symbol += '-->+=%-4s%4s+===\n' % ("I%d" % (npins-1), "Y%d=" % (npins-1))
        self.symbol += '   |         |\n'
        self.symbol += '   |         |\n'
        self.symbol += '   |         |\n'
        self.symbol += '   |  xnn    |\n'
        self.symbol += '   |         |\n'
        self.symbol += '   |  _      |\n'
        self.symbol += '   +---------+\n'
        super().__init__()

if __name__ == "__main__":
    XBUF(4).main()
    XBUF(6).main()
    XBUF(8).main()
    XBUF(9).main()
    XBUF(12).main()
    XBUF(14).main()
    XBUF(16).main()
    XBUF(20).main()
    XBUF(21).main()
    XBUF(24).main()
    XBUF(32).main()
    XBUF(48).main()
    XBUF(56).main()
    XBUF(64).main()
    BUF(64).main()
