# -*- mode: python ; coding: utf-8 -*-

# Path to the MySQL connector locales
mysql_locales_path = 'C:\\Users\\SGS-01\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python313\\site-packages\\mysql\\connector\\locales'

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
<<<<<<< HEAD
    datas=[('config.ini', '.')],
    hiddenimports=['mysql.connector.locales'],
=======
    datas=[
        (mysql_locales_path, 'mysql/connector/locales'),
        ('config.ini', '.')
    ],
    hiddenimports=[],
>>>>>>> 0603b9909ecdcba5f43356ef23a789964c295202
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
    name='Centro Electronico Ramon',
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
)
