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
STEP 110
========

	Read the PGM file.
	Crop/paste to get rid of/ensure extra space around thick border.
	(Including special handling for IOC_0063)
	White out blank 0.1"x0.1" squares
	Write raw image
	Write landmarks for thick/thin corners
'''

import sys

import numpy as np

import imageio

import schematics as sch

import templates

from debug_snippets import DebugSnippets

class Sheet_110(sch.Sheet):

    ''' ... '''

    def load_pgm_image(self):
        ''' Load the PGM image and add a white border '''

        imgfile = "../" + self.board + "/rawimg/_-" + self.sheet + ".pgm"
        self.img = imageio.imread(imgfile).astype(np.float)
        self.img -= np.amin(self.img)
        self.img /= np.amax(self.img) * .5
        self.img -= 1

    FOO_MARGIN = 20

    def locate(self):
        self.locate_br()
        self.locate_tr()
        self.locate_tl()
        self.locate_bl()

        dbg = DebugSnippets()
        dbg.add(self.snip_tl)
        dbg.add(self.snip_tr)
        dbg.newline()
        dbg.add(self.snip_bl)
        dbg.add(self.snip_br)
        dbg.dump(self.fn_pfx + "corners.png")

        with open(self.fn_pfx + "outline.txt", "w") as file:
            file.write("\n\n%d %d\n" % self.found_br)
            file.write("%d %d\n" % self.found_tr)
            file.write("%d %d\n" % self.found_tl)
            file.write("%d %d\n" % self.found_bl)
            file.write("%d %d\n" % self.found_br)

    def locate_br(self):
        template = templates.string_2_template(open("step_110_template_br.txt").read())
        yr = [ -630, -138]
        xr = [ -376, -21]
        self.found_br, self.snip_br = self.do_locate(template, self.img.shape, yr, xr, "br")

    def locate_tr(self):
        template = templates.string_2_template(open("step_110_template_tr.txt").read())
        yr = [-3930, -3826]
        xr = [-133, -44]
        self.found_tr, self.snip_tr = self.do_locate(template, self.found_br, yr, xr, "tr")

    def locate_tl(self):
        template = templates.string_2_template(open("step_110_template_tl.txt").read())
        yr = [-112, 49]
        xr = [-6077, -5911]
        self.found_tl, self.snip_tl = self.do_locate(template, self.found_tr, yr, xr, "tl")

    def locate_bl(self):
        template = templates.string_2_template(open("step_110_template_bl.txt").read())
        yr = [3878, 4015]
        xr = [-28, 86]
        self.found_bl, self.snip_bl = self.do_locate(template, self.found_tl, yr, xr, "bl")
        if self.board == "MEM32" and self.sheet == "0005":
            self.found_bl = (
                self.found_bl[0] + 64,
                self.found_bl[1] - 64,
            )
        if self.board == "VAL" and self.sheet == "0008":
            self.found_bl = (
                self.found_bl[0] + 64,
                self.found_bl[1] - 64,
            )

    def do_locate(self, template, ref, yr, xr, suf):

        ''' yr and xr are the range of expected findings '''

        yl = max(0, min(self.img.shape[0], ref[0] + yr[0] - (template.shape[0] + self.FOO_MARGIN)))
        yh = max(0, min(self.img.shape[0], ref[0] + yr[1] + (template.shape[0] + self.FOO_MARGIN)))
        xl = max(0, min(self.img.shape[1], ref[1] + xr[0] - (template.shape[1] + self.FOO_MARGIN)))
        xh = max(0, min(self.img.shape[1], ref[1] + xr[1] + (template.shape[1] + self.FOO_MARGIN)))

        print("YYY", yl, yh, xl, xh)

        # sch.write_image_normalized(template, self.fn_pfx + "template_" + suf + ".png")

        for pix, merit, snippet in templates.find_in_window(
            self.img,
            template,
            ((yh + yl) // 2, (xh + xl) // 2),
            (yh - yl, xh - xl),
        ):
            snip = sch.snippet(self.img, *sch.window(pix, template.shape))
            snip = np.array(snip)
            if snip.shape != template.shape:
                print("SN_SHAPE", snip.shape)
            snip *= .25
            # sch.add_small_marker(self.img, *pix)
            self.write_image("match_" + suf, snippet)
            break

        print("FBL", pix)
        fo = open("/tmp/_" + suf, "a")
        fo.write(
             "%d %d %.1f %s %s %d %d\n" % (
                 pix[0], pix[1], merit, self.board, self.sheet, pix[0] - ref[0], pix[1] - ref[1]
             )
        )
        fo.close()
        return pix, snip

    def corners(self):

        self.ext_tl = (self.found_tl[0] - 28, self.found_tl[1] - 27)
        self.int_tl = (self.found_tl[0] + 34, self.found_tl[1] + 34)

        self.ext_tr = (self.found_tr[0] - 57, self.found_tr[1] + 172)
        self.int_tr = (self.found_tr[0] + 6, self.found_tr[1] + 110)

        self.ext_bl = (self.found_bl[0] + 38, self.found_bl[1] - 35)
        self.int_bl = (self.found_bl[0] - 25, self.found_bl[1] + 27)

        self.ext_br = (self.found_br[0] + 102, self.found_br[1] + 75)
        self.int_br = (self.found_br[0] + 40, self.found_br[1] + 14)

        if False:
            sch.add_small_marker(self.img, *self.ext_tl)
            sch.add_small_marker(self.img, *self.ext_tr)
            sch.add_small_marker(self.img, *self.ext_bl)
            sch.add_small_marker(self.img, *self.ext_br)
            sch.add_small_marker(self.img, *self.int_tl)
            sch.add_small_marker(self.img, *self.int_tr)
            sch.add_small_marker(self.img, *self.int_bl)
            sch.add_small_marker(self.img, *self.int_br)

    def bbox(self):
        bbox_tl = (
            min(self.ext_tl[0], self.ext_tr[0]) - 50,
            min(self.ext_tl[1], self.ext_bl[1]) - 50,
        )
        bbox_br = (
            max(self.ext_bl[0], self.ext_br[0]) + 50,
            max(self.ext_tr[1], self.ext_br[1]) + 50,
        )

        bbox_sz = (bbox_br[0] - bbox_tl[0], bbox_br[1] - bbox_tl[1])

        print("BBOX", bbox_tl, bbox_br)

        if min(bbox_tl) >= 0 and bbox_br[0] < self.img.shape[0] and bbox_br[1] < self.img.shape[1]:
            print("CROPPING", bbox_tl, bbox_br)
            off = bbox_tl
            self.img = self.img[bbox_tl[0]:bbox_br[0], bbox_tl[1]:bbox_br[1]]
        elif min(bbox_tl) >= 0:
            move = (
                min(bbox_sz[0], self.img.shape[0] - bbox_tl[0]),
                min(bbox_sz[1], self.img.shape[1] - bbox_tl[1]),
            )
            print("PASTING", bbox_tl, bbox_br, bbox_sz, move)
            tmp = np.zeros(list(bbox_sz), dtype=np.float)
            tmp += 1
            tmp[
                0 : move[0],
                0 : move[1],
            ] = self.img [
                bbox_tl[0]:bbox_tl[0] + move[0],
                bbox_tl[1]:bbox_tl[1] + move[1],
            ]
            self.img = tmp
            off = bbox_tl
        else:
            off = (0, 0)
            sch.add_small_marker(self.img, *bbox_tl)
            sch.add_small_marker(self.img, *bbox_br)

        for i in ("tl", "tr", "bl", "br"):
            for j in ("ext_", "int_"):
                a = getattr(self, j + i)
                a = (a[0] - off[0], a[1] - off[1])
                setattr(self, j + i, a)

        if False:
            sch.add_small_marker(self.img, *self.ext_tl)
            sch.add_small_marker(self.img, *self.ext_tr)
            sch.add_small_marker(self.img, *self.ext_bl)
            sch.add_small_marker(self.img, *self.ext_br)
            sch.add_small_marker(self.img, *self.int_tl)
            sch.add_small_marker(self.img, *self.int_tr)
            sch.add_small_marker(self.img, *self.int_bl)
            sch.add_small_marker(self.img, *self.int_br)
        if True:
            self.add_landmark(*self.ext_tl, *sch.INCH_T_L_E, "ec_tl")
            self.add_landmark(*self.ext_tr, *sch.INCH_T_R_E, "ec_tr")
            self.add_landmark(*self.ext_bl, *sch.INCH_B_L_E, "ec_bl")
            self.add_landmark(*self.ext_br, *sch.INCH_B_R_E, "ec_br")
        if True:
            self.add_landmark(*self.int_tl, *sch.INCH_T_L_I, "ic_tl")
            self.add_landmark(*self.int_tr, *sch.INCH_T_R_I, "ic_tr")
            self.add_landmark(*self.int_bl, *sch.INCH_B_L_I, "ic_bl")
            self.add_landmark(*self.int_br, *sch.INCH_B_R_I, "ic_br")

    def ioc_0063(self):
        tmp = np.zeros([5079,2000 + 6591] , dtype=np.float)
        tmp += 1
        tmp[:,2000:] = self.img
        self.img = tmp

        self.ext_tl = (618, 1344)
        self.ext_tr = (569, 7488)
        self.ext_bl = (4638, 1397)
        self.ext_br = (4587, 7529)

        self.int_tl = (680, 1413)
        self.int_tr = (627, 7431)
        self.int_bl = (4578, 1456)
        self.int_br = (4532, 7467)

    def white_out(self):
        y = sch.INCH_B_L_I[0]
        while y + .1 < sch.INCH_T_L_I[0]:
           x = sch.INCH_B_L_I[1]
           while x + .1 < sch.INCH_B_R_I[1]:
               pix_tl = self.inch2pix((y + .1, x))
               pix_br = self.inch2pix((y, x + .1))
               print("%.1f %.1f" % (y, x), pix_tl, pix_br)
               snippet = sch.snippet(self.img, pix_tl, pix_br)
               if np.amin(snippet) >= 0:
                   snippet *= 0
                   snippet += 1
               x += .1
           y += .1

if __name__ == "__main__":
    assert len(sys.argv) == 3
    sheet = Sheet_110(sys.argv)
    sheet.load_pgm_image()
    if sheet.board == "IOC" and sheet.sheet == "0063":
        sheet.ioc_0063()
    else:
        sheet.locate()
        sheet.corners()
    sheet.bbox()
    sheet.white_out()
    sheet.write_image("raw_image")
    sheet.write_landmarks()
    sheet.write_interpolators()
    sheet.write_interpolated()
