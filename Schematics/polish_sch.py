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

import os
import glob
import sys
import subprocess

sys.path.append("../ImageProcessing")

from sexp import SExp

BRANCH = subprocess.check_output(["git", "branch"])
BRANCH = BRANCH.split(b'\n', maxsplit=1)[0].decode("utf-8")
BRANCH = BRANCH.split()[-1]

def delete_matching(sexp, name, text):
    ''' delete leave `name` if it matches the `text` '''
    for i in sexp:
        if i.name == name:
            if " ".join(i.serialize('')) == text:
                sexp -= i
                return

def delete_defaults(sexp):
    ''' delete certain default value leaves '''
    delete_matching(
        sexp,
        "stroke",
        "(stroke (width 0) (type default) (color 0 0 0 0) )",
    )
    delete_matching(
        sexp,
        "fill",
        "(fill (color 0 0 0 0.0000) )",
    )

class KiCadSheet():
    ''' A Kicad `.kicad_sch` file '''
    def __init__(self, filename):
        self.fullname = filename
        self.filename = filename.split("/")[-1]
        self.sexp = SExp(None)
        self.sexp.parse(open(filename).read())
        self.title = self.sexp.find_first("title_block.title")[0].name
        self.title = self.title.replace("\\\\n", "\n")
        self.title = self.title.replace('"', '')
        self.uuid = self.sexp.find_first("uuid")[0].name
        print("R", self.filename, [self.uuid], [self.title])
        self.sort_lib_symbols()

    def delete(self, name):
        ''' delete all leaves named `name` '''
        for i in list(self.sexp.find(name)):
            self.sexp -= i

    def sort_lib_symbols(self):
        ''' Sort the symbols in lib_symbols '''
        i = self.sexp.find_first("lib_symbols")
        if i is not None:
            i.members = list(sorted(i.members, key=lambda x: x[0].name))

    def write(self):
        ''' Write back to file (atomically) '''
        with open(self.fullname + "_", "w") as file:
            file.write('(' + self.sexp.name + '\n')
            for i in self.sexp:
                if i.name not in (
                    "lib_symbols",
                    "sheet_instances",
                ):
                    file.write('  ' + ' '.join(i.serialize("")) + '\n')
                else:
                    file.write('  (' + i.name + '\n')
                    for j in i:
                        file.write('    ' + ' '.join(j.serialize("")) + '\n')
                    file.write('  )\n')
            file.write(')\n')
        os.rename(self.fullname + "_", self.fullname)

class Element():
    ''' A schematic element, used for sorting them '''
    def __init__(self, sexp):
        self.sexp = sexp
        self.create_sort_key()

    def create_sort_key(self):
        low_x = 9e9
        low_y = 9e9
        coord = False
        siz = None
        for i in self.sexp:
            if i.name == "size":
                siz = "|".join(i.serialize(""))
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
            self.key = "* %8.2f" % low_x + "%8.2f " % low_y + self.sexp.name
        else:
            self.key = "|".join(self.sexp.serialize(""))
        if siz:
            self.key += "|" + siz

    def __lt__(self, other):
        return self.key < other.key

