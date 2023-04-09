# -*- mode: python ; coding: utf-8 -*-

import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)
from glob import glob

block_cipher = None

added_files = [
    ('./content/ultralytics/*', 'ultralytics/'),
    ('./utils/data/kor_list.txt', 'utils/data/'),
    ('./utils/icons/dobby.ico', 'utils/icons/'),
    ('./content/ultralytics/trained', 'content/ultralytics/trained'),
    ('form.ui', '.')
]

a = Analysis(
    ['widget.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DobByiSFreE',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='utils\\icons\\dobby.ico',
)
