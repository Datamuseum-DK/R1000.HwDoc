# Author: Poul-Henning Kamp <phk@phk.freebsd.dk>
#
# SPDX-License-Identifier: BSD-2-Clause
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

'''
STEP 140
========

	Landmark TL corner of docbox
'''

import sys

import schematics as sch

from debug_snippets import DebugSnippets

from corner import Corner

class Sheet_140(sch.Sheet):
    ''' ... '''

    def locate_docbox(self):
        ''' Create a landmark for the top left corner of the documentation box '''
        debug = DebugSnippets()
        pix = self.inch2pix(sch.INCH_T_L_DOCBOX)
        for box in (40, 60, 30):
            corner = Corner(
                self.img,
                pix,
                name="docbox",
                debug=debug,
                width=3,
                box=box,
            )
            if None in corner.pix:
                print("DOCBOX not found (box=%d)" % box, corner.pix)
            else:
                break
        debug.dump(self.fn_pfx + "docbox.png")
        if None in corner.pix:
            print("NB: DOCBOX not found", corner.pix)
        else:
            sch.add_small_marker(self.img, *corner.pix)
            self.add_landmark(*corner.pix, *sch.INCH_T_L_DOCBOX, "docbox")

if __name__ == "__main__":
    sheet = Sheet_140(sys.argv)
    sheet.load_raw_image()
    sheet.locate_docbox()
    sheet.write_landmarks()
    sheet.write_interpolators()
    sheet.write_interpolated()
