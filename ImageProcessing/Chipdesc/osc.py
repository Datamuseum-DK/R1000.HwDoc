#!/usr/bin/env python3

''' DIL Xtal Oscillator '''

from Chipdesc.chip import Chip

class OSC(Chip):

    ''' DIL Xtal Oscillator '''

    symbol_name = "OSC"

    checked = "IOC 0020"

    symbol = '''
   +-----+
   |     |
   |     |
   |     |
   | _   |8
   |  OUT+-->
   | xnn |
   |     |
   |     |
   |     |
   +-----+
'''

if __name__ == "__main__":
    OSC().main()
