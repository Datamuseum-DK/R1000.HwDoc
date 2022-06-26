#!/usr/bin/env python3

''' 74x163 - Synchronous 4-Bit Binary Counters '''

from Chipdesc.chip import Chip

class F163(Chip):

    ''' 74x163 - Synchronous 4-Bit Binary Counters '''

    def __init__(self, name, width):

        self.symbol_name = name

        self.checked = "IOC 0064"

        self.symbol = '''
      |  |  |
      |  |  |
     %v %v %v
   +--+--o--o--+
   |  v        |
   | CLK LD CLR|
   |           |%
   |         CO+-->
'''
        for i in range(width):
            self.symbol += '  %|           |%\n'
            self.symbol += '-->+D%-2d     %3s+-->\n' % (i, "Q%d" % i)
        self.symbol += '''  %|           |
-->+ENP        |
  %|           |
-->+ENT xnn    |
   |           |
   |    _      |
   +-----------+
'''

        super().__init__()

if __name__ == "__main__":
    F163("F163", 4).main()
    F163("F163X3", 12).main()
