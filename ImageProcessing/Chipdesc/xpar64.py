#!/usr/bin/env python3

''' 8x8 parity generator '''

from Chipdesc.chip import Chip

class XPAR18(Chip):

    ''' 2x9 parity generator '''

    symbol_name = "XPAR18"

    symbol = '''
         |
         |
        %v
   +-----o-----+
  %|     ODD   |%
-->+I0       P0+-->
  %|           |%
-->+I1       P1+-->
  %|           |
-->+I2         |
  %|           |%
-->+I3     PALL+-->
  %|           |
-->+I4         |
  %|           |
-->+I5         |
  %|           |
-->+I6         |
  %|           |
-->+I7         |
  %|           |
-->+I8         |
  %|           |
-->+I9         |
  %|           |
-->+I10        |
  %|           |
-->+I11        |
  %|           |
-->+I12        |
  %|           |
-->+I13        |
  %|           |
-->+I14        |
  %|           |
-->+I15        |
  %|           |
-->+I16        |
  %|           |
-->+I17        |
   |           |
   |           |
   |    xnn    |
   |           |
   | _         |
   +-----------+
'''


class XPAR64(Chip):

    ''' 8x8 parity generator '''

    symbol_name = "XPAR64"

    symbol = '''
         |
         |
        1v
   +-----o-----+
  2|    ODD    |66
-->+I0       P0+-->
  3|           |67
-->+I1       P1+-->
  4|           |68
-->+I2       P2+-->
  5|           |69
-->+I3       P3+-->
  6|           |70
-->+I4       P4+-->
  7|           |71
-->+I5       P5+-->
  8|           |72
-->+I6       P6+-->
  9|           |73
-->+I7       P7+-->
 10|           |
-->+I8         |
 11|           |74
-->+I9     PALL+-->
 12|           |
-->+I10        |
 13|           |
-->+I11        |
 14|           |
-->+I12        |
 15|           |
-->+I13        |
 16|           |
-->+I14        |
 17|           |
-->+I15        |
 18|           |
-->+I16        |
 19|           |
-->+I17        |
 20|           |
-->+I18        |
 21|           |
-->+I19        |
 22|           |
-->+I20        |
 23|           |
-->+I21        |
 24|           |
-->+I22        |
 25|           |
-->+I23        |
 26|           |
-->+I24        |
 27|           |
-->+I25        |
 28|           |
-->+I26        |
 29|           |
-->+I27        |
 30|           |
-->+I28        |
 31|           |
-->+I29        |
 32|           |
-->+I30        |
 33|           |
-->+I31        |
 34|           |
-->+I32        |
 35|           |
-->+I33        |
 36|           |
-->+I34        |
 37|           |
-->+I35        |
 38|           |
-->+I36        |
 39|           |
-->+I37        |
 40|           |
-->+I38        |
 41|           |
-->+I39        |
 42|           |
-->+I40        |
 43|           |
-->+I41        |
 44|           |
-->+I42        |
 45|           |
-->+I43        |
 46|           |
-->+I44        |
 47|           |
-->+I45        |
 48|           |
-->+I46        |
 49|           |
-->+I47        |
 50|           |
-->+I48        |
 51|           |
-->+I49        |
 52|           |
-->+I50        |
 53|           |
-->+I51        |
 54|           |
-->+I52        |
 55|           |
-->+I53        |
 56|           |
-->+I54        |
 57|           |
-->+I55        |
 58|           |
-->+I56        |
 59|           |
-->+I57        |
 60|           |
-->+I58        |
 61|           |
-->+I59        |
 62|           |
-->+I60        |
 63|           |
-->+I61        |
 64|           |
-->+I62        |
 65|    xnn    |
-->+I63        |
   |           |
   | _         |
   +-----------+
'''


class XADRPAR(Chip):

    ''' 8x8 parity generator '''

    def __init__(self):
        self.symbol_name = "XADRPAR"

        l = []
        l.append('   +-----------+')

        out = [0]
        def sect(let, low, pins):
            # l.append('   |           |')
            for pin in range(low, low + pins):
                pn = let + "%d" % pin
                if pin == low:
                    l.append('  %|           |%')
                    l.append('-->+%-3s    PEV%d+-->' % (pn, out[0]))
                elif pin == low + 1:
                    l.append('  %|           |%')
                    l.append('-->+%-3s    POD%d+-->' % (pn, out[0]))
                else:
                    l.append('  %|           |')
                    l.append('-->+%-3s        |' % pn)
            out[0] += 1

        sect("S", 0, 3)
        sect("N", 0, 8)
        sect("N", 8, 8)
        sect("N", 16, 8)
        sect("N", 24, 8)
        sect("O", 0, 8)
        sect("O", 8, 11)
        sect("O", 19, 6)
        sect("B", 0, 7)
        l.append('   |           |%')
        l.append('   |  xnn   TST+<--')
        l.append('   |           |')
        l.append('   | _         |')
        l.append('   +-----------+')

        self.symbol=("\n".join(l))
        super().__init__()

if __name__ == "__main__":
    XPAR18().main()
    XPAR64().main()
    XADRPAR().main()
