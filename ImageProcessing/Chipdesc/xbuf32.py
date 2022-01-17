#!/usr/bin/env python3

''' 32 bit buffers '''

from Chipdesc.chip import Chip

class XBUF32(Chip):

    ''' 32 bit buffer '''

    symbol_name = "XBUF32"

    symbol = '''
        |
        |
       1v
   +----o-----+
  2|   OE     |35
-->+I0      Y0+===
  3|          |36
-->+I1      Y1+===
  4|          |37
-->+I2      Y2+===
  5|          |38
-->+I3      Y3+===
  6|          |39
-->+I4      Y4+===
  7|          |40
-->+I5      Y5+===
  8|          |41
-->+I6      Y6+===
  9|          |42
-->+I7      Y7+===
 10|          |43
-->+I8      Y8+===
 11|          |44
-->+I9      Y9+===
 12|          |45
-->+I10    Y10+===
 13|          |46
-->+I11    Y11+===
 14|          |47
-->+I12    Y12+===
 15|          |48
-->+I13    Y13+===
 16|          |49
-->+I14    Y14+===
 17|          |50
-->+I15    Y15+===
 18|          |51
-->+I16    Y16+===
 19|          |52
-->+I17    Y17+===
 20|          |53
-->+I18    Y18+===
 21|          |54
-->+I19    Y19+===
 22|          |55
-->+I20    Y20+===
 23|          |56
-->+I21    Y21+===
 24|          |57
-->+I22    Y22+===
 25|          |58
-->+I23    Y23+===
 26|          |59
-->+I24    Y24+===
 27|          |60
-->+I25    Y25+===
 28|          |61
-->+I26    Y26+===
 29|          |62
-->+I27    Y27+===
 30|          |63
-->+I28    Y28+===
 31|          |64
-->+I29    Y29+===
 32|          |65
-->+I30    Y30+===
 33|          |66
-->+I31    Y31+===
   |   xnn    |
   | _        |
   +----------+
'''

if __name__ == "__main__":
    XBUF32().main()
