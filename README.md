# Py-TwelveLabs
Copyright © 2024 Minura Punchihewa

Py-TwelveLabs is a Python library for interacting with the TwelveLabs API.

## Installation
### With pip
```bash
pip install py_twelvelabs
```

## Usage

First, sign up for a TwelveLabs account [here](https://playground.twelvelabs.io/signup) and get your API key.

The API key can either be passed to the constructor directly or through the environment variable `TWELVE_LABS_API_KEY` like so:
```bash
export TWELVE_LABS_API_KEY=tlk_...
```

Then, import the library and create a client object:
```python
from py_twelvelabs import TwelveLabsAPIClient

client = TwelveLabsAPIClient()
# OR
client = TwelveLabsAPIClient(api_key='tlk_...')
```



