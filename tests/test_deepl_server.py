"""Sanity check."""
import os
import sys
from pathlib import Path
from time import sleep

import requests
from subprocess import Popen
import portalocker
from logzero import logger

# start the server if not already started

lockfile = f'{Path(__file__).parent.parent / "deepl_fastapi" / "deepl_server.py.portalocker.lock"}'
logger.info("lockfile: %s", lockfile)
file = open(lockfile, "r+")
try:
    portalocker.lock(file, portalocker.LOCK_EX | portalocker.LOCK_NB)
    locked = False
    portalocker.unlock(file)
except Exception:
    locked = True

logger.debug("locked: %s", locked)
if not locked:
    cwd = Path(__file__).absolute().parent.as_posix()
    executable = f"{sys.executable}"
    if os.name in ["posix"]:  # linux and friends
        cmd = f"nohup python -m deepl_fastapi.run_uvicorn > {cwd}" "/server.out 2>&1 &"
        Popen(cmd, shell=True)
        logger.info(
            "fastapi server running in background, output logged to: %s/server.out",
            cwd,
        )
    else:
        try:
            Popen(f"{executable} -m deepl_fastapi.run_uvicorn", shell=True)
            logger.info(
                "\n\t [%s] fastapi server running in background\n",
                "deepl_fastapi.run_uvicorn",
            )
        except Exception as exc:
            logger.debug(exc)

    # wait for server to come up
    sleep(20)


def test_deepl_server():
    try:
        _ = requests.get("http://127.0.0.1:8000/text/?q=test me", verify=False)
        res = str(_.json())
    except Exception as exc:
        logger.error(exc)

        # try one more time
        if os.name.lower() in ["posix"]:  # linux and friends
            sleep(25)
        else:  # Windows wait longer
            sleep(40)
        try:
            _ = requests.get("http://127.0.0.1:8000/text/?q=test me", verify=False)
            res = str(_.json())
        except Exception as exc:
            logger.error("2nd try: %s", exc)
            res = str(exc)

    assert "我" in res
