
''' Template / 2D correlation matching '''

import os

import numpy as np

from scipy.signal import correlate2d

import schematics as sch

from debug_snippets import DebugSnippets

from rectangle import Rectangle

# import type_patterns

def string_2_template(source, reflect=False, black=-1, white=1):
    ''' convert an ascii-image to a real image '''
    lines = source.split("\n")
    if len(lines[0]) == 0:
        lines.pop(0)
    if len(lines[-1]) == 0:
        lines.pop(-1)

    if min(len(x) for x in lines) != max(len(x) for x in lines):
        for i in lines:
            print(len(i), i)
        assert min(len(x) for x in lines) == max(len(x) for x in lines)
    if reflect:
        lines += reversed(lines[:-1])
    dim_x = len(lines[0])
    dim_y = len(lines)
    # print("H", dim_y, "W", dim_x)
    img = np.zeros([dim_y, dim_x], dtype=np.float)
    for pix_y, i in enumerate(lines):
        for pix_x, j in enumerate(i):
            img[pix_y][pix_x] = {
                "#": black,
                " ": 0,
                "-": white,
            }[j]
    return img

def read_pgm(filename=None, string=None):
    assert filename or string
    assert not filename and string
    if filename:
        string = open(filename).read()
    tokens = []
    for i in string.split('\n'):
        if i and i[0] != '#':
            tokens += i.split()
    assert tokens.pop(0) == "P2"
    tokens = [int(x, 10) for x in tokens]
    dimx = tokens.pop(0)
    dimy = tokens.pop(0)
    _maxval = tokens.pop(0)
    img = np.zeros([dimy, dimx], dtype=np.float)
    for pix_y in range(dimy):
        img[pix_y, :] = tokens[:dimx]
        tokens = tokens[dimx:]
    img -= np.amin(img)
    img /= np.amax(img) * .5
    img -= 1
    return img

def find_in_snippet(target, template):
    weight = np.sum(template * template)
    corr = correlate2d(
        target,
        template,
        "same"
    )
    mask = np.zeros(target.shape, dtype=np.float)
    while True:
        ctr = np.unravel_index(np.argmax(corr, axis=None), corr.shape)
        yield (
            ctr,
            corr[ctr[0]][ctr[1]] / weight,
        )
        snip = sch.snippet(corr, *sch.window(ctr, template.shape))
        if 0 in snip.shape:
            snip = sch.snippet(corr, *sch.window(ctr, (10, 10)))
        snip *= 0
        corr[ctr[0]][ctr[1]] = 0

def find_in_window(target, template, pix, size):
    pix_tl, pix_br = sch.window(pix, size)
    snippet = sch.snippet(target, pix_tl, pix_br)
    weight = np.sum(template * template)
    if 0 in snippet.shape:
        sch.write_image_normalized(target, "/tmp/_.png")
    corr = correlate2d(
        snippet,
        template,
        "same"
    )
    while True:
        ctr = np.unravel_index(np.argmax(corr, axis=None), corr.shape)
        yield (
            (
                ctr[0] + pix_tl[0],
                ctr[1] + pix_tl[1]
            ),
            corr[ctr[0]][ctr[1]] / weight,
            snippet
        )
        corr[ctr[0]][ctr[1]] = 0

class Match():
    ''' A match '''

    def __init__(
        self,
        template,
        merit,
        order,
        pix,
        snippet,
        priv,
    ):
        self.template = template
        self.merit = merit
        self.order = order
        self.snippet = snippet
        self.pix = pix
        self.priv = priv

    def __lt__(self, other):
        return self.merit < other.merit

    def __str__(self):
        txt = "<M"
        txt += " %03d" % self.order
        txt += " %.3f" % self.merit
        txt += " %4d %4d" % self.pix
        return txt + ">"

    def __repr__(self):
        return self.__str__()

