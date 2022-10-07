"""Fastapi server"""
#

from typing import Optional

import os

# import sys
import asyncio

# import subprocess as sp

from signal import signal, SIGINT, SIG_DFL

import portalocker
import logzero
from logzero import logger

logzero.loglevel(10)

import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel

# lazy loading LOOP, wait for run_uvicorn to start first
# import lazy_import
# get_ppbrowser = lazy_import.lazy_module(get_ppbrowser)

from deepl_scraper_pp.deepl_tr import deepl_tr
from get_ppbrowser.get_ppbrowser import get_ppbrowser


async def get_page():
    try:
        browser = await get_ppbrowser()
    except Exception as exc:
        logger.error(exc)
        raise
    try:
        page = await browser.newPage()
    except Exception as exc:
        logger.error(exc)
        raise

    url = r"https://www.deepl.com/translator"
    try:
        await page.goto(url, timeout=16 * 1000)
    except Exception as exc:
        logger.error(exc)
        raise

    return page


try:
    LOOP = asyncio.get_event_loop()
    # LOOP = asyncio.get_running_loop()
except Exception as exc:
    logger.error("weird: %s", exc)
    raise SystemExit(1) from exc

try:
    PAGE = LOOP.run_until_complete(get_page())
except Exception as exc:
    logger.error(exc)
    raise SystemExit("Unable to connect to deepl.com") from exc


class Text(BaseModel):
    text: str
    from_lang: Optional[str] = None
    to_lang: Optional[str] = None
    description: Optional[str] = None


app = FastAPI(title="deepl-fastapi")


@app.post("/text/")
async def post_text(q: Text):
    text = q.text
    to_lang = q.to_lang
    from_lang = q.from_lang
    logger.debug("text: %s", text)

    # _ = sent_corr(text1, text2)
    try:
        _ = await deepl_tr(text, from_lang, to_lang, page=PAGE,)
    except Exception as exc:
        logger.error(exc)
        _ = {"error": True, "message": str(exc)}

    return {"q": q, "result": _}


@app.get("/text/")
async def get_text(
    q: Optional[str] = Query(
        None,
        max_length=1500,
        min_length=1,
        title="text to translate",
        description="max. 5000 chars, paragraphs will not be preserved. multiple translations may be provided for short phrases.",
    ),
    from_lang: Optional[str] = None,
    to_lang: Optional[str] = "zh",
):
    """Get text.

    http://127.0.0.1:8000/text/?q=abc&to_lang=zh
    """
    result = {
        "q": q,
        "from_lang": from_lang,
        "to_lang": to_lang,
    }
    try:
        trtext = await deepl_tr(q, from_lang, to_lang, page=PAGE,)
    except Exception as exc:
        logger.error(exc)
        trtext = str(exc)

    result.update({"trtext": trtext})
    result.update({"translation": trtext})

    logger.debug("result: %s", result)

    return result


def run_uvicorn():
    """Run uvicor.

    Must be run from a different file, e.g., run_uvicorn.py
    """
    uvicorn.run(
        # app="deepl_fastapi.deepl_server:app",
        app=app,  # this should work with python -m deepl_fastapi.deepl_server, still "attached to a different loop" error
        host="0.0.0.0",
        port=8000,
        # debug=True,
        # reload=True,
        # workers=2,
        # loop="asyncio",  # default "auto"
        # loop="uvloop",  # posix (linux and mac) only
    )


async def main():
    """Start run_uvicorn in the current our own LOOP.

    LOOP was used in deepl_scraper_pp.deepl_tr
    """
    # from get_ppbrowser.get_ppbrowser import LOOP

    # loop = asyncio.new_event_loop()
    # loop = asyncio.get_event_loop()

    # loop.run_in_executor(None, run_uvicorn)  # current loop

    future = LOOP.run_in_executor(None, run_uvicorn)

    # future = loop.run_in_executor(None, run_uvicorn)  # future from different loop

    # errors, crashed
    # future = LOOP.run_in_executor(LOOP, run_uvicorn)
    # future = loop.run_in_executor(LOOP, run_uvicorn)

    await future  # wrong?

    _ = """
    try:
        await future
    except Exception as exc:
        logger.error(exc)
        raise SystemExit(1) from exc
    # """


if __name__ == "__main__":
    logger.info("pid: %s", os.getpid())

    signal(SIGINT, SIG_DFL)
    print("ctrl-C to interrupt")

    # uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn.run("app.app:app",host='0.0.0.0', port=4557, reload=True, debug=True, workers=3)

    # uvicorn deepl_fastapi.deepl_server:app --reload
    # works with nest_asyncio

    # loop = asyncio.new_event_loop()
    # loop.create_task(main())
    # loop.run_forever()

    _ = """
    try:
        LOOP.run_until_complete(main())
    except Exception as exc:
        logger.error(exc)
    finally:
        LOOP.close()
    # """

    _ = """
    try:
        LOOP.create_task(main())
        LOOP.run_forever()
    except Exception as exc:
        logger.error(exc)
    finally:
        LOOP.close()
    # """
    # only run one instance
    # if not Path(f"{__file__}.portalocker.lock").exists(): sp.Popen("touch

    try:
        # portalocker.lock(file, portalocker.constants.LOCK_EX)
        file = open(f"{__file__}.portalocker.lock", "r+")
        portalocker.lock(file, portalocker.LOCK_EX | portalocker.LOCK_NB)
        ...
    except Exception as exc:
        logger.debug(exc)
        logger.error("Another copy is running, exiting...")
        raise SystemExit(1) from exc
        # raise
    finally:
        # LOOP.close()
        ...

    run_uvicorn()
