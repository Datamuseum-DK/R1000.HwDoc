#!/usr/bin/env python3

''' Intel 8051 - 8 Bit Control Oriented Microcomputers '''

from Chipdesc.chip import Chip

class I8051(Chip):

    ''' Intel 8051 - 8 Bit Control Oriented Microcomputers '''

    symbol_name = "8051"

    checked = "VAL 0069"

    symbol = '''
      |      |
      |      |
    19v     9v
   +--+------+----+
   |  v           |
   | XTAL1  RST   |32
   |            C0+===
   |              |33
   |            C1+===
 18|              |34
-->+XTAL2       C2+===
   |              |35
   |            C3+===
 31|        0     |36
-->+EA~         C4+===
   |              |37
   |            C5+===
 29|              |38
<--+PSEN~       C6+===
   |              |39
   |            C7+===
 30|              |
<--+ALE           |
   |              |8
   |            D0+===
 10|              |7
-->+RXD         D1+===
   |              |6
   |            D2+===
 11|              |5
<--+TXD         D3+===
   |        1     |4
   |            D4+===
 12|              |3
===+INT0~       D5+===
   |              |2
   |            D6+===
 13|              |1
-->+INT1~       D7+===
   |        ---   |28
   |            D8+===
 14|              |27
<->+T0          D9+===
   |              |26
   |           D10+===
 15|              |25
-->+T1         D11+===
   |        2     |24
   |           D12+===
 16|              |23
<--+WR~        D13+===
   |              |22
   |           D14+===
 17|     xnn      |21
<->+RD~        D15+===
   |     _        |
   |              |
   +--------------+
'''

if __name__ == "__main__":
    I8051(__file__).main()
