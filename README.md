# 📡 pytile: A simple Python API for Tile® Bluetooth trackers

[![CI](https://github.com/bachya/pytile/workflows/CI/badge.svg)](https://github.com/bachya/pytile/actions)
[![PyPi](https://img.shields.io/pypi/v/pytile.svg)](https://pypi.python.org/pypi/pytile)
[![Version](https://img.shields.io/pypi/pyversions/pytile.svg)](https://pypi.python.org/pypi/pytile)
[![License](https://img.shields.io/pypi/l/pytile.svg)](https://github.com/bachya/pytile/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/pytile/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/pytile)
[![Maintainability](https://api.codeclimate.com/v1/badges/71eb642c735e33adcdfc/maintainability)](https://codeclimate.com/github/bachya/pytile/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

`pytile` is a simple Python library for retrieving information on
[Tile® Bluetooth trackers](https://www.thetileapp.com/en-us/) (including last
location and more).

This library is built on an unpublished, unofficial Tile API; it may alter or
cease operation at any point.

- [Python Versions](#python-versions)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

# Python Versions

`pytile` is currently supported on:

* Python 3.6
* Python 3.7
* Python 3.8

# Installation

```python
pip install pytile
```

# Usage

```python
import asyncio

from aiohttp import ClientSession

from pytile import async_login


async def main() -> None:
    """Run!"""
    client = await async_login("<EMAIL>", "<PASSWORD>")

    # Get all Tiles associated with an account:
    await client.tiles.all()


asyncio.run(main())
```

By default, the library creates a new connection to Tile with each coroutine. If you are
calling a large number of coroutines (or merely want to squeeze out every second of
runtime savings possible), an
[`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` can be used for connection
pooling:

```python
import asyncio

from aiohttp import ClientSession

from pytile import async_login


async def main() -> None:
    """Run!"""
    async with ClientSession() as session:
        client = await async_login("<EMAIL>", "<PASSWORD>", session)

        # Get all Tiles associated with an account:
        await client.tiles.all()


asyncio.run(main())
```

If for some reason you need to use a specific client UUID (to, say, ensure that the
Tile API sees you as a client it's seen before) or a specific locale, you can do
so easily:

```python
import asyncio

from aiohttp import ClientSession

from pytile import async_login


async def main() -> None:
    """Run!"""
    client = await async_login(
        "<EMAIL>", "<PASSWORD>", client_uuid="MY_UUID", locale="en-GB"
    )

    # Get all Tiles associated with an account:
    await client.tiles.all()


asyncio.run(main())
```

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/pytile/issues)
  or [initiate a discussion on one](https://github.com/bachya/pytile/issues/new).
2. [Fork the repository](https://github.com/bachya/pytile/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `script/test`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!
