from cx_Freeze import setup, Executable

base = None    

executables = [Executable("timer.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "TOEFL Timer Lite",
    options = options,
    version = "0.0.1",
    description = 'A timer and recorder for TOEFL Speaking test',
    executables = executables
)