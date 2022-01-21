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
    def __init__(self, name, *vals):
        self.name = name
        self.recursive = False
        if len(vals) == 1 and vals[0] is None:
            self.members = None
        else:
            self.members = []
            for i in vals:
                self += i

    def __str__(self):
        if self.members is None:
             return self.name
        return "(" + self.name + " <%d>)" % len(self.members)

    def __iadd__(self, child):
        assert isinstance(child, SExp)
        self.members.append(child)
        self.recursive |= child.members is not None
        return self

    def __isub__(self, child):
        self.members.remove(child)
        return self

    def __len__(self):
        return len(self.members)

    def __getitem__(self, idx):
        return self.members[idx]

    def pop(self, idx):
        ''' pop a member '''
        return self.members.pop(idx)

    def __iter__(self):
        yield from self.members

    def parse(self, src):
        ''' Parse sexp string '''
        begin = 0

        while src[begin] in " \t\n":
            begin += 1

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
            self.name = src[begin:end]
            self.members = None
            return end

        if src[begin] != '(':
            end = begin
            while src[end] not in " \t\n)":
                end += 1
            self.name = src[begin:end]
            self.members = None
            return end

        begin += 1
        end = begin
        while src[end] not in " \t\n)":
            end += 1
        self.name = src[begin:end]
        while True:
            while src[end] in " \t\n":
                end += 1
            if src[end] == ')':
                break
            sexp = SExp(None)
            end += sexp.parse(src[end:])
            self += sexp
        return end + 1

    def serialize(self, indent="  "):
        ''' Serialize recursively '''
        if self.members is None:
            yield self.name
        elif self.recursive:
            yield '(' + self.name
            for i in self.members:
                for j in i.serialize(indent):
                    yield indent + j
            yield ')'
        elif len(self.members) == 0:
            yield '(' + self.name + ')'
        else:
            i = ' '.join(x.name for x in self.members)
            yield '(' + self.name + ' ' + i + ')'

def sortkey(s):
    if s.name == "sheet":
        for i in s:
            if i.name == "property":
                if i[0].name == '"Sheet file"':
                    return s.name + " " + i[1].name
    for i in s:
        if i.name == "uuid":
            s -= i
            break
    for i in s:
        if i.name == "stroke":
            if " ".join(i.serialize('')) == "(stroke (width 0) (type default) (color 0 0 0 0) )":
                s -= i
                break
    low_x = 9e9
    low_y = 9e9
    coord = False
    for i in s:
        if i.name == "diameter":
            if i[0].name != "0":
                i[0].name = "0"
        if i.name in (
            "at",
            "xy",
        ):
            low_x = min(low_x, float(i[0].name))
            low_y = min(low_y, float(i[1].name))
            coord = True
    if coord:
        t = "* %8.2f" % low_x + "%8.2f " % low_y + s.name
        return t

    return ' '.join(s.serialize())

def polish_kicad_sch(fn):
    print(fn)
    sexp = SExp(None)
    sexp.parse(open(fn).read())

    m = sexp.members[4:]
    sexp.members = sexp.members[:4]

    for j in (
        "title_block",
        "lib_symbols",
    ):
        for i in m:
            if i.name == j:
                i.members = list(sorted(i.members, key=sortkey))
                sexp += i

    for i in sorted(m, key=sortkey):
        if i.name not in (
            "lib_symbols",
            "title_block",
            "sheet_instances",
            "symbol_instances",
        ):
            sexp += i
    last = None
    if False:
        for n, i in enumerate(sexp):
            if i.name != last:
                print("   ", n, i)
                last = i.name
    with open(fn, "w") as file:
        file.write('(' + sexp.name + '\n')
        for i in sexp:
            if i.name in (
                "lib_symbols",
            ):
                file.write('  (' + i.name + '\n')
                for j in i:
                    file.write('    ' + ' '.join(j.serialize("")) + '\n')
                file.write('  )\n')
            else:
                file.write('  ' + ' '.join(i.serialize("")) + '\n')
        file.write(')\n')

def main():
    ''' ... '''

    import glob

    for fn in sorted(glob.glob("/home/phk/Proj/R1000.HwDoc/Schematics/*/*.kicad_sch")):
        polish_kicad_sch(fn)
    for fn in sorted(glob.glob("/tmp/F/R1000.HwDoc/Schematics/*/*.kicad_sch")):
        polish_kicad_sch(fn)

if __name__ == "__main__":
    main()
