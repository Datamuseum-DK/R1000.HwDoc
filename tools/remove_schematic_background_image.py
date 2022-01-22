
import os
import glob

from ImageProcessing import sexp

def main():
     for fname in sorted(glob.glob("Schematics/*/*.kicad_sch")):
         print(fname)
         pcb = sexp.SExp(None)
         pcb.parse(open(fname).read())
         for i in pcb:
             if i.name == "image":
                 pcb -= i
                 break
         with open(fname + "_", "w") as file:
             for i in pcb.serialize():
                 file.write(i + "\n")
         os.rename(fname, fname + ".bak")
         os.rename(fname + "_", fname)


if __name__ == "__main__":
     main()
