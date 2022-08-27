#!/usr/bin/env python3

''' 128 bit ECC generator '''

from Chipdesc.chip import Chip

class XECC64(Chip):

    ''' 128 bit ECC generator '''

    symbol_name = "XECC64"

    symbol = '''
      |     ^
      |     |
     1v    2|
   +--+-----+--+
  3|  I     O  |67
-->+T0       V0+<--
  4|           |68
-->+T1       V1+<--
  5|           |69
-->+T2       V2+<--
  6|           |70
-->+T3       V3+<--
  7|           |71
-->+T4       V4+<--
  8|           |72
-->+T5       V5+<--
  9|           |73
-->+T6       V6+<--
 10|           |74
-->+T7       V7+<--
 11|           |75
-->+T8       V8+<--
 12|           |76
-->+T9       V9+<--
 13|           |77
-->+T10     V10+<--
 14|           |78
-->+T11     V11+<--
 15|           |79
-->+T12     V12+<--
 16|           |80
-->+T13     V13+<--
 17|           |81
-->+T14     V14+<--
 18|           |82
-->+T15     V15+<--
 19|           |83
-->+T16     V16+<--
 20|           |84
-->+T17     V17+<--
 21|           |85
-->+T18     V18+<--
 22|           |86
-->+T19     V19+<--
 23|           |87
-->+T20     V20+<--
 24|           |88
-->+T21     V21+<--
 25|           |89
-->+T22     V22+<--
 26|           |90
-->+T23     V23+<--
 27|           |91
-->+T24     V24+<--
 28|           |92
-->+T25     V25+<--
 29|           |93
-->+T26     V26+<--
 30|           |94
-->+T27     V27+<--
 31|           |95
-->+T28     V28+<--
 32|           |96
-->+T29     V29+<--
 33|           |97
-->+T30     V30+<--
 34|           |98
-->+T31     V31+<--
 35|           |99
-->+T32     V32+<--
 36|           |100
-->+T33     V33+<--
 37|           |101
-->+T34     V34+<--
 38|           |102
-->+T35     V35+<--
 39|           |103
-->+T36     V36+<--
 40|           |104
-->+T37     V37+<--
 41|           |105
-->+T38     V38+<--
 42|           |106
-->+T39     V39+<--
 43|           |107
-->+T40     V40+<--
 44|           |108
-->+T41     V41+<--
 45|           |109
-->+T42     V42+<--
 46|           |110
-->+T43     V43+<--
 47|           |111
-->+T44     V44+<--
 48|           |112
-->+T45     V45+<--
 49|           |113
-->+T46     V46+<--
 50|           |114
-->+T47     V47+<--
 51|           |115
-->+T48     V48+<--
 52|           |116
-->+T49     V49+<--
 53|           |117
-->+T50     V50+<--
 54|           |118
-->+T51     V51+<--
 55|           |119
-->+T52     V52+<--
 56|           |120
-->+T53     V53+<--
 57|           |121
-->+T54     V54+<--
 58|           |122
-->+T55     V55+<--
 59|           |123
-->+T56     V56+<--
 60|           |124
-->+T57     V57+<--
 61|           |125
-->+T58     V58+<--
 62|           |126
-->+T59     V59+<--
 63|           |127
-->+T60     V60+<--
 64|           |128
-->+T61     V61+<--
 65|           |129
-->+T62     V62+<--
 66|    xnn    |130
-->+T63     V63+<--
   |           |
   | _         |
   +-----------+
'''

if __name__ == "__main__":
    XECC64().main()
