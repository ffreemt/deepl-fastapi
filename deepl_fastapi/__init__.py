"""Init."""
# need this to rid of loop is already running
# get_page (runs pyppeteeer after main loop in uvicorn already started) after
import nest_asyncio

# from .deepl_server import app  # make uvicorn deepl_fastapi:app possible

nest_asyncio.apply()

__version__ = "0.1.2"
# __all__ = ("app",)
