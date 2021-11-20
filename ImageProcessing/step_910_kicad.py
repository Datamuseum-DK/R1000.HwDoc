#!/usr/local/bin/python3.8
#
# NB: We strive to use y-x coordinate order to match numpy's convention

''' STEP 910: Add/Update background picture '''

import sys
import os
import time
import base64

import schematics as sch

import shutil

from sexp import SExp

from make_kicad_projects import mkuuid

class Sheet_910(sch.Sheet):

    def __init__(self, *args, **kvargs):
        super().__init__(*args, **kvargs)
        self.ki_proj = "Proj/" + self.board

        self.sch = SExp()
        self.sch.parse(open(self.sch_file, "r").read())

        for n, i in enumerate(self.sch):
            if i.name == "image":
                self.sch.members.pop(n)
                break

        img = self.mk_sch_image()
        if not img:
             return
        print("Adding image", img)
        self.sch += img

        with open(self.sch_file + "_", "w") as file:
             for i in self.sch.serialize():
                 file.write(i + "\n")
        os.rename(self.sch_file + "_", self.sch_file)

    def mk_sch_image(self):
        try:
            img_bits = open(self.dstdir + "projected_75_light.png", "rb").read()
        except FileNotFoundError:
            return None

        img = SExp("image")
        img += SExp("at", "%.2f" % (.5 * sch.INCH_WIDTH * 25.4), "%.2f" % (.5 * sch.INCH_HEIGHT * 25.4))
        img += SExp("scale", "4")
        img += SExp("uuid", mkuuid())
        img += SExp("data", base64.b64encode(img_bits).decode('ASCII'))
        print(img.members[-1])

        return img

        file = open(self.ki_pfx + ".sch", "a")
        file.write("$Bitmap\n")
        file.write("Pos 11500 7450\n")
        file.write("Scale 4.000000\n")
        file.write("Data\n")
        while True:
             a = fi.read(32)
             file.write(" ".join("%02X" % i for i in a) + "\n")
             if len(a) != 32:
                  break
        file.write("EndData\n")
        file.write("$EndBitmap\n")



if __name__ == "__main__":
    sheet = Sheet_910(sys.argv)
