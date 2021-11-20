
import glob
import os

def gen_makefile():

    fo = open("Makefile", "w")
    fo.write("default: all\n")
    for img in sorted(glob.glob("../[A-Z]*/rawimg/*.pgm")):

        fo.write("\n")

        brd = img.split('/')[1]
        try:
            os.mkdir(brd)
        except FileExistsError:
            pass

        nbr = img.split('.')[-2]
        nbr = nbr.split('-')[-1]

        wd = brd + "/" + nbr

        prev_ok = ""
        for step_prog in sorted(glob.glob("step*.py")):
            step_no = step_prog.split("step_")[1]
            step_no = step_no.split("_")[0]
            step_no = int(step_no, 10)
            ok = wd + "/%03d_ok" % step_no
            log = wd + "/%03d_log" % step_no
            err = wd + "/%03d_error" % step_no
            fo.write("\n")
            fo.write(ok + ": " + step_prog)
            if prev_ok:
                fo.write(" " + prev_ok)
            fo.write("\n")

            if not prev_ok:
                fo.write("\t@mkdir -p " + wd + "\n")
                fo.write("\t@rm -rf " + wd + "/*\n")
            else:
                fo.write("\t@rm -f " + wd + "/%03d_*\n" % step_no)
            fo.write("\t@echo " + step_prog + " " + brd + " " + nbr + "\n")
            fo.write("\t@(python3 -u " + step_prog + " " + brd + " " + nbr)
            fo.write(" > " + log + " 2>&1 && \\\n")
            fo.write("\t    mv " + log + " " + ok)
            fo.write(") || (mv " + log + " " + err + " && false)")
            fo.write("\n")
            prev_ok = ok

        fo.write("ALLTGT += " + prev_ok + "\n")

        fo.write("\n" + brd + "_" + nbr + ": " + prev_ok + "\n")
        fo.write("\t@${MAKE} " + prev_ok + "|| cat " + brd + "/" + nbr + "/_err*\n")

    fo.write("\nall: ${ALLTGT}\n\n")
    fo.write("\t-ls */????/_err*\n")
    fo.write("\t-sh summary.sh\n")

gen_makefile()
