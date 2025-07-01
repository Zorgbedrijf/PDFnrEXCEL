# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['streamlit_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('frontend/app.py', 'frontend'),
        ('.venv/Lib/site-packages/streamlit/static', 'streamlit/static'),
        ('.venv/Lib/site-packages/streamlit/runtime', 'streamlit/runtime'),
    ],
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'streamlit.runtime.caching.legacy_caching',
        'pandas',
        'fitz',  # PyMuPDF
        'openpyxl',
        'io',
        're',
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
    name='Medicatie_PDF_Converter',
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
