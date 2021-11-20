#!/usr/local/bin/python3.8
#
# NB: We strive to use y-x coordinate order to match numpy's convention


''' ... '''

import sys
import os

import numpy as np

import schematics as sch

from debug_snippets import DebugSnippets

import templates

PATT2 = '''
-------------------------------
-------------------------------
-------------------------------
-------------------------------
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
----#######################----
-------------------------------
-------------------------------
-------------------------------
-------------------------------
'''

if __name__ == "__main__":
    sheet = sch.Sheet(sys.argv)
    sheet.load_raw_image()

    dbg = DebugSnippets()
    w_tl, w_br = sch.window((200,200), (26,26))
    j = sch.snippet(sheet.img, w_tl, w_br)

    fo = open("/tmp/__", "w")

    for _lim, patt in (
        (55, PATT2),
    ):
        template = templates.string_2_template(patt)
        print(template.shape, np.sum(template), template.size, np.sum(template) / template.size)

        tm = templates.TemplateMatcher(template=template)
        idle = 0
        for n, i in enumerate(tm.match(sheet.img, threshold=-30000)):
            if not (n % 64):
                dbg.newline()
            inch = sheet.pix2inch(i.pix)
            if -9999 in inch:
                continue
            y = inch[0] - round(inch[0], 1)
            x = inch[1] - round(inch[1], 1)
            w_tl, w_br = sch.window(i.pix, (31,31))
            j = sch.snippet(sheet.img, w_tl, w_br)
            dbg.add(j)
            fo.write("%7.3f %7.3f" % inch + " %7.3f" % i.merit + " %4d %4d" % i.pix + " %6.3f" % y + " %6.3f" % x + "\n")
            print(
                i.merit,
                "%7.3f %7.3f" % inch,
                "%7.3f %7.3f" % (y, x),
                i
            )
            if n >= 48*64:
                break
        print("UNMERIT", tm.first_unmerit)

    dbg.dump(sheet.fn_pfx + "debug.png")
    # sheet.write_landmarks()
    # sheet.write_interpolators()
    # sheet.write_interpolated()
