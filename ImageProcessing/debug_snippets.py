#!/usr/local/bin/python3.8
#
# NB: We strive to use y-x coordinate order to match numpy's convention

''' ... '''

import imageio

import numpy as np

class DebugSnippets():
    ''' A crude facilty for dumping debug-snippets '''

    def __init__(self):
        self.reset()

    def reset(self):
        self.rows = [[]]
        self.count = 0
        self.cur_x = 0

    def add(self, img):
        ''' Add a snippet to the collection '''
        if 0 in img.shape:
            return
        if self.cur_x + 2 + img.shape[1] > 1800:
            self.newline()
        self.rows[-1].append(np.array(img))
        self.count += 1
        self.cur_x += 2 + img.shape[1]

    def newline(self):
        self.rows.append([])
        self.cur_x = 0

    def dump(self, filename, **kwargs):
        ''' Create an image with all the collected snippets '''
        if not self.count:
            return
        height = 0
        width = 0
        for row in self.rows:
            if not row:
                continue
            row_height = 2 + max(i.shape[0] for i in row)
            row_width = sum(2 + i.shape[1] for i in row)
            height += row_height
            width = max(width, row_width)

        img = np.zeros([height, width])
        pix_y = 1
        for row in self.rows:
            pix_x = 1
            if not row:
                continue
            dy = 0
            for snippet in row:
                pix_height, pix_width = snippet.shape
                img[pix_y:pix_y+pix_height, pix_x:pix_x+pix_width] = snippet
                pix_x += pix_width + 2
                dy = max(dy, pix_height)
            pix_y += dy + 2

        img -= np.amin(img)
        img *= 255. / np.amax(img)
        imageio.imwrite(filename, img.astype(np.uint8), **kwargs)
        self.reset()
