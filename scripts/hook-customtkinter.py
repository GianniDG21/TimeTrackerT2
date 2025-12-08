"""
Hook PyInstaller per CustomTkinter
Ottimizza l'inclusione dei file necessari
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Raccoglie tutti i file di dati di CustomTkinter
datas = collect_data_files('customtkinter')

# Raccoglie tutti i submoduli
hiddenimports = collect_submodules('customtkinter')

# Aggiunge importazioni specifiche per PIL/Pillow
hiddenimports += [
    'PIL._tkinter_finder',
    'PIL.Image',
    'PIL.ImageTk',
    'PIL.ImageFont',
    'PIL.ImageDraw'
]