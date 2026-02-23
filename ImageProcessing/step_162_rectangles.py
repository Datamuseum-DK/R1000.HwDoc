#!/usr/local/bin/python3.8
#
# NB: We strive to use y-x coordinate order to match numpy's convention

'''
'''

import sys

import imageio

import numpy as np

import schematics as sch

from debug_snippets import DebugSnippets

from rectangle import Rectangle

import templates

class SchematicImage(sch.Sheet):

    ''' One Schematic Image file '''

    PSIZE = 35
    MIN_WID = .5 * sch.APPROX_DPI
    MAX_WID = 3.0 * sch.APPROX_DPI
    MIN_HT = .5 * sch.APPROX_DPI
    MAX_HT = 10 * sch.APPROX_DPI

    def __init__(self, argv):
        super().__init__(argv)

        self.load_proj50_image()
        self.load_raw_image()

        debug = DebugSnippets()
        for pt_bl in self.iter_bl():

            debug.newline()
            snippet = sch.snippet(self.img, *sch.window(pt_bl.pix, (120,140)))
            if 0 in snippet.shape:
                continue
            snippet = np.array(snippet)
            snippet[60,:] *= -.25
            snippet[:,70] *= -.25
            debug.add(snippet)

            pt_br = self.wander_to_br(pt_bl, debug)
            if not pt_br:
                continue
            if pt_br.px - pt_bl.px < self.MIN_WID:
                print("Too narrow", (pt_br.px - pt_bl.px) / sch.APPROX_DPI)
                continue

            pt_tr = self.wander_to_tr(pt_br, debug)
            if not pt_tr:
                continue
            if pt_br.py - pt_tr.py < self.MIN_HT:
                print("Too low", (pt_br.py - pt_tr.py) / sch.APPROX_DPI)
                continue

            pt_tl = self.wander_to_tl(pt_tr, debug)
            if not pt_tl:
                continue
            pt_bl2 = self.wander_to_bl(pt_tl, debug)
            if not pt_bl2:
                continue

            d = (pt_bl2.px - pt_bl.px)**2 + (pt_bl2.py - pt_bl.py)**2
            if d > 200:
                print("D-bl", d)
                continue

            print("BL+", "%.3f" % pt_bl.merit, "%3d" % d, pt_bl, pt_br, pt_tr, pt_tl)

            pt_tl.proj_inch(self)
            pt_bl.proj_inch(self)
            pt_tr.proj_inch(self)
            pt_br.proj_inch(self)
            proj_tr = sch.inch2proj(pt_tr.inch)
            proj_bl = sch.inch2proj(pt_bl.inch)
            snippet = self.proj50[
                proj_tr[0] - 3: proj_bl[0] + 3,
                proj_bl[1] - 3: proj_tr[1] + 3,
            ]
            debug.add(snippet)
            snippet *= -.25

            pos = "%.1f_%.1f" % pt_tl.inch

            if pos == "1.8_18.4":
                # We found the docbox
                continue

            fn = self.fn_pfx + "rectangle_at_" + pos + ".png"

            snippet = self.img[
                pt_tl.py - 75 : pt_br.py + 75,
                pt_tl.px - 75 : pt_br.px + 75,
            ]
            sch.write_image_normalized(snippet, fn)

            rect = Rectangle(
                pt_tl,
                pt_tr,
                pt_bl,
                pt_br,
            )
            rect.align_to_pins(self)
            self.bom.add_chip(rect, fn)

        debug.dump(self.fn_pfx + "wander.png")

    def wander_to_br(self, pt_bl, debug):

        pt_br = sch.Point(pt_bl.pix)

        while True:
            if pt_br.px - pt_bl.px > self.MAX_WID:
                print("Too wide", (pt_br.px - pt_bl.px) / sch.APPROX_DPI)
                return None
            if False:
                print("br", pt_br)
                snippet = sch.snippet(self.img, *sch.window(pt_br.pix, (20,20)))
                debug.add(snippet)
            for dy in (0, -1, 1, -2, 2,):
                if np.count_nonzero(self.img[pt_br.py + dy , pt_br.px:pt_br.px + 10] > 0) < 1:
                    pt_br.py += dy
                    pt_br.px += 1
                    break
            if self.img[pt_br.py][pt_br.px + 1] < 0:
                pt_br.px += 1
                continue
            break

        for n in range(10):
            if np.count_nonzero(self.img[pt_br.py - 10:pt_br.py, pt_br.px] < 0) == 10:
                break
            pt_br.px -= 1

        snippet = sch.snippet(self.img, *sch.window(pt_br.pix, (120,120)))
        snippet = np.array(snippet)
        snippet[60,:] *= -.25
        snippet[:,60] *= -.25
        debug.add(snippet)

        if n == 9:
            return None

        return pt_br

    def wander_to_tr(self, pt_br, debug):

        pt_tr = sch.Point(pt_br.pix)

        while True:
            if pt_br.py - pt_tr.py > self.MAX_HT:
                print("Too tall", (pt_br.py - pt_tr.py) / sch.APPROX_DPI)
                return None
            if False:
                print("tr", pt_tr)
                snippet = sch.snippet(self.img, *sch.window(pt_tr.pix, (20,20)))
                debug.add(snippet)
            for dx in (0, -1, 1, -2, 2):
                if np.count_nonzero(self.img[pt_tr.py - 10:pt_tr.py, pt_tr.px + dx] > 0) < 1:
                    pt_tr.py -= 2
                    pt_tr.px += dx
                    break
            if self.img[pt_tr.py - 1][pt_tr.px] < 0:
                pt_tr.py -= 1
                continue
            break

        for n in range(10):
            if np.count_nonzero(self.img[pt_tr.py , pt_tr.px - 10:pt_tr.px] < 0) == 10 :
                break
            pt_tr.py += 1

        snippet = sch.snippet(self.img, *sch.window(pt_tr.pix, (120,120)))
        snippet = np.array(snippet)
        snippet[60,:] *= -.25
        snippet[:,60] *= -.25
        debug.add(snippet)

        if n == 9:
            return None

        return pt_tr

    def wander_to_tl(self, pt_tr, debug):

        pt_tl = sch.Point(pt_tr.pix)

        while True:
            if pt_tr.px - pt_tl.px > self.MAX_WID:
                return None
            if False:
                print("tl", pt_tl)
                snippet = sch.snippet(self.img, *sch.window(pt_tl.pix, (20,20)))
                debug.add(snippet)
            for dy in (0, -1, 1, -2, 2, -3, 3):
                if np.count_nonzero(self.img[pt_tl.py + dy , pt_tl.px - 10:pt_tl.px] > 0) < 1:
                    pt_tl.py += dy
                    pt_tl.px -= 2
                    break
            if self.img[pt_tl.py][pt_tl.px + 1] < 0:
                pt_tl.px -= 1
                continue
            break

        for n in range(10):
            if np.count_nonzero(self.img[pt_tl.py:pt_tl.py + 10, pt_tl.px] < 0) == 10:
                break
            pt_tl.px += 1

        snippet = sch.snippet(self.img, *sch.window(pt_tl.pix, (120,120)))
        snippet = np.array(snippet)
        snippet[60,:] *= -.25
        snippet[:,60] *= -.25
        debug.add(snippet)

        if n == 9:
            return None

        return pt_tl

    def wander_to_bl(self, pt_tl, debug):

        pt_bl= sch.Point(pt_tl.pix)

        while True:
            if pt_bl.py - pt_tl.py > self.MAX_HT:
                return None
            if False:
                print("bl", pt_bl)
                snippet = sch.snippet(self.img, *sch.window(pt_bl.pix, (20,20)))
                debug.add(snippet)
            for dx in (0, -1, 1, -2, 2):
                if np.count_nonzero(self.img[pt_bl.py:pt_bl.py + 10, pt_bl.px + dx] > 0) < 1:
                    pt_bl.py += 2
                    pt_bl.px += dx
                    break
            if self.img[pt_bl.py + 1][pt_bl.px] < 0:
                pt_bl.py += 1
                continue
            break

        for n in range(10):
            if np.count_nonzero(self.img[pt_bl.py , pt_bl.px:pt_bl.px + 10] < 0) == 10 :
                break
            pt_bl.py -= 1

        snippet = sch.snippet(self.img, *sch.window(pt_bl.pix, (120,120)))
        snippet = np.array(snippet)
        snippet[60,:] *= -.25
        snippet[:,60] *= -.25
        debug.add(snippet)

        if n == 9:
            return None

        return pt_bl


    def find_bl(self, ctr_bl):

        for dy in range(-10, 10):
            for dx in range(-10, 10):
                snip = self.img[
                    ctr_bl.py + dy - 50 : ctr_bl.py + dy,
                    ctr_bl.px + dx
                ]
                if np.count_nonzero(snip > 0) > 5:
                    continue
                snip = self.img[
                    ctr_bl.py + dy,
                    ctr_bl.px + dx: ctr_bl.px + dx + 50
                ]
                if np.count_nonzero(snip > 0) < 5:
                    return sch.Point((ctr_bl.py + dy, ctr_bl.px + dx))
        snip = self.img[
            ctr_bl.py - 40 : ctr_bl.py + 40,
            ctr_bl.px - 40 : ctr_bl.px + 40,
        ]
        # snip *= -.25
        return None

    def is_bl(self, ctr_bl):

        snip2 = self.img [
            ctr_bl.py - 50 : ctr_bl.py,
            ctr_bl.px,
        ]
        if np.count_nonzero(snip2 > 0) > 0:
            return False

        snip2 = self.img [
            ctr_bl.py,
            ctr_bl.px : ctr_bl.px + 50,
        ]
        if np.count_nonzero(snip2 > 0) > 0:
            return False

        for dy in range(0, 20):
            snip2 = self.img[
                ctr_bl.py + dy,
                ctr_bl.px - 4 : ctr_bl.px + 4,
            ]
            if not np.count_nonzero(snip2 < 0):
                break

        if dy == 19:
            return False

        for dx in range(0, 20):
            snip2 = self.img[
                ctr_bl.py - 4 : ctr_bl.py + 4,
                ctr_bl.px - dx
            ]
            if not np.count_nonzero(snip2 < 0):
                break

        if dx == 19:
            return False

        return True

    def iter_bl(self):
        a =  imageio.imread(self.find_stepped_file("corr_h.png")).astype(float)
        b =  imageio.imread(self.find_stepped_file("corr_v.png")).astype(float)

        c = np.zeros(a.shape)

        c[sch.LINE_CORR:,:] += b[:-sch.LINE_CORR,:]
        c[:,:-sch.LINE_CORR] += a[:,sch.LINE_CORR:]

        print(np.amin(a), np.amin(b), np.amin(c), np.amax(a), np.amax(b), np.amax(c))

        c /= np.amax(c)

        ok = DebugSnippets()
        reject = DebugSnippets()
        for n in range(10000):
            ctr = np.unravel_index(np.argmax(c, axis=None), c.shape)

            ctr = sch.Point(ctr)
            merit = c[ctr.py,ctr.px]
            if merit < .9:
                break

            snippet = sch.snippet(self.img, *sch.window(ctr.pix, (60,60)))
            if not self.is_bl(ctr):
                snippet = np.array(snippet)
                reject.add(snippet)
            else:
                print("CNR", n, ctr, "%.3f" % c[ctr.py,ctr.px])
                snippet = np.array(snippet)
                #snippet[:10,:] *= -.5
                #snippet[-10:,:] *= -.5
                #snippet[:,:10] *= -.5
                #snippet[:,-10:] *= -.5
                ok.add(snippet)
                ctr.merit = merit
                yield ctr

            snippet =c[
                ctr.py - 20 : ctr.py + 20,
                ctr.px - 20 : ctr.px + 20,
            ]
            snippet *= 0
            snippet -= .5


        ok.dump(self.fn_pfx + "iter_bl_ok.png")
        reject.dump(self.fn_pfx + "iter_bl_reject.png")

if __name__ == "__main__":
    sheet = SchematicImage(sys.argv)
    sheet.write_image("proj50", sheet.proj50)
    sheet.write_components()
    sheet.write_interpolators()
    sheet.write_interpolated()
    sheet.write_landmarks()
