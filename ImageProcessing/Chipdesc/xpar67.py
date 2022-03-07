#!/usr/bin/env python3

''' 67 bit address parity generator '''

from Chipdesc.chip import Chip

class XPAR67(Chip):

    ''' 67 bit address parity generator '''

    symbol_name = "XPAR67"

    symbol = '''
   +-----------+
  2|           |70
-->+S0     PEV0+-->
  3|           |71
-->+S1     PEV1+-->
  4|           |72
-->+S2     PEV2+-->
  5|           |73
-->+N0     PEV3+-->
  6|           |74
-->+N1     PEV4+-->
  7|           |75
-->+N2     PEV5+-->
  8|           |76
-->+N3     PEV6+-->
  9|           |77
-->+N4     PEV7+-->
 10|           |78
-->+N5     PEV8+-->
 11|           |
-->+N6         |79
 12|       POD0+-->
-->+N7         |80
 13|       POD1+-->
-->+N8         |81
 14|       POD2+-->
-->+N9         |82
 15|       POD3+-->
-->+N10        |83
 16|       POD4+-->
-->+N11        |84
 17|       POD5+-->
-->+N12        |85
 18|       POD6+-->
-->+N13        |86
 19|       POD7+-->
-->+N14        |87
 20|       POD8+-->
-->+N15        |
 21|           |
-->+N16        |
 22|           |
-->+N17        |
 23|           |
-->+N18        |
 24|           |
-->+N19        |
 25|           |
-->+N20        |
 26|           |
-->+N21        |
 27|           |
-->+N22        |
 28|           |
-->+N23        |
 29|           |
-->+N24        |
 30|           |
-->+N25        |
 31|           |
-->+N26        |
 32|           |
-->+N27        |
 33|           |
-->+N28        |
 34|           |
-->+N29        |
 35|           |
-->+N30        |
 36|           |
-->+N31        |
 37|           |
-->+O0         |
 38|           |
-->+O1         |
 39|           |
-->+O2         |
 40|           |
-->+O3         |
 41|           |
-->+O4         |
 42|           |
-->+O5         |
 43|           |
-->+O6         |
 44|           |
-->+O7         |
 45|           |
-->+O8         |
 46|           |
-->+O9         |
 47|           |
-->+O10        |
 48|           |
-->+O11        |
 49|           |
-->+O12        |
 50|           |
-->+O13        |
 51|           |
-->+O14        |
 52|           |
-->+O15        |
 53|           |
-->+O16        |
 54|           |
-->+O17        |
 55|           |
-->+O18        |
 56|           |
-->+O19        |
 57|           |
-->+O20        |
 58|           |
-->+O21        |
 59|           |
-->+O22        |
 60|           |
-->+O23        |
 61|           |
-->+O24        |
 62|           |
-->+B0         |
 63|           |
-->+B1         |
 64|           |
-->+B2         |
 65|           |
-->+B3         |
 66|           |
-->+B4         |
 67|           |
-->+B5         |
 68|    xnn    |
-->+B6         |
   |           |
   | _         |
   +-----------+
'''

if __name__ == "__main__":
    XPAR67().main()
