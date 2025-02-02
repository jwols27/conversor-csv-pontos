import nicegui
from pathlib import Path
import subprocess

static_dir = Path(nicegui.__file__).parent

script = f"""
nicegui-pack --onefile --name "conversor-csv-pontos" main.py
"""
subprocess.call(script, shell=True)
