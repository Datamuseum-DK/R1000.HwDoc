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
STEP 130
========

Landmark half the arrows between the thick/thin borders

We only do half the arrows to avoid getting too thin triangulators
and pick the half without numbers for robustness.
'''

import sys

import schematics as sch

from debug_snippets import DebugSnippets

class VArrow():

    ''' Use arrow to locate Y, and lines to locate X '''

    def __init__(self, sheet, inch_x_thickline, inch_x_thinline, inch_y, nam):

        inch_x_arrow = .5 * (inch_x_thickline + inch_x_thinline)

        apix_y, apix_x = sheet.inch2pix((inch_y, inch_x_arrow))
        apix_y, apix_x, _snippet = sheet.dark_median(apix_y, apix_x, 40, 20)

        _lpix_y, lpix_x = sheet.inch2pix((inch_y, inch_x_thinline))
        _lpix_y, lpix_x, _snippet = sheet.dark_median(apix_y, lpix_x, 40, 12)

        sheet.add_landmark(apix_y, lpix_x, inch_y, inch_x_thinline, nam)

        _tpix_y, tpix_x = sheet.inch2pix((inch_y, inch_x_thickline))
        _tpix_y, tpix_x, _snippet = sheet.dark_median(apix_y, tpix_x, 40, 20)

        if tpix_x is not None:
            sheet.add_landmark(apix_y, tpix_x, inch_y, inch_x_thickline, nam)
        else:
            _tpix_y, tpix_x = sheet.inch2pix((inch_y, inch_x_thickline))

        self.snippet = sheet.img[
            apix_y - 20 : apix_y + 20,
            min(tpix_x, lpix_x) - 20 : max(tpix_x, lpix_x) + 20,
        ]

        print("VA", nam, (tpix_x - lpix_x) / (inch_x_thickline - inch_x_thinline))

class HArrow():

    ''' Use arrow to locate X, and lines to locate Y '''

    def __init__(self, sheet, inch_y_thickline, inch_y_thinline, inch_x, nam):

        self.snippet = None

        inch_y_arrow = .5 * (inch_y_thickline + inch_y_thinline)

        apix_y, apix_x = sheet.inch2pix((inch_y_arrow, inch_x))
        apix_y, apix_x, _snippet = sheet.dark_median(apix_y, apix_x, 20, 40)
        if apix_x is None:
            return

        lpix_y, _lpix_x = sheet.inch2pix((inch_y_thinline, inch_x))
        lpix_y, _lpix_x, _snippet = sheet.dark_median(lpix_y, apix_x, 12, 40)
        if lpix_y is None:
            return

        tpix_y, _tpix_x = sheet.inch2pix((inch_y_thickline, inch_x))
        tpix_y, _tpix_x, _snippet = sheet.dark_median(tpix_y, apix_x, 20, 40)

        sheet.add_landmark(lpix_y, apix_x, inch_y_thinline, inch_x, nam)
        sheet.add_landmark(tpix_y, apix_x, inch_y_thickline, inch_x, nam)

        self.snippet = sheet.img[
            min(tpix_y, lpix_y) - 20 : max(tpix_y, lpix_y) + 20,
            apix_x - 20 : apix_x + 20,
        ]

        print("HA", nam, (tpix_y - lpix_y) / (inch_y_thickline - inch_y_thinline))

class Sheet_130(sch.Sheet):
    ''' ... '''

    def locate_arrows(self):
        ''' Locate the arrows in the drawing border '''

        debug = DebugSnippets()

        for x_inch in range(1, 23, 2):
            arrow = HArrow(
                self,
                sch.INCH_T_L_E[0],
                sch.INCH_T_L_I[0],
                x_inch,
                "at_%d" % x_inch
            )
            if arrow.snippet is not None:
                debug.add(arrow.snippet)

        debug.newline()

        for y_inch in range(1, 14, 2):
            if not hasattr(self, "no_left_arrows"):
                arrow = VArrow(
                    self,
                    sch.INCH_B_L_E[1],
                    sch.INCH_B_L_I[1],
                    y_inch,
                    "al_%d" % y_inch
                )
                debug.add(arrow.snippet)
            if not hasattr(self, "no_right_arrows"):
                arrow = VArrow(
                    self,
                    sch.INCH_B_R_E[1],
                    sch.INCH_B_R_I[1],
                    y_inch,
                    "ar_%d" % y_inch
                )
                debug.add(arrow.snippet)
            debug.newline()

        for x_inch in range(1, 23, 2):
            arrow = HArrow(
                self,
                sch.INCH_B_L_E[0],
                sch.INCH_B_L_I[0],
                x_inch,
                "ab_%d" % x_inch
            )
            if arrow.snippet is not None:
                debug.add(arrow.snippet)

        debug.dump(self.fn_pfx + "arrows.png")

def main():
    ''' ... '''
    sheet = Sheet_130(sys.argv)
    sheet.load_raw_image()
    sheet.locate_arrows()
    sheet.write_landmarks()
    sheet.write_interpolators()
    sheet.write_interpolated()

if __name__ == "__main__":
    main()