class Board():
    ''' A Kicad project directory '''
    def __init__(self, directory):
        self.dir = directory
        self.name = self.dir.split("/")[-1]

        self.read_files()

        self.fix_top_sheet()
        for i in self.pages.values():
            self.fix_page_sheet(i.sexp)

        self.top.write()
        for i in self.pages.values():
            i.write()

    def read_files(self):
        ''' Read the `.kicad_sch` files '''
        self.top = KiCadSheet(self.dir + "/" + self.name + ".kicad_sch")
        # polish_kicad_sch(self.dir + "/" + self.name + ".kicad_sch")
        self.pages = {}
        for filename in sorted(glob.glob(self.dir + "/pg_??.kicad_sch")):
            pgno = int(filename.split("/")[-1].split(".")[0][3:], 10)
            sexp = KiCadSheet(filename)
            self.pages[pgno] = sexp

    def fix_top_sheet(self):
        ''' ... '''
        self.top.delete("symbol_instances")
        self.top.delete("sheet_instances")
        self.top.delete("text")
        self.top.sexp += SExp(
            "text",
            '"Board: %s Branch: %s"' % (self.name, BRANCH),
            SExp("at", "7.62", "370.84", "0"),
            SExp(
                 "effects",
                 SExp("font",
                     SExp("size", "7.62", "7.62"),
                     SExp("thickness", "1.27"),
                     "bold",
                 ),
                 SExp("justify", "left", "bottom"),
            ),
        )
        sheet_instances = SExp("sheet_instances")
        top_instance = SExp(
            "path",
            '"/"',
            SExp("page", '"00"')
        )
        sheet_instances += top_instance
        for pgno, page in sorted(self.pages.items()):
            page_instance = SExp(
                "path",
                '"/' + page.uuid + '"',
                SExp(
                    "page",
                    '"%02d"' % pgno,
                )
            )
            sheet_instances += page_instance
        self.top.sexp += sheet_instances

        self.top.delete("sheet")
        coor_y0 = coor_y = 12.7
        coor_x = 12.7
        for pgno, page in sorted(self.pages.items()):
            title = page.title.replace("\n", " - ")
            title = title.replace("  ", " ")
            title = title.replace("  ", " ")
            siz = len(page.sexp)
            if siz < 10:
                title += " <%d>" % siz
            sheet = SExp(
                "sheet",
                SExp("at", "%.2f" % coor_x, "%.2f" % coor_y),
                SExp("size", "20.32", "5.08"),
                SExp("uuid", page.uuid),
                SExp(
                    "property",
                    '"Sheet name"',
                    '"Page %02d"' % pgno,
                    SExp("id", "0"),
                    SExp("at", "%.2f" % (coor_x + 22.86), "%.2f" % (coor_y + 5.08), "0"),
                    SExp(
                         "effects",
                         SExp("font", SExp("size", "2.54", "2.54")),
                         SExp("justify", "left", "bottom"),
                    ),
                ),
                SExp(
                    "property",
                    '"Sheet file"',
                    '"%s"' % page.filename,
                    SExp("id", "1"),
                    SExp("at", "%.2f" % (coor_x + 22.86), "%.2f" % (coor_y + 2.54), "0"),
                    SExp(
                         "effects",
                         SExp("justify", "left", "bottom"),
                         "hide",
                    ),
                )
            )
            if siz < 20:
                sheet += SExp("fill", SExp("color", "192", "192", "192", "1.0"))
            self.top.sexp += sheet
            self.top.sexp += SExp(
                "text",
                '"%s"' % title,
                SExp("at", "%.2f" % (coor_x + 40.64), "%.2f" % (coor_y + 5.08), "0"),
                SExp(
                     "effects",
                     SExp("font", SExp("size", "2.54", "2.54")),
                     SExp("justify", "left", "bottom"),
                ),
            )
            coor_y += 3 * 2.54
            if coor_y > 355:
                coor_y = coor_y0
                coor_x += 10 * 25.4

    def fix_page_sheet(self, sexp):
        ''' ... '''
        elems = []
        tmp = sexp.members
        sexp.members = []
        for i in tmp:
            delete_defaults(i)
            for j in list(i.find("pin")):
                for k in list(j.find("uuid")):
                    j -= k
            for j in list(i.find("uuid")):
                i -= j
            if i.name in (
                "version",
                "generator",
                "uuid",
                "paper",
                "title_block",
                "lib_symbols",
            ):
                sexp += i
            else:
                elems.append(Element(i))
        for i in sorted(elems):
            sexp += i.sexp

def main():
    ''' ... '''

    if len(sys.argv) > 1:
        for i in sys.argv[1:]:
            Board(i)
    else:
        for i in ("FIU", "IOC", "MEM32", "SEQ", "TYP", "VAL"):
            Board(i)

if __name__ == "__main__":
    main()
