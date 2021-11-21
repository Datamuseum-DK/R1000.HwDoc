#!/usr/bin/env python3
#
# Copyright (c) 2021 Poul-Henning Kamp
# All rights reserved.
#
# Author: Poul-Henning Kamp <phk@phk.freebsd.dk>
#
# SPDX-License-Identifier: BSD-2-Clause
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

''' Python wrapper for FRONTPLANE.TXT '''

import os
import re

class R1000FrontPlane():

    ''' Python wrapper around FRONTPLANE.txt '''
    def __init__(self):
        self.bypin = {}
        self.byname = {}
        self.connected = ["-------"] * 301
        self.mem2 = [None] * 301
        self.mem0 = [None] * 301
        self.fiu = [None] * 301
        self.seq = [None] * 301
        self.typ = [None] * 301
        self.val = [None] * 301
        self.ioc = [None] * 301
        self.mem32 = self.mem0
        self.boards = [
            self.mem2,
            self.mem0,
            self.fiu,
            self.seq,
            self.typ,
            self.val,
            self.ioc,
        ]
        npin = 1
        for line in open(
            os.path.join(
                os.path.dirname(__file__),
                "FRONTPLANE.txt"
            )
        ):
            fields = line.split()
            if not fields or fields[0][0] == "#":
                continue

            if len(fields[0]) == 3 and len(fields[1]) == 3:
                if len(fields) == 3:
                    assert npin + 1 == int(fields[2])
                for name in fields[:2]:
                    self.bypin[npin] = name
                    if name not in ("GND",):
                        assert name not in self.byname
                        self.byname[name] = npin
                    npin += 1
            else:
                assert len(fields[0]) == 3
                assert len(fields[1]) == 7
                regex = re.compile(
                    fields[0].replace('#', '[0-9]')
                )
                for pin, name in self.bypin.items():
                    if not regex.match(name):
                        continue
                    self.connected[pin] = fields[1]
                    for board, conn in zip(self.boards, fields[1]):
                        if conn == '+':
                            board[pin] = name
                        else:
                            assert conn == '-'

    def __getitem__(self, pin):
        return self.bypin.get(pin)

def main():
    ''' Function test '''
    fplane = R1000FrontPlane()
    print(fplane.bypin[32])
    print(fplane.byname["V23"])
    print(fplane.ioc[32])
    print(fplane[32])

if __name__ == "__main__":
    main()