class TemplateMatcher():
    ''' Iterates over template matches in best->worst order '''

    def __init__(
        self,
        filename=None,
        template=None,
        name=None,
        validator=None,
    ):
        self.validator = validator
        self.name = name
        self.first_unmerit = None

        if filename:
            self.template = read_pgm(filename)
            if name is None:
                self.name = os.path.basename(filename).replace(".pgm", "")
        else:
            self.template = template

    def match(self, target_img, threshold, priv=None):
        ''' The iterator function '''

        weight = np.sum(self.template * self.template)
        corr = correlate2d(target_img, self.template, "same")
        corr /= weight
        # sch.write_image_normalized(corr, "/tmp/_coor.png")
        order = 0

        while True:
            order += 1

            ctr = np.unravel_index(np.argmax(corr, axis=None), corr.shape)

            pix_tl, pix_br = sch.window(ctr, self.template.shape)

            corr_snippet = sch.snippet(corr, pix_tl, pix_br)
            target_snippet = sch.snippet(target_img, pix_tl, pix_br)

            if corr_snippet.shape != self.template.shape:
                print("SNIPPET MISMATCH, corr", corr_snippet.shape, "template", self.template.shape)
                corr[ctr[0],ctr[1]] = 0
                continue

            merit = np.amax(corr_snippet)
            if merit < threshold:
                self.first_unmerit = merit
                break

            match = Match(
                self.template,
                merit,
                order,
                ctr,
                np.array(target_snippet),
                priv,
            )
            corr_snippet *= 0
            if not self.validator or self.validator(match):
                yield match

# def type_matcher(snippet, pix, window, type_list):
#     best_score = ("-", 0)
#     lsnippet = None
#     bsnippet = None
#     for name in type_list:
#         tpatt = getattr(type_patterns, name, None)
#         if not tpatt:
#             print("UNKNOWN PATTERN %s" % name)
#             continue
#         pattern = string_2_template(tpatt)
#         if 0 in pattern.shape:
#             print("BAD PATTERN %s" % name)
#             continue
#         for pix, score, snip2 in find_in_window(
#             snippet,
#             pattern,
#             pix,
#             window,
#         ):
#             lsnippet = snip2
#             if score > best_score[1]:
#                 best_score = (name, score)
#                 best_tl, best_br = sch.window(pix, pattern.shape)
#                 bsnippet = sch.snippet(snip2, best_tl, best_br)
#             break
# 
#     if best_score[1] < .17:
#          best_score = ("-", best_score[1])
# 
#     return best_score, lsnippet

