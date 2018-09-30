# -*- mode: python -*-

block_cipher = None


a = Analysis(['timer3.py'],
             pathex=['C:\\Users\\ray\\Desktop\\timer'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
a.scripts += [('\\resources\\recorder.exe', 'C:\\Users\\ray\Desktop\\timer\\resources\\recorder.exe', 'BINARY')]
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [('\\resources\\playing.png','C:\\Users\\ray\Desktop\\timer\\resources\\playing.png','DATA'),
           ('\\resources\\playing1.png','C:\\Users\\ray\Desktop\\timer\\resources\\playing1.png','DATA'),
           ('\\resources\\recording.png','C:\\Users\\ray\Desktop\\timer\\resources\\recording.png','DATA'),
           ('\\resources\\recording1.png','C:\\Users\\ray\Desktop\\timer\\resources\\recording1.png','DATA'),
           ('\\resources\\theman.jpg','C:\\Users\\ray\Desktop\\timer\\resources\\theman.jpg','DATA'),
           ('\\resources\\15.wav','C:\\Users\\ray\Desktop\\timer\\resources\\15.wav','DATA'),
           ('\\resources\\45.wav','C:\\Users\\ray\Desktop\\timer\\resources\\45.wav','DATA'),
           ('\\resources\\playing.png','C:\\Users\\ray\Desktop\\timer\\resources\\playing1.png','DATA')],
          name='TOEFL Timer Lite',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='C:\\Users\\ray\Desktop\\timer\\resources\\themanicon_XKf_icon.ico')
