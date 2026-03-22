# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\kk\\.gemini\\antigravity\\playground\\stellar-spicule\\video_sentinel_product.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\kk\\.gemini\\antigravity\\playground\\stellar-spicule\\redpanda_ceo.mp4', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Panda_Video_Sentinel_Pro',
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
    icon=['C:\\ag_labs\\super_panda.ico'],
)
