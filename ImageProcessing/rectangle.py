#!/usr/local/bin/python3.8
#
# NB: We strive to use y-x coordinate order to match numpy's convention

import numpy as np

from debug_snippets import DebugSnippets

class Rectangle():
    def __init__(self, tl, tr, bl, br):
        self.tl = tl
        self.tr = tr
        self.bl = bl
        self.br = br

    def __str__(self):
        return " ".join(
            [
                 "<R",
                 self.size(),
                 "h",
                 "%4.3f" % self.height(),
                 "w",
                 "%4.3f" % self.width(),
                 "tl",
                 "%6.3f %6.3f" % self.tl.inch,
                 "br",
                 "%6.3f %6.3f" % self.br.inch,
                 ">",
            ]
        )

    def __lt__(self, other):
        return self.area() < other.area()

    def height(self):
        return self.tl.inch[0] - self.br.inch[0]

    def width(self):
        return self.br.inch[1] - self.tl.inch[1]

    def size(self):
        return "%.1fx%.1f" % (round(self.width(),1), round(self.height(),1))

    def area(self):
        return (self.tl.pix[0] - self.br.pix[0]) * (self.tl.pix[1] - self.br.pix[1])

    def center_pix(self):
        cy = 0
        cx = 0
        for corner in (self.tl, self.tr, self.bl, self.br):
            cy += corner.pix[0]
            cx += corner.pix[1]
        return (cy//4, cx//4)

    def overlap(self, other):
        jtl_x = max(self.tl.pix[1], other.tl.pix[1])
        jtl_y = max(self.tl.pix[0], other.tl.pix[0])
        jbr_x = min(self.br.pix[1], other.br.pix[1])
        jbr_y = min(self.br.pix[0], other.br.pix[0])
        if jbr_y < jtl_y:
            return False
        if jbr_x < jtl_x:
            return False
        return True

    def align_to_pins(self, sheet):
        inch_center = sheet.pix2inch(self.center_pix())
        pin_off_y = self.pin_y_align(sheet, inch_center[0])
        print("PIN_Y", pin_off_y)
        pin_off_x = self.pin_x_align(sheet, inch_center[1])
        print("PIN_X", pin_off_x)
        if True:
            sheet.add_landmark(
                *self.center_pix(),
                pin_off_y,
                pin_off_x,
                "pin_xy"
            )

    def pin_y_align(self, sheet, base):
        debug = DebugSnippets()

        yhist = [0] * 10
        median = []

        for x0, x1 in (
            (self.tl.pix[1]-70, self.tl.pix[1]-25),
            (self.br.pix[1]+25, self.br.pix[1]+70),
        ):
            snippet = sheet.img[
                self.tl.pix[0] : self.br.pix[0],
                x0: x1,
            ]
            debug.add(snippet)

            for y in range(self.tl.pix[0], self.br.pix[0]):
                snippet = sheet.img[y, x0:x1]
                inch = sheet.pix2inch((y, (x0 + x1) // 2))
                idx = int(inch[0] * 100) % 10
                i = np.count_nonzero(snippet < 0)
                if i == snippet.shape[0]:
                    median.append(inch[0] - round(inch[0], 1))
                    yhist[idx] += 1

        median.sort()
        print("YHIST", " ".join("%2d" % i for i in yhist))
        print("YMEDIAN", sum(median), " ".join("%.2f" % x for x in median))
        debug.dump(sheet.fn_pfx + "piny_%.1fx%.1f.png" % sheet.pix2inch(self.tl.pix))
        if len(median) < 5:
            return None
        return base - median[len(median)//2]

    def pin_x_align(self, sheet, base):
        debug = DebugSnippets()

        xhist = [0] * 10
        median = []

        for y0, y1, y2, y3 in (
            (self.tl.pix[0]-70, self.tl.pix[0]-25, self.tl.pix[0]-15, self.tl.pix[0]-10),
            (self.br.pix[0]+25, self.br.pix[0]+70, self.br.pix[0]+10, self.br.pix[0]+15),
        ):
            snippet = sheet.img[
                y2: y3,
                self.tl.pix[1] : self.br.pix[1],
            ]
            debug.add(snippet)
            if np.amin(snippet) > 0:
                continue

            snippet = sheet.img[
                y0: y1,
                self.tl.pix[1] : self.br.pix[1],
            ]
            debug.add(snippet)

            for x in range(self.tl.pix[1], self.br.pix[1]):
                snippet = sheet.img[y0:y1, x]
                i = np.count_nonzero(snippet > 0)
                if i > 10:
                    continue

                inch = sheet.pix2inch(((y0 + y1) // 2, x))
                idx = int(inch[1] * 100) % 10
                i = np.count_nonzero(snippet < 0)
                if i == snippet.shape[0]:
                    median.append(inch[1] - round(inch[1], 1))
                    xhist[idx] += 1

        median.sort()
        print("XHIST", " ".join("%2d" % i for i in xhist))
        print("XMEDIAN", sum(median), " ".join("%.2f" % x for x in median))
        debug.dump(sheet.fn_pfx + "pinx_%.1fx%.1f.png" % sheet.pix2inch(self.tl.pix))
        if len(median) < 5:
            return None
        return base - median[len(median)//2]
