#!/usr/local/bin/python3.8
#
# NB: We strive to use y-x coordinate order to match numpy's convention

'''
'''

import sys
import os

import numpy as np

import imageio

import schematics as sch

import components

from Chipdesc import chipdict

from debug_snippets import DebugSnippets

from scipy.signal import correlate2d

class Sheet_360(sch.Sheet):
    ''' ... '''

    def __init__(self, argv):
        super().__init__(argv)
        self.load_raw_image()
        self.load_components()

        self.pat_non = imageio.imread("step_360_non.png").astype(float)
        self.pat_non -= np.amin(self.pat_non)
        self.pat_non /= .5 * np.amax(self.pat_non)
        self.pat_non -= 1
        self.w_non = np.sum(self.pat_non * self.pat_non)

        self.pat_inv = imageio.imread("step_360_inv.png").astype(float)
        self.pat_inv -= np.amin(self.pat_inv)
        self.pat_inv /= .5 * np.amax(self.pat_inv)
        self.pat_inv -= 1
        self.w_inv = np.sum(self.pat_inv * self.pat_inv)

    def ident_pin(self, snippet):

        nzero = 0
        for y in range(snippet.shape[0]):
            if not np.count_nonzero(snippet[y,5:-5] < -.1):
                print("ZERO", y)
                nzero += 1
                if nzero > 2:
                   return '_'

        coor_non = correlate2d(snippet, self.pat_non, "same")
        coor_inv = correlate2d(snippet, self.pat_inv, "same")
        merit_non = np.amax(coor_non) / self.w_non
        merit_inv = np.amax(coor_inv) / self.w_inv

        print(
            "CORR",
            "%7.3f" % merit_non,
            "%7.3f" % merit_inv,
        )

        if merit_inv > .50 and (merit_inv > merit_non or merit_non < .7):
            return 'o'

        if merit_non < .65 and merit_inv < .4:
            return '_'

        for x in range(4, 26):
            i = np.count_nonzero(snippet[:,x] < -.1)
            if i >= snippet.shape[0] - 3:
                return 'I'
        return '?'

    def signatures(self):
        dbg = DebugSnippets()
        for n, comp in enumerate(self.bom):
            if not isinstance(comp, components.Chip):
                continue
            if comp.symbol:
                continue
            print(comp)

            top = ""
            for j in comp.top_side_pins(self):
                 j = np.rot90(j, 2)
                 top += self.ident_pin(j)
                 if top[-1] != '?':
                     j = np.array(j) * .5
                 dbg.add(j)
                 print("T", top[-1])
            dbg.newline()

            left = ""
            right = ""
            for j, k in zip(comp.left_side_pins(self), comp.right_side_pins(self)):
                 j = np.rot90(j, 1)
                 k = np.rot90(k, 3)
                 left += self.ident_pin(j)
                 if left[-1] != '?':
                     j = np.array(j) * .5
                 dbg.add(j)
                 print("L", left[-1])
                 right += self.ident_pin(k)
                 if right[-1] != '?':
                     k = np.array(k) * .5
                 dbg.add(k)
                 dbg.newline()
                 print("R", right[-1])

            print("l", left)
            print("r", right)
            while left and left[0] == '_' and right[0] == '_':
                 left = left[1:]
                 right = right[1:]
            while left and left[-1] == '_' and right[-1] == '_':
                 left = left[:-1]
                 right = right[:-1]
            print("L", left)
            print("R", right)
                
            bottom = ""
            for j in comp.bottom_side_pins(self):
                 j = np.rot90(j, 0)
                 bottom += self.ident_pin(j)
                 if bottom[-1] != '?':
                     j = np.array(j) * .5
                 dbg.add(j)
                 print("B", bottom[-1])

            print("t", top)
            print("b", bottom)
            while top and top[0] == '_' and bottom[0] == '_':
                 top = top[1:]
                 bottom = bottom[1:]
            while top and top[-1] == '_' and bottom[-1] == '_':
                 top = top[:-1]
                 bottom = bottom[:-1]
            print("T", top)
            print("B", bottom)
                
            comp.signature = "L" + left + "R" + right + "T" + top + "B" + bottom
            if '?' in comp.signature:
                dbg.dump(self.fn_pfx + "sig_%d.png" % n)
            else:
                dbg.reset()
            chip = chipdict.CHIPSIGS.get(comp.signature)
            if chip:
                print("COMP", comp.signature, chip)
                comp.symbol = chip[0].symbol_name

            if not comp.symbol:
                chip = chipdict.CHIPSIGS.get(comp.signature.replace('?', 'o'))
                if chip:
                    print("FALLBACK", comp.signature, chip)
                    comp.symbol = chip[0].symbol_name

            if not comp.symbol:
                print("UNKNOWN", comp.signature)
          

    def debug_pins(self):
        dbg = DebugSnippets()
        for n, i in enumerate(self.bom):
            if not isinstance(i, components.Chip):
                continue
            print(i)
            for j in i.top_side_pins(self):
                dbg.add(j)
            dbg.newline()
            for j, k in zip(i.left_side_pins(self), i.right_side_pins(self)):
                dbg.add(j)
                dbg.add(k)
                dbg.newline()
            for j in i.bottom_side_pins(self):
                dbg.add(j)
            dbg.dump(self.fn_pfx + "pins_%d.png" % n)

if __name__ == "__main__":
    sheet = Sheet_360(sys.argv)
    sheet.debug_pins()
    sheet.signatures()
    sheet.write_components()
