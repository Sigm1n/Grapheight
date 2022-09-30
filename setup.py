from cx_Freeze import setup, Executable

base = None

executables = [Executable("GraphUI.py", base=base)]

packages = ["os", "tkinter", "challonge", "PIL", "csv", "requests", "json"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "Grapheight",
    options = options,
    version = "0.2",
    description = 'Top 8 Graphic creator for AZ Rivals',
    executables = executables
)