#!/usr/bin/env python3

''' SEQ DISP sign-extender '''

from Chipdesc.chip import Chip, FChip, ChipSig

class XDISPSE(FChip):

    ''' SEQ DISP sign-extender '''

    symbol_name = "XDISPSE"

    def __init__(self):
        super().__init__()

        self.sig_left(ChipSig("-->+", "SGEXT"))
        self.sig_left(ChipSig("-->+", "DISP", 0, 15))

        self.sig_right(ChipSig("+-->", "Q", 0, 19))

        self.finish()

if __name__ == "__main__":
    XDISPSE().main()


