import nicegui
from pathlib import Path
import subprocess
from platform import system

static_dir = Path(nicegui.__file__).parent

windows = ''
if system() == 'Windows':
    windows = r' --windowed'

script = f'nicegui-pack{windows} --onefile --name "conversor-csv-pontos" --icon=icon.ico main.py'
subprocess.call(script, shell=True)
