# uv run build.py
import subprocess
from platform import system

windows = ''
if system() == 'Windows':
    windows = r' --windowed'

script = f'nicegui-pack{windows} --onefile --name "conversor-csv-pontos" --icon=icon.ico main.py'
subprocess.call(script, shell=True)
