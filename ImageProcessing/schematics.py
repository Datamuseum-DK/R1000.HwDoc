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
The main tool-chest for the project
===================================

About coordinates and coordinate systems.

First, and most importantly, numpy indexes like this:  Image[Y][X]

The most important coordinate system is the original "drawing
coordinates", as marked out by the arrows and numbers between the
thick and the then borders:  This is what all the components, texts
and lines are positioned relative to.

The following have been established by counding pixels in the
original images:

The image resolution of the drawing coordinates is approx 265 ± 10 DPI

The inside of the thick outer border marks the edge of the "drawing
sheet", which is 23" wide and 14.9" tall.

The thick border was probably drawn with 0.06" thickness:  16 px / 265 px.

The middle of the thin inner border is located 0.2" from the edge
of the logical sheet (ie: BL=0.2"x0.2" TR=22.8"x14.7")

The thin border was probably drawn with 0.025" thickness: (6-7) px / 265 px.

It looks like the software used depended on a custom character-generator
with a 0.1"x0.1" pitch, driving a Versatec electrostatic matrix
plotter, and there are artifacts consistent with the actual output
having been produced on one.

This means that graphical objects could not be arbitrarily placed
on the paper, for instance all letters, digits and other glyphs
fit in a 0.1"x0.1" raster.

