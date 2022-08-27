#!/usr/bin/env python3

''' 74x169 - Synchronous 4-Bit Bidirectional Counters '''

from Chipdesc.chip import Chip

class F169(Chip):

    ''' 74x169 - Synchronous 4-Bit Bidirectional Counters '''

    def __init__(self, width):

        if width == 4:
            self.symbol_name = "F169"
        else:
            self.symbol_name = "F169X%d" % (width // 4)

        self.checked = "TYP 0018"

        lines = []
        lines.append("      |  |  |")
        lines.append("      |  |  |")
        lines.append("     %v %v %v")
        lines.append("   +--+--o--+--+")
        lines.append("   |  v        |")
        lines.append("   | CLK LD UP |")
        lines.append("   |           |%")
        lines.append("   |         COo-->")
        for i in range(width):
            lines.append("  %|           |%")
            lines.append("-->+D%-2d     %3s+-->" % (i, "Q%d" % i))
        lines.append("  %|           |")
        lines.append("-->oENP        |")
        lines.append("  %|           |")
        lines.append("-->oENT xnn    |")
        lines.append("   |           |")
        lines.append("   |    _      |")
        lines.append("   +-----------+")

        self.symbol = "\n".join(lines)

        super().__init__()

if __name__ == "__main__":
    F169(4).main()
    F169(8).main()
    F169(12).main()
    F169(16).main()
    F169(20).main()
