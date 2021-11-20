#!/usr/local/bin/python3.8

'''
   Find a corner in a specified box
'''

import numpy as np

import schematics as sch

CORNER_BOX = 50

class Corner():
    ''' A line turning a corner '''

    def __init__(self, img, pix, name, debug=None, width=3, box=CORNER_BOX):
        self.name = name
        self.xyh = sch.XY_Histogram(img, *pix, box, minwidth=width, gate=.80)
        self.arg_pix = pix
        # print("CORNER", name, self.xyh)
        self.pix = (self.xyh.val_y, self.xyh.val_x)
        self.snippet = self.xyh.snippet
        if debug:
            debug.add(self.snippet)

        box2 = box // 2
        band = width * 2

        snippet = img[
            self.pix[0] - band : self.pix[0] + band,
            self.pix[1] - box2 : self.pix[1] - band,
        ]
        if debug:
            debug.add(snippet)
        self.left = 1 + np.count_nonzero(snippet < 0)

        snippet = img[
            self.pix[0] - band : self.pix[0] + band,
            self.pix[1] + band : self.pix[1] + box2,
        ]
        if debug:
            debug.add(snippet)
        self.right = 1 + np.count_nonzero(snippet < 0)

        snippet = img[
            self.pix[0] - box2 : self.pix[0] - band,
            self.pix[1] - band : self.pix[1] + band,
        ]
        if debug:
            debug.add(snippet)
        self.top = 1 + np.count_nonzero(snippet < 0)

        snippet = img[
            self.pix[0] + band : self.pix[0] + box2,
            self.pix[1] - band : self.pix[1] + band,
        ]
        if debug:
            debug.add(snippet)
        self.bottom = 1 + np.count_nonzero(snippet < 0)

        self.left_right_balance = min(self.left, self.right) / max(self.left, self.right)
        self.top_bottom_balance = min(self.top, self.bottom) / max(self.top, self.bottom)

        if self.left_right_balance > .25:
            self.pix = (self.pix[0], None)
        if self.top_bottom_balance > .25:
            self.pix = (None, self.pix[1])

        if None in self.pix:
             self.which = "not"
        elif self.is_b_l():
             self.which = "bl"
        elif self.is_b_r():
             self.which = "br"
        elif self.is_t_r():
             self.which = "tr"
        elif self.is_t_l():
             self.which = "tl"
        else:
             self.which = "not"

        if False:
            print("LRTB", self)

    def __lt__(self, other):
        if self.pix[0] != other.pix[0]:
            return self.pix[0] < other.pix[0]
        return self.pix[1] < other.pix[1]

    def __str__(self):
        return " ".join([
            "<C",
            self.name,
            self.which,
            "L %4d" % self.left,
            "R %4d" % self.right,
            "T %4d" % self.top,
            "B %4d" % self.bottom,
            "Qlr %5.2f" % self.left_right_balance,
            "Qtb %5.2f" % self.top_bottom_balance,
            "dy %5g" % (self.xyh.val_y - self.arg_pix[0]),
            "dx %5g" % (self.xyh.val_x - self.arg_pix[1]),
            ">"        
        ])
 

    def is_b_l(self):
        return self.top > self.bottom and self.right > self.left

    def is_b_r(self):
        return self.top > self.bottom and self.right < self.left

    def is_t_l(self):
        return self.top < self.bottom and self.right > self.left

    def is_t_r(self):
        return self.top < self.bottom and self.right < self.left

