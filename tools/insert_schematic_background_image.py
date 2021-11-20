
import os
import glob
import random
import base64

from ImageProcessing.sexp import SExp
from ImageProcessing.page_numbers import page_number

MAGIC = "20011966"

def mkuuid():
    s = MAGIC
    s += "-%04x" % random.randint(0, 1<<16 - 1)
    s += "-%04x" % random.randint(0, 1<<16 - 1)
    s += "-%04x" % random.randint(0, 1<<16 - 1)
    s += "-%012x" % random.randint(0, 1<<48 - 1)
    return s

def main():
     for imgfile in glob.glob("BackgroundImages/*/*/projected_75_light.png"):
         i = imgfile.split("/")
         board = i[-3]
         sheet = i[-2]
         page_no = page_number(i[-3], i[-2])
         print(imgfile, "->", board, page_no)
         pcb = SExp()
         sch_name = "Schematics/%s/pg_%02d.kicad_sch" % (board, page_no)
         pcb.parse(open(sch_name).read())
         img = open(imgfile, "rb").read()
         i = SExp(name="image")
         i += SExp("at", "292.10", "189.23")
         i += SExp("scale", "4")
         i += SExp("uuid", mkuuid())
         i += SExp("data", base64.b64encode(img).decode("utf8"))
         pcb += i
         with open(sch_name + "_", "w") as file:
             for i in pcb.serialize():
                 file.write(i + "\n")
         os.rename(sch_name, sch_name + ".bak")
         os.rename(sch_name + "_", sch_name)


if __name__ == "__main__":
     main()
