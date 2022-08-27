#!/usr/bin/env python3

''' 74x245 - Octal Bus Transceiver, Non-Inverting Outputs '''

from Chipdesc.chip import Chip, Pin

class F245(Chip):

    ''' 74x245 - Octal Bus Transceiver, Non-Inverting Outputs '''

    def __init__(self, npins=8):
        if npins == 8:
            self.symbol_name = "F245"
        else:
            self.symbol_name = "XBIDIR%d" % npins

        self.symbol =  '''      |  |\n'''
        self.symbol += '''      |  |\n'''
        self.symbol += '''     %v %v\n'''
        self.symbol += '''   +--+--o--+\n'''
        self.symbol += '''   |        |\n'''
        self.symbol += '''   | DIR OE |\n'''
        for i in range(npins):
            if i == npins - 1:
                self.symbol += '''  %|  xnn   |%\n'''
            else:
                self.symbol += '''  %|        |%\n'''
            self.symbol += '''<->+A%-2d  %3s+<->\n''' % (i, "B%d" % i)
        self.symbol += '''   |        |\n'''
        self.symbol += '''   | _      |\n'''
        self.symbol += '''   +--------+\n'''

        super().__init__()

if __name__ == "__main__":
    F245().main()
    F245(11).main()
    F245(16).main()
    F245(32).main()
    F245(64).main()