class Template_Sheet(sch.Sheet):
    ''' ... '''

    def __init__(
        self,
        shape,
        argv,
        pattern_50,
        pattern_scan,
        threshold_50,
        threshold_scan,
        save_extra=.3,
        type_pix=None,
        type_window=None,
        type_list=None,
    ):
        super().__init__(argv)
        self.shape = shape
        self.debug = DebugSnippets()
        self.fout = None
        self.type_pix = type_pix
        self.type_window = type_window
        self.type_list = type_list

        self.template_50 = pattern_50
        self.write_image("template_50", self.template_50)

        self.template_scan = pattern_scan
        self.write_image("template_scan", self.template_scan)

        self.window_height = self.template_50.shape[0] / 50 + 2/50
        self.window_width = self.template_50.shape[1] / 50 + 2/50

        self.threshold_50 = threshold_50
        self.threshold_scan = threshold_scan

        self.hits = 0
        self.save_extra = int(save_extra * sch.APPROX_DPI)


    def validator(self, target):
        return None

    def tagger(self, order, save, save_tl, save_br):
        if self.type_list:
            print("71", save.shape, self.type_pix, self.type_window)
            type_pix_img = (
                save_tl[0] + self.type_pix[0],
                save_tl[1] + self.type_pix[1],
            )
            score,window_snippet = type_matcher(
                self.img,
                type_pix_img,
                self.type_window,
                self.type_list,
            )
            pfx = "match_%04d_%03d_" % (int(score[1] * 1000), order)
            if score[1] < .10:
                self.write_image(pfx + "blank.png", window_snippet)
            elif score[1] < .17:
                self.write_image(pfx + "none.png", window_snippet)
            return "%s,%.3f" % score
        return "-"

    def match(self):
        ''' Match patterns, report findings '''

        self.mask = np.zeros(self.img.shape, dtype=np.float)

        i = TemplateMatcher(
            template=self.template_50,
            name="or-ish",
        )

        for match in i.match(self.proj50,threshold=self.threshold_50):
            print("match50", match)
            self.debug.add(match.snippet)

            pic = sch.snippet(self.proj50, *sch.window(match.pix, (100, 100)))
            if 0 in pic.shape:
                pic = sch.snippet(self.proj50, *sch.window(match.pix, (50, 50)))
            print("PIC", pic.shape)
            self.debug.add(pic)

            self.study(
                (
                sch.INCH_HEIGHT - match.pix[0] / 50,
                match.pix[1] / 50
                ),
                match
            )
            self.debug.dump(self.fn_pfx + "coarse_%03d.png" % match.order)

        if self.hits:
            self.write_image("proj50", self.proj50)
            print("FOUND", self.hits)

    def study(self, inch, match):
        ''' A potential hit '''
        pix = self.inch2pix(inch)
        print("STUDY", inch, pix)
        for ctr, peak, snippet in find_in_window(
            self.img,
            self.template_scan,
            pix,
            (
                int(self.window_height * sch.APPROX_DPI),
                int(self.window_width * sch.APPROX_DPI),
            )
        ):
            print("CTR", ctr, peak, self.pix2inch(ctr), snippet.shape)
            self.debug.add(snippet)

            target_tl, target_br = sch.window(ctr, self.template_scan.shape)
            target = np.array(sch.snippet(self.img, target_tl, target_br))
            save = target

            mask = sch.snippet(self.mask, target_tl, target_br)
            if 0 in mask.shape:
                print("Bad mask shape",mask.shape)
                continue
                  
            if np.amax(mask) > 0:
                print("MASKED")
                return

            tag = "-" 

            if peak < self.threshold_scan:
                what = "miss"
            elif self.validator(target) is False:
                what = "rej"
            else:
                self.hits += 1
                what = "hit"
                inch_tl = self.pix2inch(target_tl)
                inch_br = self.pix2inch(target_br)
                hit_tl = sch.inch2proj(inch_tl)
                hit_br = sch.inch2proj(inch_br)
                snip = sch.snippet(self.proj50, hit_tl, hit_br)
                snip *= -.25
                mask += 1
                save_tl = (target_tl[0] - self.save_extra, target_tl[1] - self.save_extra)
                save_br = (target_br[0] + self.save_extra, target_br[1] + self.save_extra)
                save = np.array(sch.snippet(self.img, save_tl, save_br))
                tag = self.tagger(match.order, save, save_tl, save_br)

            self.debug.add(target)

            filename = self.fn_pfx + what + "_%04d_" % int(1000*peak)
            filename += self.board + "_" + self.sheet
            filename += "_%03d.png" % match.order

            if not self.fout:
                self.fout = open(self.fn_pfx + "findings.txt", "w")
            self.fout.write("%4s" % what)
            self.fout.write(" %-12s" % self.shape)
            self.fout.write(" %-12s" % tag)
            self.fout.write(" %3d" % match.order)
            self.fout.write(" %6.3f %6.3f" % inch)
            self.fout.write(" -")
            self.fout.write(" %6.3f" % match.merit)
            self.fout.write(" %6.3f %6.3f" % self.pix2inch(ctr))
            self.fout.write(" %6.3f" % peak)
            self.fout.write(" %4d %4d" % ctr)
            self.fout.write(" %4d %4d" % (pix[0] - ctr[0], pix[1] - ctr[1]))
            self.fout.write(" " + filename)
            self.fout.write(" " + str(match) + "\n")
            self.fout.flush()
            sch.write_image_normalized(save, filename)
            break

class Template_Rectangle_Sheet(Template_Sheet):

    SYMBOL = None

    def study(self, inch, match):
        dbg = DebugSnippets()
        print("STUD", inch, match)
        dbg.add(match.snippet)
        pix = self.inch2pix(inch)

        for corner, dy, dx, box in self.CORNERS:
            cnr = sch.Point((pix[0] + dy, pix[1] + dx))
            sch.add_small_marker(self.img, *cnr.pix)
            setattr(self, "cnr_" + corner, cnr)
                
        rect = Rectangle(self.cnr_tl, self.cnr_tr, self.cnr_bl, self.cnr_br)
        rect.align_to_pins(self)
                
        fn = self.fn_pfx + "rectangle_%03d.png" % match.order
            
        snippet = sch.snippet(
            self.img,
            (rect.tl.pix[0] - 100, rect.tl.pix[1] - 100),
            (rect.br.pix[0] + 100, rect.br.pix[1] + 100),
        )
        sch.write_image_normalized(snippet, fn)
            
        chip = self.bom.add_chip(rect, fn)
        if self.SYMBOL:
            chip.symbol = self.SYMBOL

        dbg.add(snippet)

        print("tl", rect.tl)
        print("br", rect.br)
        rect.tl.proj_inch(self)
        print("tl2", rect.tl)
        rect.br.proj_inch(self)
        print("br2", rect.br)
        proj_tl = sch.inch2proj(rect.tl.inch)
        proj_br = sch.inch2proj(rect.br.inch)
        snippet = sch.snippet(self.proj50, proj_tl, proj_br)
        dbg.add(snippet)
        snippet *= -.25
        dbg.add(snippet)
            
        dbg.dump(self.fn_pfx + "study_%03d.png" % match.order)
