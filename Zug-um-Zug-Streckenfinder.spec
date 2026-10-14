# Erstellt von CodeCockpit. Sie dürfen die Datei anpassen, das Cockpit nutzt sie
# bei jedem Bau weiter. Pfade sind relativ zum Ordner Repository.

a = Analysis(['gui.py'], pathex=[], binaries=[], datas=[],
             hiddenimports=[], excludes=[])
pyz = PYZ(a.pure)

exe = EXE(pyz, a.scripts, a.binaries, a.datas, [], name='Zug-um-Zug-Streckenfinder',
          console=False, icon=None, upx=False)
