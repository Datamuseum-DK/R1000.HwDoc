#!/usr/bin/env python3

''' 74x138 - 1-to-8 Decoder-Demultiplexer '''

# XXX: Incomplete

from Chipdesc.chip import Chip

class F154(Chip):

    ''' 74x154 - 1-to-16 decoder '''

    symbol_name = "F154"

    symbol = '''
   +--------+
   |        |%
  %|      Y0o===
-->oE1      |%
  %|      Y1o===
-->oE2      |%
   |      Y2o===
   |        |%
   |      Y3o===
   |xnn     |%
   |      Y4o===
  %|        |%
-->+S0    Y5o===
  %|        |%
-->+S1    Y6o===
  %|        |%
-->+S2    Y7o===
  %|        |%
-->+S3    Y8o===
   |        |%
   |      Y9o===
   |        |%
   |     Y10o===
   |        |%
   |     Y11o===
   |        |%
   |     Y12o===
   |        |%
   |     Y13o===
   |        |%
   |     Y14o===
   |        |%
   |     Y15o===
   |        |
   |        |
   | _      |
   +--------+
'''

if __name__ == "__main__":
    F154().main()
