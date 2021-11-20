#!/usr/local/bin/python3
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

'''
S-Expressions
'''

class SExp():
    ''' Painfully primitive s-exp handling '''
    def __init__(self, name=None, *vals):
        self.name = name
        self.simple = True
        self.members = []
        for i in vals:
            self += i

    def __iadd__(self, child):
        if isinstance(child, SExp):
            self.simple = False
        self.members.append(child)
        return self

    def __len__(self):
        return len(self.members)

    def __getitem__(self, idx):
        return self.members[idx]

    def pop(self, idx):
        return self.members.pop(idx)

    def __iter__(self):
        yield from self.members

    def parse(self, src, pfx=""):
        ''' Parse sexp string '''
        begin = 0
        while src[begin] in " \t\n":
            begin += 1
        assert src[begin] == '('
        begin += 1
        end = begin
        while src[end] not in " \t\n)":
            end += 1
        self.name = src[begin:end]
        begin = end
        while True:
            while src[begin] in " \t\n":
                begin += 1
            if src[begin] == ')':
                return begin + 1
            if src[begin] == '(':
                sexp = SExp()
                self.members.append(sexp)
                self.simple = False
                begin += sexp.parse(src[begin:], pfx = pfx + "  ")
                continue
            if src[begin] == '"':
                end = begin + 1
                while True:
                    while src[end] not in '\\"':
                        end += 1
                    if src[end] == '"':
                        end += 1
                        break
                    assert src[end:end+2] in ('\\\\', '\\"', '\\n')
                    end += 2
            else:
                end = begin
                while src[end] not in " \t\n)":
                    end += 1
            self.members.append(src[begin:end])
            begin = end

    def serialize(self):
        ''' Serialize recursively '''
        if self.simple:
            yield '(' + " ".join([self.name] + self.members) + ')'
        else:
            yield '(' + self.name
            for i in self.members:
                if isinstance(i, SExp):
                    for j in i.serialize():
                        yield "  " + j
                else:
                    yield "  " + i
            yield ')'

def main():
    ''' ... '''
    sexp = SExp()
    sexp.parse(open("/critter/R1K/W/SEQ/SEQ_PROJ/SEQ_PROJ.kicad_sch").read())

    with open("/tmp/_8", "w") as file:
        for i in sexp.serialize():
            print(i)
            file.write(i + "\n")

if __name__ == "__main__":
    main()
