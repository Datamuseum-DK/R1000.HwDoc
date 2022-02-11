
help:
	@echo "Available Targets:"
	@echo "	Fetch		- Fetch PDF files from datamuseum.dk bitstore"
	@echo "	Extract		- Extract images from the PDF files"
	@echo "	ImageProc	- Setup for Image Processing"
	@echo "	RemoveImages	- Remove background images from schematics"
	@echo "	AddImages	- Add background images to schematics"
	@echo "	RebuildSymbols	- Rebuild KiCad Symbols"
	@echo "	NetLists	- Rebuild KiCad Netlists"
	@echo
	@echo "If you want the bulk storage elsewhere, create symlinks"
	@echo "to CacheDir and WorkDir first."
	@echo "(See also target "phk" in the Makefile)"


all:	\
	CacheDir \
	WorkDir \
	Fetch \
	Extract \

CacheDir:
	[ -d CacheDir ] || mkdir -p CacheDir

WorkDir:
	[ -d WorkDir ] || mkdir -p WorkDir

Fetch:	CacheDir
	@$(MAKE) t_fetch ARTIFACT=${SCH_MEM32} EXT=pdf
	@$(MAKE) t_fetch ARTIFACT=${SCH_FIU} EXT=pdf
	@$(MAKE) t_fetch ARTIFACT=${SCH_SEQ} EXT=pdf
	@$(MAKE) t_fetch ARTIFACT=${SCH_TYP} EXT=pdf
	@$(MAKE) t_fetch ARTIFACT=${SCH_VAL} EXT=pdf
	@$(MAKE) t_fetch ARTIFACT=${SCH_IOC} EXT=pdf
	@$(MAKE) t_fetch ARTIFACT=${SCH_RESHA} EXT=pdf

Extract: WorkDir
	@$(MAKE) t_extract PDF=CacheDir/${SCH_MEM32}.pdf BOARD=MEM32
	@$(MAKE) t_extract PDF=CacheDir/${SCH_FIU}.pdf BOARD=FIU
	@$(MAKE) t_extract PDF=CacheDir/${SCH_SEQ}.pdf BOARD=SEQ
	@$(MAKE) t_extract PDF=CacheDir/${SCH_TYP}.pdf BOARD=TYP
	@$(MAKE) t_extract PDF=CacheDir/${SCH_VAL}.pdf BOARD=VAL
	@$(MAKE) t_extract PDF=CacheDir/${SCH_IOC}.pdf BOARD=IOC
	@$(MAKE) t_extract PDF=CacheDir/${SCH_RESHA}.pdf BOARD=RESHA

ImageProc: Fetch Extract
	cd ImageProcessing && sh prepare_image_processing.sh
	@echo "Now do:"
	@echo ""
	@echo "	cd WorkDir/imgproc && make -j A_LOT"
	@echo ""
	@echo "where A_LOT is as many CPU cores as you want to use"
	@echo ""
	@echo "Output can be found in WorkDir/imgproc/BOARDNAME/IMAGE/"
	@echo ""
	@echo "The process will take days, and you can stop and continue"
	@echo "with the same command as you like."
	@echo ""
	@echo "To process just a single image:"
	@echo ""
	@echo "	cd WorkDir/imgproc && make VAL_0063"

RemoveImages:
	@env PYTHONPATH=.:${PYTHONPATH} python3 -u tools/remove_schematic_background_image.py

AddImages:
	@env PYTHONPATH=.:${PYTHONPATH} python3 -u tools/insert_schematic_background_image.py

RebuildSymbols:
	(cd ImageProcessing && sh refresh_kicad_symbols.sh)

NetLists:
	(cd Schematics/FIU && eeschema_do netlist FIU.kicad_sch .)
	(cd Schematics/IOC && eeschema_do netlist IOC.kicad_sch .)
	(cd Schematics/MEM32 && eeschema_do netlist MEM32.kicad_sch .)
	(cd Schematics/SEQ && eeschema_do netlist SEQ.kicad_sch .)
	(cd Schematics/TYP && eeschema_do netlist TYP.kicad_sch .)
	(cd Schematics/VAL && eeschema_do netlist VAL.kicad_sch .)

t_fetch:
	[ -s CacheDir/${ARTIFACT}.${EXT} ] || ( \
	    curl -o CacheDir/_${ARTIFACT}.${EXT} ${BITSTORE}${ARTIFACT} && \
	    mv CacheDir/_${ARTIFACT}.${EXT} CacheDir/${ARTIFACT}.${EXT} )

t_extract:
	[ -d WorkDir/${BOARD}/rawimg ] || ( \
	    mkdir -p WorkDir/${BOARD}/_rawimg && \
	    ${PDFIMAGES} ${PDF} WorkDir/${BOARD}/_rawimg/_ && \
	    mv WorkDir/${BOARD}/_rawimg WorkDir/${BOARD}/rawimg )


phk:
	rm -f CacheDir
	rm -f WorkDir
	ln -s /critter/BitStoreCache CacheDir
	ln -s /critter/R1K/HwWork WorkDir
	make all

BITSTORE = https://datamuseum.dk/bits/
SCH_MEM32 = 30000956
SCH_FIU = 30000957
SCH_SEQ = 30000958
SCH_TYP = 30000959
SCH_VAL = 30000960
SCH_IOC = 30000961
SCH_RESHA = 30000963

PDFIMAGES = /usr/local/libexec/xpdf/pdfimages
