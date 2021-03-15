"""Fastapi server"""
#

from typing import Optional

import os
import sys
# import asyncio

# from signal import signal, SIGINT, SIG_DFL

import portalocker
import logzero
from logzero import logger

logzero.loglevel(10)

# _ = """
# only run one instance
file = open(f"{__file__}.portalocker.lock", "r+")
try:
    # portalocker.lock(file, portalocker.constants.LOCK_EX)
    portalocker.lock(file, portalocker.LOCK_EX | portalocker.LOCK_NB)
except Exception as exc:
    logger.debug(exc)
    logger.info("Another copy is running, exiting...")
    raise SystemExit(1) from exc
# """

# import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel

# from get_ppbrowser.get_ppbrowser import LOOP

# import nest_asyncio
# nest_asyncio.apply(LOOP)

from deepl_scraper_pp.deepl_tr import deepl_tr


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
        _ = await deepl_tr(text, from_lang, to_lang)
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
        trtext = await deepl_tr(q, from_lang, to_lang)
    except Exception as exc:
        logger.error(exc)
        trtext = str(exc)

    result.update({"trtext": trtext})

    logger.debug("result: %s", result)

    return result


if __name__ == "__main__":
    # signal(SIGINT, SIG_DFL)
    # print("ctrl-C to interrupt")

    # loop = asyncio.get_event_loop()

    logger.info("pid: %s", os.getpid())

    port = 50051
    if len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except Exception:
            port = 50051

    host = "::1"
    host = "::"
    if len(sys.argv) > 1:
        host = sys.argv[1]

    # uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn.run("app.app:app",host='0.0.0.0', port=4557, reload=True, debug=True, workers=3)

    # loop = asyncio.new_event_loop()

    # uvicorn deepl_fastapi.deepl_server:app --reload
    # seem to work with nest_asyncio

    _ = """
    uvicorn.run(
        # app="deepl_fastapi.deepl_server:app",
        app=app,
        host="0.0.0.0",
        port=8000,
        # debug=True,
        # reload=True,
        # workers=2,
        loop=LOOP,
    )
    # """
