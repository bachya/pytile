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

`pytile` starts within an
[aiohttp](https://aiohttp.readthedocs.io/en/stable/) `ClientSession`:


```python
import asyncio

from aiohttp import ClientSession

from pytile import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        # YOUR CODE HERE


asyncio.get_event_loop().run_until_complete(main())
```

If you receive SSL errors, use `ClientSession(connector=TCPConnector(verify_ssl=False))`
instead:

```python
import asyncio

from aiohttp import ClientSession, TCPConnector

from pytile import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession(connector=TCPConnector(verify_ssl=False)) as websession:
        # YOUR CODE HERE


asyncio.get_event_loop().run_until_complete(main())
```

Create a client, initialize it, and get to work:

```python
import asyncio

from aiohttp import ClientSession

from pytile import async_login


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        client = await async_login("<EMAIL>", "<PASSWORD>", websession)

        # Get all Tiles associated with an account:
        await client.tiles.all()


asyncio.get_event_loop().run_until_complete(main())
```

If for some reason you need to use a specific client UUID (to, say, ensure that the
Tile API sees you as a client it's seen before) or a specific locale, you can do
so easily:

```python
import asyncio

from aiohttp import ClientSession

from pytile import async_login


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        client = await async_login(
            "<EMAIL>", "<PASSWORD>", websession, client_uuid="MY_UUID", locale="en-GB"
        )

        # Get all Tiles associated with an account:
        await client.tiles.all()


asyncio.get_event_loop().run_until_complete(main())
```

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/pytile/issues)
  or [initiate a discussion on one](https://github.com/bachya/pytile/issues/new).
2. [Fork the repository](https://github.com/bachya/pytile/fork).
3. Install the dev environment: `make init`.
4. Enter the virtual environment: `source .venv/bin/activate`
5. Code your new feature or bug fix.
6. Write a test that covers your new functionality.
7. Run tests and ensure 100% code coverage: `make coverage`
8. Add yourself to `AUTHORS.md`.
9. Submit a pull request!
