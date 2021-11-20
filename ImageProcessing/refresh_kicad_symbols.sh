#!/bin/sh
#
# Preparations for the image processing
#

set -e

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

# Rebuild Kicad symbol library
(
	cd KiCadFiles
	sh -x build.sh
)

cp KiCadFiles/R1000.kicad_sym ../Schematics

for board in TYP VAL IOC SEQ FIU RESHA MEM32
do
	dir=../Schematics/$board
	if [ -d $dir ] ; then
		echo '(sym_lib_table (lib (name "r1000")(type "KiCad")(uri "${KIPRJMOD}/../R1000.kicad_sym")(options "")(descr "")))' > $dir/sym-lib-table
	fi
done
