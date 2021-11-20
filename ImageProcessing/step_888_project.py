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
    proj_height = int(sch.INCH_HEIGHT * dpi)
    proj_width = int(sch.INCH_WIDTH * dpi)
    desired_shape = (proj_height, proj_width)
    filename1 = sheet.dstdir + "projected_%d.png" % dpi
    filename2 = sheet.dstdir + "projected_%d_light.png" % dpi
    filename3 = sheet.dstdir + "projected_%d_grid.png" % dpi
    try:
        i = imageio.imread(filename1).shape
        print(i)
        j = imageio.imread(filename2).shape
        print(j)
        if i == desired_shape and j == desired_shape:
            return
    except Exception as e:
        print("E", e)
        pass
    sheet.load_raw_image()
    img = sheet.project(dpi)
    sch.write_image_normalized(img, filename1, bits=4)
    img2 = np.array(img)
    for px in range(0, img2.shape[1], dpi // 5):
       for py in range(img2.shape[0]):
           img2[py][px] *= .5
    for py in range(0, img2.shape[0], dpi // 5):
       for px in range(img2.shape[1]):
           img2[py][px] *= .5
    sch.write_image_normalized(img2, filename3, bits=4)
    if dpi == 75:
        img -= np.amin(img)
        img *= 63. / np.amax(img)
        img += 192
        img = img.astype(np.uint8)
        imageio.imwrite(filename2, img, bits=4)

if __name__ == "__main__":
    do_project(sys.argv, 75)
    #do_project(sys.argv, 200)
    #do_project(sys.argv, 150)
    #do_project(sys.argv, 300)
