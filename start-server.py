import os
from pathlib import Path

os.system("python -V")
# py = Path().absolute() / ".venv/Scripts/python.exe"
# print(py.exists())

os.system("start python -m deepl_fastapi.run_uvicorn")
os.system("python -V")