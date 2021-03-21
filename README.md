# deepl-fastapi
<!--- repo-name  pypi-name  mod_name func_name --->
[![tests](https://github.com/ffreemt/deepl-fastapi/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/deepl-fastapi.svg)](https://badge.fury.io/py/deepl-fastapi)

your own deepl server via fastapi, cross-platform (Windows/Linux/MacOs)

## Installation
```bash
pip install deepl-fastapi
```
or (if your use poetry)
```bash
poetry add deepl-fastapi
```
or
```
 pip install git+https://github.com/ffreemt/deepl-fastapi.git
```
or
*   Clone the repo [https://github.com/ffreemt/deepl-fastapi.git](https://github.com/ffreemt/deepl-fastapi.git)
    ```bash
    git clone https://github.com/ffreemt/deepl-fastapi.git
    ```
    and `cd deepl-fastapi`
*   `pip install -r requirements.txt
    * or ``poetry install``

## Usage

*   (Optional) but recommended: Create a virual environment
    e.g.,
    ```bash
    # Linux and friends
    python3.7 -m venv .venv
    source .venv/bin/activate

    # Windows
    # py -3.7 -m venv .venv
    # .venv\Scripts\activate
    ```

*   Start the server

Use uvicorn directly (note the `deepl_server` module, not `run_uvicorn`)
```bash
uvicorn deepl_fastapi.deepl_server:app
```

or
```bash
deepl-fastapi
# this option is available only if installed via pip install or poetry add
```

or
```bash
python3.7 -m deepl_fastapi.run_uvicorn
```

or run the server on the external net, for example at port 9888
```
uvicorn deepl_fastapi.deepl_server:app --reload --host 0.0.0.0 --port 9888
```

*   Explore and consume

Point your browser to [http://127.0.0.1:8000/text/?q=test&to_lang=zh](http://127.0.0.1:8000/text/?q=test&to_lang=zh)

Or in python code (`pip install requests` first)
```python
import requests

# get
url =  "http://127.0.0.1:8000/text/?q=test me&to_lang=zh"
print(requests.get(url).json())
# {'q': 'test me', 'from_lang': None, 'to_lang': 'zh',
# 'trtext': '考我 试探我 测试我 试探'}

# post
text = "test this and that"
data = {"text": text, "to_lang": "zh"}
resp = requests.post("http://127.0.0.1:8000/text", json=data)
print(resp.json())
# {'q': {'text': 'test this and that', 'from_lang': None, 'to_lang': 'zh', 'description': None},
# 'result': '试探 左右逢源 检验 审时度势'}

```

## Interactice Docs (Swagger UI)

 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
