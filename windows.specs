# -*- mode: python -*-

block_cipher = None

a = Analysis(['run.py'],
             binaries=[],
             datas=[('rpkflashtool/firmware', 'rpkflashtool/firmware')],
             hiddenimports=[],
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
		  a.binaries,
		  a.datas,
          name='rpkflashtool',
          debug=False,
          strip=False,
          upx=True,
          console=False )
