#!/usr/bin/env python3

''' 64 bit '374-style register '''

from Chipdesc.chip import Chip

class XREG64(Chip):

    ''' 64 bit '374-style register '''

    symbol_name = "XREG64"

    symbol = '''
      |    |
      |    |
     1v   2v
   +--o----o--+
  3|  CLK  OE |67
-->+I0      Y0+===
  4|          |68
-->+I1      Y1+===
  5|          |69
-->+I2      Y2+===
  6|          |70
-->+I3      Y3+===
  7|          |71
-->+I4      Y4+===
  8|          |72
-->+I5      Y5+===
  9|          |73
-->+I6      Y6+===
 10|          |74
-->+I7      Y7+===
 11|          |75
-->+I8      Y8+===
 12|          |76
-->+I9      Y9+===
 13|          |77
-->+I10    Y10+===
 14|          |78
-->+I11    Y11+===
 15|          |79
-->+I12    Y12+===
 16|          |80
-->+I13    Y13+===
 17|          |81
-->+I14    Y14+===
 18|          |82
-->+I15    Y15+===
 19|          |83
-->+I16    Y16+===
 20|          |84
-->+I17    Y17+===
 21|          |85
-->+I18    Y18+===
 22|          |86
-->+I19    Y19+===
 23|          |87
-->+I20    Y20+===
 24|          |88
-->+I21    Y21+===
 25|          |89
-->+I22    Y22+===
 26|          |90
-->+I23    Y23+===
 27|          |91
-->+I24    Y24+===
 28|          |92
-->+I25    Y25+===
 29|          |93
-->+I26    Y26+===
 30|          |94
-->+I27    Y27+===
 31|          |95
-->+I28    Y28+===
 32|          |96
-->+I29    Y29+===
 33|          |97
-->+I30    Y30+===
 34|          |98
-->+I31    Y31+===
 35|          |99
-->+I32    Y32+===
 36|          |100
-->+I33    Y33+===
 37|          |101
-->+I34    Y34+===
 38|          |102
-->+I35    Y35+===
 39|          |103
-->+I36    Y36+===
 40|          |104
-->+I37    Y37+===
 41|          |105
-->+I38    Y38+===
 42|          |106
-->+I39    Y39+===
 43|          |107
-->+I40    Y40+===
 44|          |108
-->+I41    Y41+===
 45|          |109
-->+I42    Y42+===
 46|          |110
-->+I43    Y43+===
 47|          |111
-->+I44    Y44+===
 48|          |112
-->+I45    Y45+===
 49|          |113
-->+I46    Y46+===
 50|          |114
-->+I47    Y47+===
 51|          |115
-->+I48    Y48+===
 52|          |116
-->+I49    Y49+===
 53|          |117
-->+I50    Y50+===
 54|          |118
-->+I51    Y51+===
 55|          |119
-->+I52    Y52+===
 56|          |120
-->+I53    Y53+===
 57|          |121
-->+I54    Y54+===
 58|          |122
-->+I55    Y55+===
 59|          |123
-->+I56    Y56+===
 60|          |124
-->+I57    Y57+===
 61|          |125
-->+I58    Y58+===
 62|          |126
-->+I59    Y59+===
 63|          |127
-->+I60    Y60+===
 64|          |128
-->+I61    Y61+===
 65|   xnn    |129
-->+I62    Y62+===
 66|   _      |130
-->+I63    Y63+===
   +----------+
'''

if __name__ == "__main__":
    XREG64().main()