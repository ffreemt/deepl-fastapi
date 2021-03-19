import sys

import subprocess

subprocess.Popen(f"{sys.executable} -m deepl_fastapi.run_uvicorn")
print(f"{sys.executable}")

print("continue...")
