#!/bin/sh
#
# Preparations for the image processing
#

set -e

WDIR=../WorkDir/imgproc

if [ ! -d $WDIR ] ; then
	mkdir -p $WDIR
fi

# Rebuild Chipdesc/chipdict.py

(
echo '#!/usr/bin/env python3'
echo ''
echo '# NB: MACHINE GENERATED FILE - DO NOT EDIT BY HAND!'
echo ''
echo '# see populate.sh for details'
echo ''
) > Chipdesc/chipdict.py

(
echo ''
echo 'CHIPSIGS = {}'
echo 'CHIPS = {}'
) > Chipdesc/chipdict.py.suf

for i in Chipdesc/[a-z]*.py
do
	env PYTHONPATH=".:"$PYTHONPATH python3 -u $i rebuild
done

sort Chipdesc/chipdict.py.suf >> Chipdesc/chipdict.py
rm -f Chipdesc/chipdict.py.suf

echo '

if __name__ == "__main__":
    for i, j in CHIPSIGS.items():
        if len(j) > 1:
            print("Chip Sig Collision:", j)
' >> Chipdesc/chipdict.py

env PYTHONPATH=. python3 Chipdesc/chipdict.py


rm -f ${WDIR}/* > /dev/null 2>&1 || true
rm -rf ${WDIR}/Chipdesc

find \
	Chipdesc \
	KiCadFiles \
	components.py \
	corner.py \
	debug_snippets.py \
	delaunay_interpolator.py \
	finagle.py \
	make_makefile.py \
	make_kicad_projects.py \
	page_numbers.py \
	rectangle.py \
	schematics.py \
	sexp.py \
	templates.py \
	step_???_* \
	hack_???_* \
	-print | cpio --insecure -dump ${WDIR}

# Remove non-schematic pages
rm -f ${WDIR}/../FIU/rawimg/_-000[0-8].pgm
rm -f ${WDIR}/../IOC/rawimg/_-000[0-9].pgm
rm -f ${WDIR}/../SEQ/rawimg/_-000[0-5].pgm
rm -f ${WDIR}/../SEQ/rawimg/_-009[2-9].pgm
rm -f ${WDIR}/../SEQ/rawimg/_-01??.pgm
rm -f ${WDIR}/../TYP/rawimg/_-000[0-7].pgm
rm -f ${WDIR}/../VAL/rawimg/_-000[0-7].pgm

(cd ${WDIR} && python3 -u make_makefile.py)

# Rebuild Kicad symbol library
#(
#	cd KiCadFiles
#	sh build.sh
#)
#MANUAL=/critter/R1K/Manual_Schematics
#
#for i in MEM32 TYP VAL IOC FIU SEQ
#do
#	cp KiCadFiles/R1000.kicad_sym $MANUAL/$i
#done
