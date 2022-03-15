#!/usr/bin/env python3

''' N bit two input mux with common select '''

from chip import Chip

class XMUX(Chip):

    ''' N bit two input mux with common select '''

    def __init__(self, npins):
        self.xreg_npins = npins
        self.symbol_name = "XMUX%d" % npins
        self.symbol = ''
        self.symbol += '      |  |\n'
        self.symbol += '      |  |\n'
        self.symbol += '     %v %v\n'
        self.symbol += '   +--+--o--+\n'
        self.symbol += '   |        |\n'
        self.symbol += '   |  S  E  |\n'

        for i in range(npins):
            if not i:
                self.symbol += '  %|        |%\n'
                self.symbol += '-->+%-4s INVo<--\n' % ("A%d" % i)
            else:
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

    def other_macros(self, file):
        file.write("#define %s_PINLIST" % self.symbol_name)
        for pin in self.pins:
            if "Y" in pin.name:
                file.write(" \\\n\tsc_out <sc_logic> pin%s;" % pin.number)
            else:
                file.write(" \\\n\tsc_in <sc_logic> pin%s;" % pin.number)
        file.write("\n")
        file.write("\n")
        file.write("#ifdef ANON_PINS\n")
        file.write("#define PIN_SETS(macro)")
        for i in range(0, self.xreg_npins):
            file.write(" \\\n\tmacro(PIN_A%d, PIN_B%d, PIN_Y%d)" % (i, i, i))
        file.write("\n")
        file.write("#endif\n")
           
if __name__ == "__main__":
    XMUX(6).main()
    XMUX(7).main()
    XMUX(16).main()
