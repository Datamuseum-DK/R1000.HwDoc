#!/usr/bin/env python3

''' STK RAM 16x16 '''

from Chipdesc.chip import Chip

class XSTKRAM(Chip):

    ''' STK RAM 16x16 '''

    symbol_name = "XSTKRAM"

    symbol = '''
      |   |
      |   |
    33v 34v
   +--o---o--+
   | WE   CS |
  1|         |17
-->+D0     Q0o===
  2|         |18
-->+D1     Q1o===
  3|         |19
-->+D2     Q2o===
  4|         |20
-->+D3     Q3o===
  5|         |21
-->+D4     Q4o===
  6|         |22
-->+D5     Q5o===
  7|         |23
-->+D6     Q6o===
  8|         |24
-->+D7     Q7o===
  9|         |25
-->+D8     Q8o===
 10|         |26
-->+D9     Q9o===
 11|         |27
-->+D10   Q10o===
 12|         |28
-->+D11   Q11o===
 13|         |29
-->+D12   Q12o===
 14|         |30
-->+D13   Q13o===
 15|         |31
-->+D14   Q14o===
 16|         |32
-->+D15   Q15o===
   |         |
 35|         |
-->+A0       |
 36|         |
-->+A1       |
 37|         |
-->+A2       |
 38|         |
-->+A3       |
   |         |
   |  xnn    |
   |         |
   |  _      |
   +---------+
'''

if __name__ == "__main__":
    XSTKRAM(__file__).main()
