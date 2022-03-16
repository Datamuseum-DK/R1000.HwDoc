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

    def other_macros(self, file):
        file.write("#define %s_PINLIST" % self.symbol_name)
        for pin in self.pins:
            if "Y" in pin.name:
                file.write(" \\\n\tsc_out <sc_logic> pin%s;" % pin.number)
            elif "CO" in pin.name:
                file.write(" \\\n\tsc_out <sc_logic> pin%s;" % pin.number)
            else:
                file.write(" \\\n\tsc_in <sc_logic> pin%s;" % pin.number)
        file.write("\n")
        file.write("\n")
        file.write("#ifdef ANON_PINS\n")

        file.write("\n")
        file.write("#define PIN_SETS_A(macro)")
        for i in range(0, self.xreg_npins):
            file.write(" \\\n\tmacro(%d, PIN_A%d)" % (self.xreg_npins - (i+1), i))
        file.write("\n")

        file.write("\n")
        file.write("#define PIN_SETS_B(macro)")
        for i in range(0, self.xreg_npins):
            file.write(" \\\n\tmacro(%d, PIN_B%d)" % (self.xreg_npins - (i+1), i))

        file.write("\n")
        file.write("#define PIN_SETS_IN(macro)")
        file.write(" \\\n\tPIN_SETS_A(macro)")
        file.write(" \\\n\tPIN_SETS_B(macro)")
        file.write(" \\\n\tmacro(0, PIN_CI)\n")
        file.write("\n")

        file.write("\n")
        file.write("#define PIN_SETS_OUT(macro)")
        file.write(" \\\n\tmacro(%d, PIN_CO)" % self.xreg_npins)
        for i in range(0, self.xreg_npins):
            file.write(" \\\n\tmacro(%d, PIN_Y%d)" % (self.xreg_npins - (i+1), i))
        file.write("\n")
        file.write("#endif\n")
           
if __name__ == "__main__":
    XADD(8).main()
