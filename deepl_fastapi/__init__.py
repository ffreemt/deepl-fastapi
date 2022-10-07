"""Init."""
# need this to rid of loop is already running
# get_page (runs pyppeteeer after main loop in uvicorn already started) after
import nest_asyncio

nest_asyncio.apply()

__version__ = "0.1.1"
