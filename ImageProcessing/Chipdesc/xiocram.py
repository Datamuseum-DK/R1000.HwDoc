#!/usr/bin/env python3

''' 32Kx8x4 SRAM '''

from Chipdesc.chip import Chip

class XIOCRAM(Chip):

    ''' 32Kx8x4 SRAM '''

    symbol_name = "XIOCRAM"

    symbol = '''
   +----------+
  1|          |17
-->+A0     CS0o<--
  2|          |18
-->+A1     CS1o<--
  3|          |  
-->+A2        |   
  4|          |19
-->+A3     WE0o<--
  5|          |20
-->+A4     WE1o<--
  6|          |21
-->+A5     WE2o<--
  7|          |22
-->+A6     WE3o<--
  8|          |
-->+A7        |
  9|          |
-->+A8        |
 10|          |
-->+A9        |
 11|          |
-->+A10       |
 12|          |
-->+A11       |
 13|          |
-->+A12       |
 14|          |
-->+A13       |
 15|          |
-->+A14       |
 16|          |
-->+A15       |
   |          |
   |          |
 23|          |59
-->+D00    Q00+-->
 24|          |60
-->+D01    Q01+-->
 25|          |61
-->+D02    Q02+-->
 26|          |62
-->+D03    Q03+-->
 27|          |63
-->+D04    Q04+-->
 28|          |64
-->+D05    Q05+-->
 29|          |65
-->+D06    Q06+-->
 30|          |66
-->+D07    Q07+-->
 31|          |67
-->+D08    Q08+-->
   |          |
   |          |
 27|          |63
-->+D10    Q10+-->
 28|          |64
-->+D11    Q11+-->
 29|          |65
-->+D12    Q12+-->
 30|          |66
-->+D13    Q13+-->
 31|          |67
-->+D14    Q14+-->
 32|          |68
-->+D15    Q15+-->
 33|          |69
-->+D16    Q16+-->
 34|          |70
-->+D17    Q17+-->
 35|          |71
-->+D18    Q18+-->
   |          |
   |          |
 31|          |67
-->+D20    Q20+-->
 32|          |68
-->+D21    Q21+-->
 33|          |69
-->+D22    Q22+-->
 34|          |70
-->+D23    Q23+-->
 35|          |71
-->+D24    Q24+-->
 36|          |72
-->+D25    Q25+-->
 37|          |73
-->+D26    Q26+-->
 38|          |74
-->+D27    Q27+-->
 39|          |75
-->+D28    Q28+-->
   |          |
   |          |
 35|          |71
-->+D30    Q30+-->
 36|          |72
-->+D31    Q31+-->
 37|          |73
-->+D32    Q32+-->
 38|          |74
-->+D33    Q33+-->
 39|          |75
-->+D34    Q34+-->
 40|          |76
-->+D35    Q35+-->
 41|          |77
-->+D36    Q36+-->
 42|          |78
-->+D37    Q37+-->
 43|   xnn    |79
-->+D38    Q38+-->
   |          |
   | _        |
   +----------+
'''

if __name__ == "__main__":
    XIOCRAM().main()
