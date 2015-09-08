# -*- coding: utf-8 -*-
"""
    explorer.py
    ~~~~~~~~~~~
    d3.js
    
    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD-style, see LICENSE for details
"""

from konfoo import *


def decode(decoder, source=None):
    if source:
        decoder.read(source, nested=True)
    decoder.save('data.ini', nested=True)
    return d3json(decoder.json())


def dpr(source=None):
    return decode(DPRAMAnalyzerPointer(address=0x62088000, interface=3), source)


if __name__ == "__main__":
    data = dpr()
    open('data.json', 'w').write(data)