'''

import glob
import subprocess

import imageio

import numpy as np

from delaunay_interpolator import Interpolator

import finagle

import components
import page_numbers

APPROX_DPI = 265

INCH_HEIGHT = 14.9
INCH_WIDTH = 23.0

# Four corners of the logical sheet
INCH_T_L = (INCH_HEIGHT, 0)
INCH_T_R = (INCH_HEIGHT, INCH_WIDTH)
INCH_B_L = (0, 0)
INCH_B_R = (0, INCH_WIDTH)

# Four corners of the thick exterior border
# (The inner side is the logical sheet. Thickness is 16/265 = 0.06")
INCH_T_L_E = (INCH_HEIGHT + .03, -.03)
INCH_T_R_E = (INCH_HEIGHT + .03, INCH_WIDTH + .03)
INCH_B_L_E = (-.03, -.03)
INCH_B_R_E = (-.03, INCH_WIDTH + .03)

# Four corners of the thin interior border
INCH_T_L_I = (INCH_HEIGHT - .2, .2)
INCH_T_R_I = (INCH_HEIGHT - .2, INCH_WIDTH - .2)
INCH_B_L_I = (.2, .2)
INCH_B_R_I = (.2, INCH_WIDTH - .2)

# Top left corner of documentation box
INCH_T_L_DOCBOX = (4.10, 18.40)

LINE_CORR = 20

class Point():

    def __init__(self, pix=(None, None), inch=(None, None)):
        self.py, self.px = pix
        self.iy, self.ix = inch

    def get_pix(self):
        return (self.py, self.px)

    def set_pix(self, pix):
        self.py, self.px = pix

    pix = property(get_pix, set_pix)

    def get_inch(self):
        return (self.iy, self.ix)

    def set_inch(self, inch):
        self.iy, self.ix = inch

    inch = property(get_inch, set_inch)

    def proj_pix(self, sheet):
        self.pix = sheet.inch2pix(self.inch)

    def proj_inch(self, sheet):
        self.inch = sheet.pix2inch(self.pix)

    def __str__(self):
        return " ".join(
            (
                 "<P",
                 str(self.py),
                 str(self.px),
                 str(self.iy),
                 str(self.ix),
                 ">",
            )
        )

def inch2proj(inch):
    return (int((INCH_HEIGHT - inch[0]) * 50), int(inch[1] * 50))

def proj2inch(pix):
    return (INCH_HEIGHT - pix[0] / 50, pix[1] / 50)

def write_image_normalized(img, fno, **kwargs):
    ''' Normalize (copy of) image to [0…255] and write to file '''
    min_val = np.amin(img)
    oimg = img - min_val
    max_val = np.amax(oimg)
    oimg *= (255. / max_val)
    imageio.imwrite(fno, oimg.astype(np.uint8), **kwargs)

def inch_window(inch, size):
    inch_tl_y = inch[0] + size[0] / 2
    inch_tl_x = inch[1] - size[1] / 2
    inch_br_y = inch_tl_y - size[0]
    inch_br_x = inch_tl_x + size[1]
    return (inch_tl_y, inch_tl_x), (inch_br_y, inch_br_x)

def window(pix, size):
    pix_tl_y = pix[0] - size[0] // 2
    pix_tl_x = pix[1] - size[1] // 2
    pix_br_y = pix_tl_y + size[0]
    pix_br_x = pix_tl_x + size[1]
    return (pix_tl_y, pix_tl_x), (pix_br_y, pix_br_x)

def snippet(image, pix_tl, pix_br):
    assert pix_tl[0] < pix_br[0]
    assert pix_tl[1] < pix_br[1]
    return image[pix_tl[0]:pix_br[0], pix_tl[1]:pix_br[1]]

def add_big_marker(image, pix_y, pix_x):
    ''' As it says in the tin... '''
    for distance, value in (
        (19, -1),
        (11, 1),
        (3, -1),
    ):
        image[
            pix_y - distance : pix_y + distance + 1,
            pix_x - distance : pix_x + distance + 1,
        ] = value
    image[pix_y][pix_x] = -value

def add_small_marker(image, pix_y, pix_x):
    ''' As it says in the tin... '''
    for distance, value in (
        (7, -1),
        (5, 1),
        (1, -1),
    ):
        image[
            pix_y - distance : pix_y + distance + 1,
            pix_x - distance : pix_x + distance + 1,
        ] = value
    image[pix_y][pix_x] = -value

class XY_Histogram():
    ''' A XY Histogram '''

    def __init__(self, img, pix_y, pix_x, dimension, gate = .66, minwidth = 5):
        ''' Find the average coordinate of the coords with the longest runs '''
        pix_y0 = pix_y - dimension // 2
        pix_x0 = pix_x - dimension // 2
        self.snippet = np.array(
            img[pix_y0 : pix_y0 + dimension, pix_x0 : pix_x0 + dimension]
        )
        histogram_x = []
        histogram_y = []

        for ipix_x in range(dimension):
            cur_run_x = 0
            pix_x_runs = set((0,))
            cur_run_y = 0
            pix_y_runs = set((0,))
            for ipix_y in range(dimension):
                if self.snippet[ipix_y][ipix_x] < 0:
                    cur_run_x += 1
                else:
                    pix_x_runs.add(cur_run_x)
                    cur_run_x = 0
                if self.snippet[ipix_x][ipix_y] < 0:
                    cur_run_y += 1
                else:
                    pix_y_runs.add(cur_run_y)
                    cur_run_y = 0
            pix_x_runs.add(cur_run_x)
            pix_y_runs.add(cur_run_y)
            histogram_x.append(max(pix_x_runs))
            histogram_y.append(max(pix_y_runs))

        if histogram_x:
            self.max_x = max(histogram_x)
        else:
            self.max_x = 0
        if histogram_y:
            self.max_y = max(histogram_y)
        else:
            self.max_y = 0

        retval=[]
        for hist in (histogram_y, histogram_x):
            if not hist:
                retval.append(2)
                continue

            threshold = gate * max(hist)
            # print(list(j for j in hist if j > threshold))
            pixel_sum = 0
            sum_count = 0
            for pixel, run_length in enumerate(hist):
                if run_length > threshold:
                    pixel_sum += pixel
                    sum_count += 1
            if sum_count >= minwidth:
                retval.append(int(pixel_sum/sum_count))
            else:
                retval.append(2)

        if histogram_x and histogram_y:
            add_small_marker(self.snippet, retval[0], retval[1])

        self.val_y = retval[0] + pix_y0
        self.val_x = retval[1] + pix_x0

    def __str__(self):
        return "<XY %.2f %.2f %.2f %.2f>" % (
            self.val_x, self.val_y,
            self.max_x, self.max_y,
        )

class LandMark(Point):
    ''' A landmark links pixel coordinates to inch coordinates '''

    def __init__(self, pix_y, pix_x, inch_y, inch_x, name):
        super().__init__((pix_y, pix_x), (inch_y, inch_x))
        self.name = name

    def __str__(self):
        return " ".join([
            "<LM",
            self.name,
            str(self.py),
            str(self.px),
            str(self.iy),
            str(self.ix),
        ])

    def dump(self, file):
        ''' Write landmark to file '''
        file.write(
            " ".join(
                (
                    str(self.py),
                    str(self.px),
                    str(self.iy),
                    str(self.ix),
                    self.name,
                )
            ) + "\n"
        )

def per_image_finagle_constants(board, sheet, cls):
    ''' Set any hardcoded properties for this specific image '''
    i = finagle.FINAGLE_PAGES.get(board)
    if not i:
        return
    i = i.get(sheet)
    if not i:
        return
    print("Configured Properties for", board, sheet)
    for prop, val in i.items():
        print("    ", prop, val)
        setattr(cls, prop, val)

class Sheet():

    ''' One Schematic Image file '''

    def __init__(self, argv):
        assert len(argv) == 3
        self.step = argv[0].split("_")[1]
        self.board = argv[1]
        self.sheet = argv[2]
        self.page = page_numbers.page_number(self.board, self.sheet)
        self.sch_file = "Proj/%s/pg_%02d.kicad_sch" % (self.board, self.page)

        self.dstdir = self.board + "/" + self.sheet + "/"
        self.fn_pfx = self.dstdir + self.step + "_"

        per_image_finagle_constants(self.board, self.sheet, self)

        self.bom = components.BOM()

        self.landmarks = []
        try:
            self.load_landmarks()
        except FileNotFoundError:
            pass
        self.pix2inch_x = None
        self.pix2inch_y = None
        self.inch2pix_x = None
        self.inch2pix_y = None
        self.img = None
        self.proj50 = None

        print("Processing", self.board, self.sheet, "step", self.step, "in", self.dstdir)

    def find_stepped_file(self, basename):
        ''' Find the most recent step for a file '''
        filename = None
        for i in sorted(glob.glob(self.dstdir + "???_" + basename)):
            if i < self.fn_pfx:
                filename = i
        if filename is None:
            raise FileNotFoundError("No (earlier) %s file found" % basename)
        return filename

    def load_raw_image(self):
        ''' Load and normalize image '''
        filename = self.find_stepped_file("raw_image.png")
        self.img = imageio.imread(filename).astype(float)
        self.img -= np.amin(self.img)
        self.img /= np.amax(self.img) * .5
        self.img -= 1
        print("Loaded", filename)

    def load_proj50_image(self):
        ''' Load and normalize image '''
        filename = self.find_stepped_file("proj50.png")
        self.proj50 = imageio.imread(filename).astype(float)
        self.proj50 -= np.amin(self.proj50)
        self.proj50 /= np.amax(self.proj50) * .5
        self.proj50 -= 1
        print("Loaded", filename)

    def load_components(self):
        ''' ... '''
        filename = self.find_stepped_file("components.txt")
        self.bom.load_from_file(filename)
        print("Loaded", filename)

    def write_components(self):
        ''' ... '''
        self.bom.write_to_file(self.fn_pfx + "components.txt")

    def write_image(self, basename, img=None):
        ''' Write the image to a file '''
        filename = self.fn_pfx + basename + ".png"
        if img is None:
            img = self.img
        print("Writing to", filename)
        write_image_normalized(img, filename)

    def project(self, resolution):
        ''' Create a projected image with resolution pixels per inch '''
        print("Projecting for", resolution, "DPI")
        proj_height = int(INCH_HEIGHT * resolution)
        proj_width = int(INCH_WIDTH * resolution)
        projected = np.zeros([proj_height, proj_width], dtype=float)

        for proj_y in range(proj_height):
            for proj_x in range(proj_width):
                inch_x = proj_x / resolution
                inch_y = proj_y / resolution
                pix_y, pix_x = self.inch2pix((INCH_HEIGHT - inch_y, inch_x))
                if pix_x != -9999 and pix_y != -9999:
                    val = self.img[pix_y][pix_x]
                    projected[proj_y][proj_x] = val

        filename = self.dstdir + '/proj_%d.png' % resolution
        return projected

    def add_grid(self, img=None):
        ''' Add inch->pix projected grid '''
        print("Adding grid")
        if img is None:
            img = self.img
        pix_height, pix_width = img.shape
        if True:
            for inch_x in range(0, int(INCH_WIDTH * 100), 10):
                for inch_y in range(0, int(INCH_HEIGHT *100), 10):
                    pix_y, pix_x = self.inch2pix(
                        (
                            inch_y * .01 + .05,
                            inch_x * .01 + .05)
                    )
                    if pix_x < 0 or pix_y < 0 or pix_x >= pix_width or pix_y >= pix_height:
                        continue
                    img[pix_y][pix_x] *= -1
                    for i in (1, 2):
                        img[pix_y+i][pix_x] *= -1
                        img[pix_y-i][pix_x] *= -1
                        img[pix_y][pix_x+i] *= -1
                        img[pix_y][pix_x-i] *= -1

        if False:
            for inch_x in range(0, int(INCH_WIDTH * 100), 10):
                for inch_y in range(0, int(INCH_HEIGHT * 100), 1):
                    pix_y, pix_x = self.inch2pix((inch_y * .01 + .05, inch_x * .01 + .05))
                    if pix_x < 0 or pix_y < 0 or pix_x >= pix_width or pix_y >= pix_height:
                        continue
                    img[pix_y-1:pix_y+1, pix_x-1:pix_x+1] *= -1

        if False:
            for inch_x in range(0, int(INCH_WIDTH * 100), 1):
                for inch_y in range(0, int(INCH_HEIGHT * 100), 10):
                    pix_y, pix_x = self.inch2pix((inch_y * .01 + .05, inch_x *.01 + .05))
                    if pix_x < 0 or pix_y < 0 or pix_x >= pix_width or pix_y >= pix_height:
                        continue
                    img[pix_y-1:pix_y+1, pix_x-1:pix_x+1] *= -1

    def pix2inch(self, pix):
        ''' Interpolate from pixels to inches '''

        if not self.pix2inch_x or len(self.pix2inch_x) != len(self.landmarks):

            self.pix2inch_x = Interpolator(
                [(l.py, l.px, l.ix) for l in self.landmarks if None not in (l.py, l.px, l.ix)]
            )

            self.pix2inch_y = Interpolator(
                [(l.py, l.px, l.iy) for l in self.landmarks if None not in (l.py, l.px, l.iy)]
            )

        return (self.pix2inch_y.lookup(*pix), self.pix2inch_x.lookup(*pix))

    def inch2pix(self, inch):
        ''' Interpolate from inches to pixels '''

        if not self.inch2pix_x or len(self.inch2pix_x) != len(self.landmarks):

            self.inch2pix_x = Interpolator(
                [(l.iy, l.ix, l.px) for l in self.landmarks if None not in (l.iy, l.ix, l.px)]
            )

            self.inch2pix_y = Interpolator(
                [(l.iy, l.ix, l.py) for l in self.landmarks if None not in (l.iy, l.ix, l.py)]
            )

        return (int(self.inch2pix_y.lookup(*inch)), int(self.inch2pix_x.lookup(*inch)))

    def add_landmark(self, pix_y, pix_x, inch_y, inch_x, name):
        ''' Add a landmark '''
        retval = LandMark(pix_y, pix_x, inch_y, inch_x, name)
        self.landmarks.append(retval)

        # When we only project one coordinate, also add an the inverse "half" landmark
        if pix_x is None:
            _pix_y, pix_x = self.inch2pix((inch_y, inch_x))
            lm = LandMark(pix_y, pix_x, inch_y, None, name)
            self.landmarks.append(lm)
        elif pix_y is None:
            pix_y, _pix_x = self.inch2pix((inch_y, inch_x))
            lm = LandMark(pix_y, pix_x, None, inch_x, name)
            self.landmarks.append(lm)
        elif inch_x is None:
            _inch_y, inch_x = self.pix2inch((pix_y, pix_x))
            lm = LandMark(pix_y, None, inch_y, inch_x, name)
            self.landmarks.append(lm)
        elif inch_y is None:
            inch_y, _inch_x = self.pix2inch((pix_y, pix_x))
            lm = LandMark(None, pix_x, inch_y, inch_x, name)
            self.landmarks.append(lm)

        return retval

    def write_landmarks(self):
        ''' Dump the landmarks '''
        filename = self.fn_pfx + "landmarks.txt"
        with open(filename, "w") as file:
            for i in self.landmarks:
                i.dump(file)
        print("Wrote", filename)

    def load_landmarks(self):
        ''' Load latest landmarks from previous steps '''

        self.landmarks = []
        self.inch2pix_y = None
        self.inch2pix_x = None
        self.pix2inch_y = None
        self.pix2inch_x = None

        filename = self.find_stepped_file("landmarks.txt")
        with open(filename, "r") as file:
            for i in file:
                j = i.split(maxsplit=5)
                l = []
                for k in j[0:4]:
                    if k == "None":
                        l.append(None)
                    else:
                        l.append(float(k))
                self.add_landmark(*(l), j[4])
        print("Loaded", filename)

    def write_interpolators(self):
        ''' Dump the geometry of the interpolators '''
        self.pix2inch((0, 0))
        self.inch2pix((0, 0))
        self.pix2inch_x.dump_x(self.fn_pfx + "pix2inch_x", inv=(True,True))
        self.pix2inch_y.dump_y(self.fn_pfx + "pix2inch_y", inv=(True,False))
        self.inch2pix_x.dump_x(self.fn_pfx + "inch2pix_x", inv=(False,False))
        self.inch2pix_y.dump_y(self.fn_pfx + "inch2pix_y", inv=(False,False))
        with open(self.fn_pfx + "_.g", "w") as file:
            file.write('set term png size 800,480\n')
            for i in (
                 "pix2inch_x",
                 "pix2inch_y",
                 "inch2pix_x",
                 "inch2pix_y",
            ):
                file.write('set output "' + self.fn_pfx + i + '.png"\n')
                file.write('load "' + self.fn_pfx + i + '.g"\n')
        subprocess.run(["gnuplot", self.fn_pfx + "_.g"])

    def write_interpolated(self):
        img = np.array(self.img)
        self.add_grid(img)
        if True:
            for landmark in self.landmarks:
                if None in (landmark.py, landmark.px):
                    continue
                py = int(landmark.py)
                px = int(landmark.px)
                if landmark.iy is not None:
                     img[py - 3, px-40:px+40] *= -1
                     img[py + 3, px-40:px+40] *= -1
                if landmark.ix is not None:
                     img[py-40:py+40, px - 3] *= -1
                     img[py-40:py+40, px + 3] *= -1
        write_image_normalized(img, self.fn_pfx + "landmarks.png")

    def dark_median(self, pix_y, pix_x, pix_height, pix_width):
        ''' return median x & y for dark pixels in pix_x±pix_width, pix_y±pix_height window '''
        snippet = self.img[
            pix_y - pix_height : pix_y + pix_height + 1,
            pix_x - pix_width : pix_x + pix_width + 1,
        ]
        pix_x_list = []
        pix_y_list = []
        for delta_y in range(-pix_height, pix_height + 1):
            for delta_x in range(-pix_width, pix_width + 1):
                if self.img[pix_y + delta_y][pix_x + delta_x] < 0:
                    pix_y_list.append(pix_y + delta_y)
                    pix_x_list.append(pix_x + delta_x)
        pix_x_list.sort()
        if pix_x_list:
            pix_x_median = pix_x_list[len(pix_x_list)//2]
        else:
            pix_x_median = None
        pix_y_list.sort()
        if pix_y_list:
            pix_y_median = pix_y_list[len(pix_y_list)//2]
        else:
            pix_y_median = None

        if pix_x_median and pix_y_median:
            add_small_marker(
                snippet,
                pix_height + pix_y_median - pix_y,
                pix_width + pix_x_median - pix_x,
            )
        return pix_y_median, pix_x_median, snippet

    def hide_borders(self, img, dpi):
        ''' Paint over the drawing border and docbox '''

        EXTRA = .05

        def inch_x(x):
            return int(x * dpi)

        def inch_y(y):
            # inch-coords are in quadrant I, pix-coords are in IV
            return int((INCH_HEIGHT - y) * dpi)

        def blank(tl, br):
            img[
                inch_y(tl[0]) : inch_y(br[0]),
                inch_x(tl[1]) : inch_x(br[1])
            ] *= 0

        blank((INCH_B_L_I[0] + EXTRA, 0), (0, INCH_WIDTH))
        blank((INCH_HEIGHT, 0), (INCH_T_R_I[0] - EXTRA, INCH_WIDTH))
        blank((INCH_HEIGHT, 0), (0, INCH_B_L_I[1] + EXTRA))
        blank((INCH_HEIGHT, INCH_T_R_I[1] - EXTRA), (0, INCH_WIDTH))
        blank((INCH_T_L_DOCBOX[0] + EXTRA, INCH_T_L_DOCBOX[1] - EXTRA), (0, INCH_WIDTH))
