# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe
options = {"py2exe":{"compressed": 9, # minimum size
                     "optimize": 2,
                     "bundle_files": 1  # if you want to compile pgnloader, you shouldn't contain this items because easygui (based on tkInter) doesn't allowed to be packaged as a single file.
                     }}
setup(
    console=["pythonpipe.py"], # change item here to compile different files
    options=options,
    zipfile=None)

