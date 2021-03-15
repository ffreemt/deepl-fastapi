# deepl-fastapi
<!--- repo-name  pypi-name  mod_name func_name --->
[![tests](https://github.com/ffreemt/deepl-fastapi/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/deepl-fastapi.svg)](https://badge.fury.io/py/deepl-fastapi)

your own deepl server

## Installation

*   Clone the repo []() and `cd deepl-fastapi`
*   `pip install -r requirements.txt
    * or ``poetry install``

## Usage

```bash
uvicorn deepl_fastapi.deepl_server:app --reload
```

Point your browser to [http://127.0.0.1:8000/text/?q=test&to_lang=zh](http://127.0.0.1:8000/text/?q=test&to_lang=zh)

Or in python code (`pip install requests`)
```python
import requests

text = "test this and that"
data = {"text": text, "to_lang": "zh"}
resp = requests.post("http://127.0.0.1:8000", data=data)
print(resp.json)
# {'q': {'text': 'test this and that', 'from_lang': None, 'to_lang': 'zh', 'description': None}, 'result': '试探 左右逢源 检验 审时度势'}

```

## Swagger UI

 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
