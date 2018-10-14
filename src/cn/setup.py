# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe
options = {"py2exe":{"compressed": 9, # 极限压缩
                     "optimize": 2,
                     "bundle_files": 1  # 打包PGN loader时请删除此项，因为easygui依赖TkInter，无法打包成单个文件
                     }}
setup(
    console=["pythonpipe.py"], # 更改要打包的文件
    options=options,
    zipfile=None)

