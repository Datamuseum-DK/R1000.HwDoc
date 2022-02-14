#!/usr/bin/env python3

''' 16 bit version of 74x169 - Synchronous 4-Bit Bidirectional Counters '''

from Chipdesc.chip import Chip

class XCTR16(Chip):

    ''' 16 bit version of 74x169 - Synchronous 4-Bit Bidirectional Counters '''

    symbol_name = "XCTR16"

    checked = "TYP 0018"

    symbol = '''
      |  |  |
      |  |  |
    33v34v35v
   +--+--o--+--+
   |  v        |
   | CLK LD UP |
   |           | 
 36|           |38
-->oENP    CO15o-->
 37|           |39
-->oENT    CO11o-->
   |           |
  1|           |17
-->+D0       Q0+-->
  2|           |18
-->+D1       Q1+-->
  3|           |19
-->+D2       Q2+-->
  4|           |20
-->+D3       Q3+-->
  5|           |21
-->+D4       Q4+-->
  6|           |22
-->+D5       Q5+-->
  7|           |23
-->+D6       Q6+-->
  8|           |24
-->+D7       Q7+-->
  9|           |25
-->+D8       Q8+-->
 10|           |26
-->+D9       Q9+-->
 11|           |27
-->+D10     Q10+-->
 12|           |28
-->+D11     Q11+-->
 13|           |29
-->+D12     Q12+-->
 14|           |30
-->+D13     Q13+-->
 15|           |31
-->+D14     Q14+-->
 16|    xnn    |32
-->+D15     Q15+-->
   |           |
   |   _       |
   +-----------+
'''

if __name__ == "__main__":
    XCTR16().main()
