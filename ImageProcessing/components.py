
import numpy as np

from rectangle import Rectangle

class Component():
    ''' ... '''

    def __init__(self, kind):
        self.kind = kind

class Corner():
    ''' ... '''

    def __init__(self, pix):
        self.pix = pix

class Chip(Component):
    ''' ... '''

    def __init__(self, rectangle=None, image=None, spec=None):
        super().__init__("chip")
        self.rectangle = rectangle
        self.image = image
        self.signature = None
        self.symbol = None

        if spec is None:
            return
        spec.pop(0)
        while spec:
            tag = spec.pop(0)
            if tag == "tl":
                y = float(spec.pop(0))
                x = float(spec.pop(0))
                tl = Corner((y, x))
            elif tag == "tr":
                y = float(spec.pop(0))
                x = float(spec.pop(0))
                tr = Corner((y, x))
            elif tag == "bl":
                y = float(spec.pop(0))
                x = float(spec.pop(0))
                bl = Corner((y, x))
            elif tag == "br":
                y = float(spec.pop(0))
                x = float(spec.pop(0))
                br = Corner((y, x))
                self.rectangle = Rectangle(tl, tr, bl, br)
            elif tag == "img":
                self.image = spec.pop(0)
            elif tag == "sig":
                self.signature = spec.pop(0)
            elif tag == "symbol":
                self.symbol = spec.pop(0)
            else:
                raise Exception("Component 'chip' Syntax Error")

    def __str__(self):
        i = [self.kind]
        for c in ("tl", "tr", "bl", "br"):
            j = getattr(self.rectangle, c)
            i.append(c)
            i.append(str(j.pix[0]))
            i.append(str(j.pix[1]))
        i.append("img")
        i.append(self.image)
        if self.signature:
            i.append("sig")
            i.append(self.signature)
        if self.symbol:
            i.append("symbol")
            i.append(self.symbol)
        return " ".join(i)

    PIN_WIDTH = 15
    PIN_LENGTH = 50

    def top_side_pins(self, sheet):
        tl = sheet.pix2inch(self.rectangle.tl.pix)
        tr = sheet.pix2inch(self.rectangle.tr.pix)
        x = round(tl[1], 1)
        while x < tr[1]:
            x += .1
            pix = sheet.inch2pix((tl[0], x))
            while True:
                snippet = sheet.img[
                    pix[0],
                    pix[1] - self.PIN_WIDTH : pix[1] + self.PIN_WIDTH,
                ]
                if np.amax(snippet) > 0:
                    break
                pix = (pix[0] - 1, pix[1])
            snippet = sheet.img[
                pix[0] - self.PIN_LENGTH : pix[0],
                pix[1] - self.PIN_WIDTH : pix[1] + self.PIN_WIDTH,
            ]
            yield snippet

    def bottom_side_pins(self, sheet):
        tl = sheet.pix2inch(self.rectangle.tl.pix)
        tr = sheet.pix2inch(self.rectangle.tr.pix)
        bl = sheet.pix2inch(self.rectangle.bl.pix)
        br = sheet.pix2inch(self.rectangle.br.pix)
        x = round(tl[1], 1)
        while x < tr[1]:
            x += .1
            pix = sheet.inch2pix((bl[0], x))
            while True:
                snippet = sheet.img[
                    pix[0],
                    pix[1] - self.PIN_WIDTH : pix[1] + self.PIN_WIDTH,
                ]
                if np.amax(snippet) > 0:
                    break
                pix = (pix[0] + 1, pix[1])
            snippet = sheet.img[
                pix[0] : pix[0] + self.PIN_LENGTH,
                pix[1] - self.PIN_WIDTH : pix[1] + self.PIN_WIDTH,
            ]
            yield snippet

    def left_side_pins(self, sheet):
        tl = sheet.pix2inch(self.rectangle.tl.pix)
        bl = sheet.pix2inch(self.rectangle.bl.pix)
        y = round(tl[0], 1)
        while y > bl[0]:
            y -= .1
            pix = sheet.inch2pix((y, tl[1]))
            while True:
                snippet = sheet.img[
                    pix[0] - self.PIN_WIDTH : pix[0] + self.PIN_WIDTH,
                    pix[1],
                ]
                if np.amax(snippet) > 0:
                    break
                pix = (pix[0], pix[1] - 1)
            snippet = sheet.img[
                pix[0] - self.PIN_WIDTH : pix[0] + self.PIN_WIDTH,
                pix[1] - self.PIN_LENGTH : pix[1],
            ]
            yield snippet

    def right_side_pins(self, sheet):
        tl = sheet.pix2inch(self.rectangle.tl.pix)
        bl = sheet.pix2inch(self.rectangle.bl.pix)
        tr = sheet.pix2inch(self.rectangle.tr.pix)
        br = sheet.pix2inch(self.rectangle.br.pix)
        y = round(tl[0], 1)
        while y > bl[0]:
            y -= .1
            pix = sheet.inch2pix((y, tr[1]))
            while True:
                snippet = sheet.img[
                    pix[0] - self.PIN_WIDTH : pix[0] + self.PIN_WIDTH,
                    pix[1],
                ]
                if np.amax(snippet) > 0:
                    break
                pix = (pix[0], pix[1] + 1)
            snippet = sheet.img[
                pix[0] - self.PIN_WIDTH : pix[0] + self.PIN_WIDTH,
                pix[1] : pix[1] + self.PIN_LENGTH,
            ]
            yield snippet

class BOM():
    ''' ... '''
    def __init__(self):
        self.bomlist = []

    def __iter__(self):
        yield from self.bomlist

    def add_chip(self, rectangle, image):
        retval = Chip(rectangle, image)
        self.bomlist.append(retval)
        return retval

    def load_from_file(self, filename):
        for i in open(filename):
            j = i.split()
            if j[0] == "chip":
                self.bomlist.append(Chip(spec=j))
            else:
                raise Exception("Component Syntax Error")

    def write_to_file(self, filename):
        file = open(filename, "w")
        for i in self.bomlist:
            file.write(str(i) + "\n")
