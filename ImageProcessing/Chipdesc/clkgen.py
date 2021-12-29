#!/usr/bin/env python3

''' R1000 Clock generator '''

from Chipdesc.chip import Chip

class CLKGEN(Chip):

    ''' R1000 Clock Generator '''

    symbol_name = "CLKGEN"

    symbol = '''
   +--------+
   |        |
   |        |
   |        |1
   |      X2+-->
   |        |2
   |      X2o-->
   |        |3
   | X2PHASE+-->
   |        |4
   |      H1+-->
   |        |5
   |      H2+-->
   |        |6
   |     H1E+-->
   |        |7
   |     H2E+-->
   |        |8
   |      Q1+-->
   |        |9
   |      Q1o-->
   |        |10
   |      Q2+-->
   |        |11
   |      Q2o-->
   |        |12
   |      Q3+-->
   |        |13
   |      Q3o-->
   |        |14
   |      Q4+-->
   |        |15
   |      Q4o-->
   | xnn    |
   |        |
   |  _     |
   +--------+
'''

if __name__ == "__main__":
    CLKGEN().main()
