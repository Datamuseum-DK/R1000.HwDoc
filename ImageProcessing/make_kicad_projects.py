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
Build per-board KiCad projects
'''

import os
import shutil
import glob
import json
import random

import schematics as sch

import page_numbers

from sexp import SExp

MAGIC = "20011966"

def mkuuid():
    s = MAGIC
    s += "-%04x" % random.randint(0, 1<<16 - 1)
    s += "-%04x" % random.randint(0, 1<<16 - 1)
    s += "-%04x" % random.randint(0, 1<<16 - 1)
    s += "-%012x" % random.randint(0, 1<<48 - 1)
    return s

def paper():
    return SExp("paper", '"User"', '%.2f' % (sch.INCH_WIDTH * 25.4), '%.2f' % (sch.INCH_HEIGHT * 25.4))

class Page():
    def __init__(self, name, page):
        self.name = name
        self.page = page
        self.uuid = mkuuid()
        self.fname = "pg_%02d" % self.page + ".kicad_sch"

    def __lt__(self, other):
        return self.page < other.page

    def mk_sch(self, ddir):

        sch = SExp("kicad_sch")
        sch += SExp("version", "20210807")
        sch += SExp("generator", "PHK115")
        sch += SExp("uuid", self.uuid)
        sch += paper()

        title = SExp("title_block")
        sch += title
        title += SExp("title", '"' + self.name + ' ' + str(self.page) + '"')
        if self.name == "FIU":
            title += SExp("date", '"20-MAR-90"')
            title += SExp("comment", "1", '"FIU"')
            title += SExp("comment", "2", '"232-003065"')
            title += SExp("comment", "3", '"S400"')
            title += SExp("comment", "4", '"RELEASED"')
            title += SExp("rev", "1.0")
        elif self.name == "IOC":
            title += SExp("date", '"22-SEP-90"')
            title += SExp("comment", "1", '"IOC"')
            title += SExp("comment", "2", '"232-003061"')
            title += SExp("comment", "3", '"S400"')
            title += SExp("comment", "4", '"RELEASED"')
            title += SExp("rev", "2.0")
        elif self.name == "MEM32":
            title += SExp("date", '"08-MAR-90"')
            title += SExp("comment", "1", '"MEM32 BOARD"')
            title += SExp("comment", "2", '"232-003066"')
            title += SExp("comment", "3", '"S400"')
            title += SExp("comment", "4", '"RELEASED"')
            title += SExp("rev", "0.0")
        elif self.name == "RESHA":
            title += SExp("date", '"90XXXX"')
            title += SExp("comment", "1", '"RESHA"')
            title += SExp("comment", "2", '"GJS"')
            title += SExp("comment", "3", '"R1000 - M400"')
            title += SExp("comment", "4", '"IN DESIGN"')
            title += SExp("rev", "1.0")
        elif self.name == "SEQ":
            title += SExp("date", '"22-MAY-90"')
            title += SExp("comment", "1", '"SEQUENCER"')
            title += SExp("comment", "2", '"232-003064"')
            title += SExp("comment", "3", '"S400"')
            title += SExp("comment", "4", '"RELEASED"')
            title += SExp("rev", "1.0")
        elif self.name == "TYP":
            title += SExp("date", '"15-MAR-90"')
            title += SExp("comment", "1", '"TYPE"')
            title += SExp("comment", "2", '"232-003062"')
            title += SExp("comment", "3", '"S400"')
            title += SExp("comment", "4", '"RELEASED"')
            title += SExp("rev", "1.0")
        elif self.name == "VAL":
            title += SExp("date", '"22-MAR-90"')
            title += SExp("comment", "1", '"VALUE"')
            title += SExp("comment", "2", '"232-003063"')
            title += SExp("comment", "3", '"S400"')
            title += SExp("comment", "4", '"RELEASED"')
            title += SExp("rev", "1.0")

        sch += SExp("lib_symbols")

        with open(ddir + self.fname, "w") as file:
            for i in sch.serialize():
                file.write(i + "\n")


class project():
    def __init__(self, dir):
        self.name = os.path.basename(dir)
        self.name = self.name.replace("_pgm", "")
        print(self.name)
        self.uuid = mkuuid()

        self.pages = []

        for fn in sorted(glob.glob(dir + "/*.pgm")):
             sheet = os.path.basename(fn)[2:-4]
             page = page_numbers.page_number(self.name, sheet)
             self.pages.append(Page(self.name, page))

        self.ddir = "Proj/" + self.name + "/"
        try:
            os.mkdir(self.ddir)
        except FileExistsError:
            pass

        shutil.copy("KiCadFiles/R1000.kicad_sym", self.ddir)
        shutil.copy("KiCadFiles/R1000.kicad_wks", self.ddir)

        with open(self.ddir + self.name + ".kicad_pcb", "w") as file:
            file.write('''(kicad_pcb (version 4) (host kicad "dummy file") )\n''')

        with open(self.ddir + "sym-lib-table", "w") as file:
            file.write('''(sym_lib_table (lib (name "r1000")(type "KiCad")(uri "${KIPRJMOD}/R1000.kicad_sym")(options "")(descr "")))''')

        proj = {
            "meta": {
                "filename": self.name + ".kicad_pro",
                "version": 1,
            },
            "schematic": {
                "drawing": {
                    "default_text_size": 100.0,
                    "intersheets_ref_own_page": True,
                    "intersheets_ref_prefix": "{",
                    "intersheets_ref_short": True,
                    "intersheets_ref_show": True,
                    "intersheets_ref_suffix": "}",
                },
                "page_layout_descr_file": "R1000.kicad_wks",
            },
            "sheets": [ ]
        }
        proj["sheets"].append([self.uuid, ""])
        for i in self.pages:
            proj["sheets"].append([i.uuid, i.fname])
        with open(self.ddir + self.name + ".kicad_pro", "w") as file:
            file.write(json.dumps(proj, sort_keys=True, indent=2))

        self.mk_sch()

    def mk_sch(self):

        sch = SExp("kicad_sch")
        sch += SExp("version", "20210807")
        sch += SExp("generator", "PHK115")
        sch += SExp("uuid", self.uuid)
        sch += paper()

        title = SExp("title_block")
        sch += title
        title += SExp("title", '"' + self.name + ' Main"')

        sch += SExp("lib_symbols")

        y_off = 0
        for pg in sorted(self.pages):
            pg.mk_sch(self.ddir)
            subsch = SExp("sheet")
            sch += subsch
            page = pg.page
            ix = page % 10
            iy = page // 10 - y_off
            cx = 12.7 + 25.4 * ix
            cy = 12.7 + 35.56 * iy
            subsch += SExp("at", "%.2f" % cx, "%.2f" % cy)
            subsch += SExp("size", "20.32", "20.32")
            subsch += SExp("fields_autoplaced")
            subsch += SExp("uuid", pg.uuid)

            prop = SExp("property")
            subsch += prop
            prop += '"Sheet name"'
            prop += '"' + "Page %d" % pg.page + '"'
            prop += SExp("id", "0")
            prop += SExp("at", "%.2f" % cx, "%.2f" % (cy - 1), "0")

            effects = SExp("effects")
            prop += effects
            effects += SExp("justify", "left", "bottom")

            font = SExp("font")
            effects += font
            font += SExp("size", "2.54", "2.54")

     
            prop = SExp("property")
            subsch += prop
            prop += '"Sheet file"'
            prop += '"' + pg.fname  + '"'
            prop += SExp("id", "1")
            prop += SExp("at", "%.2f" % cx, "%.2f" % (cy + 20.32 + 1), "0")
            effects = SExp("effects")
            prop += effects

            font = SExp("font")
            effects += font
            font += SExp("size", "1.27", "1.27")

            effects += SExp("justify", "left", "top")

        instances = SExp("sheet_instances")
        sch += instances

        path = SExp("path", '"/"')
        path += SExp("page", '"0"')
        instances += path

        for pg in sorted(self.pages):
            path = SExp("path", '"/' + pg.uuid + '"')
            path += SExp("page", '"%d"' % pg.page)
            instances += path

        with open(self.ddir + self.name + ".kicad_sch", "w") as file:
             for i in sch.serialize():
                 file.write(i + "\n")

def main():
    try:
        os.mkdir("Proj")
    except FileExistsError:
        pass
    for dir in glob.glob("*pgm"):
        project(dir)

if __name__ == "__main__":
    main()

