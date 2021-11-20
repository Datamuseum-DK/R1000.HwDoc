#!/usr/local/bin/python3
#
# Copyright (c) 2021 Poul-Henning Kamp
# All rights reserved.
#
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
STEP 150
========

	Apply finagle landmarks
	Create empty components file
	Project the 50DPI 'progress' image
	Produce horizontal/vertical line correlations
'''

import sys

from scipy.signal import correlate2d

import schematics as sch
import finagle

import templates

PATT_H = '#' * (sch.LINE_CORR * 2 + 1)

PATT_V = '#\n' * (sch.LINE_CORR * 2 + 1)

if __name__ == "__main__":
    sheet = sch.Sheet(sys.argv)
    sheet.load_raw_image()

    i = finagle.FINAGLE_LANDMARKS.get(sheet.board)
    if i:
        j = i.get(sheet.sheet)
        if j:
            for landmark in j:
                sheet.add_landmark(*landmark)
            sheet.write_landmarks()

    sheet.write_interpolators()
    sheet.write_interpolated()

    sheet.write_components()

    p50img = sheet.project(50)
    sheet.hide_borders(p50img, 50)
    sheet.write_image("proj50", p50img)

    template = templates.string_2_template(PATT_H)
    corr = correlate2d(sheet.img, template, "same")
    sheet.write_image("corr_h", corr)

    template = templates.string_2_template(PATT_V)
    corr = correlate2d(sheet.img, template, "same")
    sheet.write_image("corr_v", corr)
