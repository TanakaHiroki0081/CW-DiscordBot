# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(['app.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=['scraper', 'filter', 'discord_bot', 'main_ui'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='CW-Discord',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='CW-Discord') 