# -*- coding: utf-8 -*-
"""
    providers.py
    ~~~~~~~~~~~~
    <Add descritpion of the module here>.
    
    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD-style, see LICENSE for details
"""


class Provider:
    """

    """

    def __init__(self):
        self.is_open = False
        self.source = None
        self.handle = None

    def open(self):
        pass

    def address(self):
        return True

    def close(self):
        pass

    def read_from(self, address, count):
        return bytes()

    def write_to(self, buffer, address, count):
        pass
