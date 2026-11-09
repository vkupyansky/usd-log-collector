from pathlib import Path

root = Path(SPECPATH)
a = Analysis([str(root / "main.py")], pathex=[str(root)])
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name="usd-log-collector",
    console=False,
    icon=str(root / "icon.ico"),
)
