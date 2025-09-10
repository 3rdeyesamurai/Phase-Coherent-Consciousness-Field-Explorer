
# -*- mode: python ; coding: utf-8 -*-

import os
import sys

block_cipher = None

# Add current directory to path
current_dir = r"C:\Users\Kobyd\OneDrive\Documents\GitHub\Phase-Coherent-Consciousness-Field-Explorer\ionic_propulsion_lab"

a = Analysis(
    [os.path.join(current_dir, 'gui_app.py')],
    pathex=[current_dir],
    binaries=[],
    datas=[
        (os.path.join(current_dir, 'config.json'), '.'),
        (os.path.join(current_dir, 'README.md'), '.'),
        (os.path.join(current_dir, 'USER_GUIDE.md'), '.'),
        (os.path.join(current_dir, 'INSTALL_GUIDE.md'), '.'),
        (os.path.join(current_dir, 'ion_hall_parametric.py'), '.'),
    ],
    hiddenimports=[
        'numpy',
        'pandas',
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
        'tkinter',
        'json',
        'os',
        'sys',
        'pathlib',
        'subprocess',
        'threading',
        'webbrowser',
        'socket',
        'urllib.request',
        'ion_hall_parametric',
        'numpy.core._methods',
        'numpy.lib.format',
    ],
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
    name='Ionic_Propulsion_Lab',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
