#!/usr/local/bin/python3.8
#
# NB: We strive to use y-x coordinate order to match numpy's convention


''' Step 888: Create a 75, 150 and 300 DPI projection '''

import sys

import numpy as np

import imageio

import schematics as sch

def do_project(argv, dpi):
    sheet = sch.Sheet(argv)
    sheet.pad_landmarks()
    proj_height = int(sch.INCH_HEIGHT * dpi)
    proj_width = int(sch.INCH_WIDTH * dpi)
    desired_shape = (proj_height, proj_width)
    filename1 = sheet.dstdir + "projected_%d.png" % dpi
    try:
        i = imageio.imread(filename1).shape
        print(i)
        if i == desired_shape:
            return
    except Exception as e:
        print("E", e)
        pass
    sheet.load_raw_image()
    img = sheet.project(dpi)
    sch.write_image_normalized(img, filename1, bits=4)

if __name__ == "__main__":
    do_project(sys.argv, 75)
    do_project(sys.argv, 100)
    do_project(sys.argv, 150)
    do_project(sys.argv, 200)
    do_project(sys.argv, 300)
