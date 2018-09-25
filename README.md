# 📡 pytile: A simple Python API for Tile® Bluetooth trackers

[![Travis CI](https://travis-ci.org/bachya/pytile.svg?branch=master)](https://travis-ci.org/bachya/pytile)
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

# PLEASE READ: Version 2.0.0 and Beyond

Version 2.0.0 of `pytile` makes several breaking, but necessary changes:

* Moves the underlying library from
  [Requests](http://docs.python-requests.org/en/master/) to
  [aiohttp](https://aiohttp.readthedocs.io/en/stable/)
* Changes the entire library to use `asyncio`
* Makes 3.6 the minimum version of Python required

If you wish to continue using the previous, synchronous version of `pytile`,
make sure to pin version 1.1.0.

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

Create a client, initialize it, and get to work:

```python
import asyncio

from aiohttp import ClientSession

from pytile import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
    client = pytile.Client("<EMAIL>", "<PASSWORD>", websession)
    await client.async_init()

    # Get all Tiles associated with an account:
    await client.tiles.all()


asyncio.get_event_loop().run_until_complete(main())
```

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/pytile/issues)
  or [initiate a discussion on one](https://github.com/bachya/pytile/issues/new).
2. [Fork the repository](https://github.com/bachya/pytile/fork).
3. Install the dev environment: `make init`.
4. Enter the virtual environment: `pipenv shell`
5. Code your new feature or bug fix.
6. Write a test that covers your new functionality.
7. Run tests and ensure 100% code coverage: `make coverage`
8. Add yourself to `AUTHORS.md`.
9. Submit a pull request!
