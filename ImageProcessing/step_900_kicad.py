#!/usr/local/bin/python3.8
#
# NB: We strive to use y-x coordinate order to match numpy's convention

''' STEP 900: Create a KiCad project for this sheet '''

import sys
import os
import time

import schematics as sch

import shutil

class Sheet_900(sch.Sheet):

    def __init__(self, *args, **kvargs):
        super().__init__(*args, **kvargs)
        self.ki_proj = self.board + "_" + self.sheet
        self.ki_dir = self.dstdir + "kicad_" + self.ki_proj + "/"
        self.ki_pfx = self.ki_dir + self.ki_proj

        self.seq = int(time.time())

        print("PFX", self.ki_pfx)
        try:
            shutil.rmtree(self.ki_dir)
        except FileNotFoundError:
            pass
        os.mkdir(self.ki_dir)

        self.mk_dummy_pcb_file()
        self.mk_pro_file()
        self.mk_wks_file()
        self.mk_symlib_file()
        shutil.copy("KiCadFiles/R1000.kicad_sym", self.ki_dir)
        self.mk_sch_preamble()

        for findings in (
            "210_findings.txt",
            "211_findings.txt",
            "212_findings.txt",
            "220_findings.txt",
            "230_findings.txt",
            "240_findings.txt",
            "350_findings.txt",
        ):
            try:
                file = open(self.dstdir + findings)
            except FileNotFoundError:
                continue
            self.add_sch_findings(file)
        self.mk_sch_image()
        self.mk_sch_postamble()

    def timestamp(self):
        self.seq += 1
        return "%08X" % self.seq

    def mk_dummy_pcb_file(self):
        with open(self.ki_pfx + ".kicad_pcb", "w") as file:
            file.write('''(kicad_pcb (version 4) (host kicad "dummy file") )\n''')

    def mk_pro_file(self):
        with open(self.ki_pfx + ".pro", "w") as file:
            for i in (
                '''update=22/05/2015 07:44:53''',
                '''version=1''',
                '''last_client=kicad''',
                '''[general]''',
                '''version=1''',
                '''RootSch=''',
                '''BoardNm=''',
                '''[pcbnew]''',
                '''version=1''',
                '''LastNetListRead=''',
                '''UseCmpFile=1''',
                '''PadDrill=0.600000000000''',
                '''PadDrillOvalY=0.600000000000''',
                '''PadSizeH=1.500000000000''',
                '''PadSizeV=1.500000000000''',
                '''PcbTextSizeV=1.500000000000''',
                '''PcbTextSizeH=1.500000000000''',
                '''PcbTextThickness=0.300000000000''',
                '''ModuleTextSizeV=1.000000000000''',
                '''ModuleTextSizeH=1.000000000000''',
                '''ModuleTextSizeThickness=0.150000000000''',
                '''SolderMaskClearance=0.000000000000''',
                '''SolderMaskMinWidth=0.000000000000''',
                '''DrawSegmentWidth=0.200000000000''',
                '''BoardOutlineThickness=0.100000000000''',
                '''ModuleOutlineThickness=0.150000000000''',
                '''[cvpcb]''',
                '''version=1''',
                '''NetIExt=net''',
                '''[eeschema]''',
                '''version=1''',
                '''LibDir=''',
                '''[eeschema/libraries]''',
                '''[schematic_editor]''',
                '''version=1''',
                '''PageLayoutDescrFile=R1000.frame.kicad_wks''',
            ):
                file.write(i + "\n")

    def mk_wks_file(self):
        with open(self.ki_dir + "R1000.frame.kicad_wks", "w") as file:
            for i in (
                '''(page_layout''',
                '''  (setup (textsize 1.5 1.5)(linewidth 0.15)(textlinewidth 0.15)''',
                '''  (left_margin 0)(right_margin 0)(top_margin 0)(bottom_margin 0))''',
                '''  (line (name segm1:Line) (start 25.4 0 lbcorner) (end 25.4 5.08 lbcorner) (repeat 22) (incrx 25.4))''',
                '''  (line (name segm2:Line) (start 25 0 ltcorner) (end 25 5.08 ltcorner) (repeat 22) (incrx 25.4))''',
                '''  (line (name segm3:Line) (start 0 25.4) (end 5.08 25.4) (repeat 14) (incry 25.4))''',
                '''  (line (name segm4:Line) (start 0 25.4 lbcorner) (end 5.08 25.4 lbcorner) (repeat 14) (incry 25.4))''',
                '''  (rect (name rect1:Rect) (start 5.08 5.08 lbcorner) (end 5.08 5.08 rtcorner))''',
                '''  (rect (name rect2:Rect) (start 0 0 lbcorner) (end 0 0 rtcorner) (linewidth 0.2))''',
                '''  (tbtext "THIS DOCUMENT CONTAINS PROPRIETARY INFORMA-\\nTION DESIGNATED \\"TRADESECRET\\" AND CONFIDEN-\\nTIAL BY RATIONAL. IT IS NOT TO BE COPIED OR\\nDISTRIBUTED WITHOUT THE WRITTEN CONSENT OF\\nAN OFFICER OF RATIONAL. POSSECESSION OR RE-\\nCEIPT OF THIS DOCUMENT DOES NOT CONVEY ANY\\nRIGHT TO REPRODUCE OR DISCLOSE ITS CONTENTS\\nOR TO MANUFACTURE, USE OR SELL ANYTHING\\nBASED ON OR INCORPORATING THE CONCEPTS OR\\nDETAILS DISCLOSED BY IT WITHOUT THE WRITTEN\\nCONSENT OF AN OFFICER OF RATIONAL" (name text1:Text) (pos 113.215 99) (font (size 2.54 2.54)) (justify top))''',
                '''  (rect (name rect3:Rect) (start 7.68 7.68) (end 116.84 104.14))''',
                '''  (tbtext "Title: %T" (name text2:Text) (pos 116.002 16.007) (font (size 6 6)))''',
                ''')''',
            ):
                file.write(i + "\n")

    def mk_symlib_file(self):
        with open(self.ki_dir + "sym-lib-table", "w") as file:
            for i in (
                '''(sym_lib_table''',
                '''  (lib (name "R1000")(type "KiCad")(uri "${KIPRJMOD}/R1000.kicad_sym")(options "")(descr ""))''',
                ''')''',
            ):
                file.write(i + "\n")

    def mk_sch_preamble(self):
        with open(self.ki_pfx + ".sch", "w") as file:
            for i in (
                '''EESchema Schematic File Version 4''',
                '''EELAYER 30 0''',
                '''EELAYER END''',
                '$Descr User %.0f %.0f' % (1000 * sch.INCH_WIDTH, 1000 * sch.INCH_HEIGHT),
                '''encoding utf-8''',
                '''Sheet 1 1''',
                'Title "%s %s"' % (self.board, self.sheet),
                '''$EndDescr''',
            ):
                file.write(i + "\n")

    def mk_sch_image(self):
        try:
            fi = open(self.dstdir + "projected_75_light.png", "rb")
        except FileNotFoundError:
            return
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

    def mk_sch_postamble(self):
        with open(self.ki_pfx + ".sch", "a") as file:
            file.write("$EndSCHEMATC\n")

    def add_sch_findings(self, infile):
        n = int(time.time())
        for i in infile:
            spec = i.split()
            if spec[0] != "hit":
                continue
            kind = spec[1].split(",")[0]
            if False:
                kicad_y = round(20 * (sch.INCH_HEIGHT - float(spec[4])))
                kicad_x = round(20 * float(spec[5]))
                kicad_y = "%.0f" % (kicad_y * 50)
                kicad_x = "%.0f" % (kicad_x * 50)
            else:
                kicad_y = round(10 * (sch.INCH_HEIGHT - float(spec[4])))
                kicad_x = round(10 * float(spec[5]))
                kicad_y = "%.0f" % (kicad_y * 100)
                kicad_x = "%.0f" % (kicad_x * 100)
            if kind in (
                "orish",
                "andish",
                "bufish",
                "rectangle",
            ):
                self.add_comp(kicad_y, kicad_x, spec)
                continue
            if kind in (
                "rflag",
                "plane",
            ):
                self.add_flag(kicad_y, kicad_x, spec)
                continue
            print("UNKNOWN SPEC", spec)

    def add_flag(self, kicad_y, kicad_x, spec):
        file = open(self.ki_pfx + ".sch", "a")
        o = int(spec[3])
        file.write('Text GLabel %s %s 0    75   Input ~ 0\n' % (kicad_x, kicad_y))
        if "plane" in spec[1]:
            file.write('Plane_%03d\n' % o)
        else:
            file.write('Flag_%03d\n' % o)

    def add_comp(self, kicad_y, kicad_x, spec):
        file = open(self.ki_pfx + ".sch", "a")
        if spec[2][0] != "F":
            return
        chip = spec[2].split(",")[0]
        o = float(spec[3])
        file.write("$Comp\n")
        xlat = {
            "andish-F02": "F02N"
        }.get(spec[1] + "-" + chip)
        if xlat:
            file.write("L R1000:" + xlat + " U?\n")
        else:
            file.write("L R1000:" + chip + " U?\n")
        file.write("U 1 1 %s\n" % self.timestamp())
        file.write("P %s %s\n" % (kicad_x, kicad_y))
        file.write('F 1 "%s" H %s %s 100  0000 C CNN\n' % (chip, kicad_x, kicad_y))
        file.write("$EndComp\n")


if __name__ == "__main__":
    sheet = Sheet_900(sys.argv)
