# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Users/joiffer/Desktop/选课/大语言模型辅助软件工程/HomeWork/PhotoWatermark2/src/main.py'],
    pathex=['/Users/joiffer/Desktop/选课/大语言模型辅助软件工程/HomeWork/PhotoWatermark2'],
    binaries=[],
    datas=[
        ('/Users/joiffer/Desktop/选课/大语言模型辅助软件工程/HomeWork/PhotoWatermark2/resources/icons', 'resources/icons'),
        ('/Users/joiffer/Desktop/选课/大语言模型辅助软件工程/HomeWork/PhotoWatermark2/resources/fonts', 'resources/fonts')
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'src.core.image_processor',
        'src.core.watermark',
        'src.core.batch_processor',
        'src.ui.main_window',
        'src.utils.config',
        'src.utils.logger',
        'src.utils.font_manager',
        'src.utils.template_manager'
    ],
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
    [],
    exclude_binaries=True,
    name='PhotoWatermark2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PhotoWatermark2',
)
app = BUNDLE(
    coll,
    name='PhotoWatermark2.app',
    icon=None,
    bundle_identifier=None,
)
