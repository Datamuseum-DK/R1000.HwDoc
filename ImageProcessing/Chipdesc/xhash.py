#!/usr/bin/env python3

''' 8x8 parity generator '''

from Chipdesc.chip import Chip

class XHASH(Chip):

    ''' mem32 hash generator '''

    def __init__(self):
        self.symbol_name = "XHASH"

        l = []
        l.append('   +-----------+')

        hash = [0]
        def sect(let, low, pins):
            # l.append('   |           |')
            for pin in range(low, low + pins):
                pn = '-->+%-3s' % (let + "%d" % pin)
                if hash[0] < 12:
                    l.append('  %|           |%')
                    l.append(pn + '  %6s+-->' % ("HASH%d" % hash[0]))
                    hash[0] += 1
                else:
                    l.append('  %|           |')
                    l.append(pn + '        |')

        sect("S", 0, 3)
        sect("N", 0, 8)
        sect("N", 8, 8)
        sect("N", 16, 8)
        sect("N", 24, 8)
        sect("O", 0, 8)
        sect("O", 8, 11)
        sect("O", 19, 6)
        l.append('   |           |')
        l.append('   |  xnn      |')
        l.append('   |           |')
        l.append('   | _         |')
        l.append('   +-----------+')

        self.symbol=("\n".join(l))
        super().__init__()

if __name__ == "__main__":
    XHASH().main()
