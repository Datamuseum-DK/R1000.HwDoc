#!/usr/bin/env python3

''' two 74x181 - Arithmetic Logic Unit '''

from Chipdesc.chip import Chip, Pin

class XALUN(Chip):

    ''' N 74x181 - Arithmetic Logic Unit '''

    def __init__(self, width):
        self.symbol_name = "XALU%d" % width
        right = [
            "   |%",
            " COo-->",
            "   |%",
            "A=B+-->",
            "   |",
            "   |%",
            "  M+<--",
            "   |%",
            " S0+<--",
            "   |%",
            " S1+<--",
            "   |%",
            " S2+<--",
            "   |%",
            " S3+<--",
        ]

        if width in (24, 32):
            right.append("   |")
            right.append("   |")
            for i in range(0, width, 8):
                right.append("   |%")
                right.append("EQ%d+-->" % (i // 8))
            right.append("   |")
            right.append("   |")
            right.append("   |%")
            right.append("MAG+<--")

        left = [
            "   |   ",
            "   |   ",
            "   |   ",
        ]
        for i in range(width):
            left.append("  %|   ")
            left.append("-->+A%-2d" % i)

        left.append("   |   ")

        for i in range(width):
            left.append("  %|   ")
            left.append("-->+B%-2d" % i)

        while len(right) < len(left) - (2 * width + 4):
            right.append("   |")

        for i in range(width):
            right.append("   |%   ")
            right.append("%3s+-->" % ("Y%d" % i))

        right.append("   |")
        right.append("   |")
        right.append("   |%")
        right.append(" CIo<--")

        self.symbol = ['   +--------------+']
        for i, j in zip(left, right):
            self.symbol.append(i + "        " + j)
        self.symbol.append('   |              |')
        self.symbol.append('   |   _          |')
        self.symbol.append('   +--------------+')

        self.symbol[-5] = self.symbol[-5][:9] + "xnn" + self.symbol[-5][12:]

        self.symbol = "\n".join(self.symbol)

        super().__init__()

if __name__ == "__main__":
    XALUN(8).main()
    XALUN(20).main()
    XALUN(24).main()
    XALUN(32).main()
