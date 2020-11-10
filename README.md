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

# NOTE: Version 5.0.0

Version 5.0.0 is a complete re-architecture of `pytile` – as such, the API has changed.
Please read the documentation carefully!

# Python Versions

`pytile` is currently supported on:

* Python 3.6
* Python 3.7
* Python 3.8
* Python 3.9

# Installation

```python
pip install pytile
```

# Usage

## Getting an API Object

`pytile` usage starts with an [`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` –
note that this ClientSession is required to properly authenticate the library:

```python
import asyncio

from aiohttp import ClientSession

from pytile import async_login


async def main() -> None:
    """Run!"""
    async with ClientSession() as session:
        api = await async_login("<EMAIL>", "<PASSWORD>", session)


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
    async with ClientSession() as session:
        api = await async_login(
            "<EMAIL>", "<PASSWORD>", session, client_uuid="MY_UUID", locale="en-GB"
        )


asyncio.run(main())
```

## Getting Tiles

```python
import asyncio

from aiohttp import ClientSession

from pytile import async_login


async def main() -> None:
    """Run!"""
    async with ClientSession() as session:
        api = await async_login("<EMAIL>", "<PASSWORD>", session)

        tiles = await api.async_get_tiles()


asyncio.run(main())
```

The `async_get_tiles` coroutine returns a dict with Tile UUIDs as the keys and `Tile`
objects as the values.

### The `Tile` Object

The Tile object comes with several properties:

* `accuracy`: the location accuracy of the Tile
* `altitude`: the altitude of the Tile
* `archetype`: the internal reference string that describes the Tile's "family"
* `dead`: whether the Tile is inactive
* `firmware_version`: the Tile's firmware version
* `hardware_version`: the Tile's hardware version
* `kind`: the kind of Tile (e.g., `TILE`, `PHONE`)
* `last_timestamp`: the timestamp at which the current attributes were received
* `latitude`: the latitude of the Tile
* `longitude`: the latitude of the Tile
* `lost`: whether the Tile has been marked as "lost"
* `lost_timestamp`: the timestamp at which the Tile was last marked as "lost"
* `name`: the name of the Tile
* `uuid`: the Tile UUID
* `visible`: whether the Tile is visible in the mobile app

```python
import asyncio

from aiohttp import ClientSession

from pytile import async_login


async def main() -> None:
    """Run!"""
    async with ClientSession() as session:
        api = await async_login("<EMAIL>", "<PASSWORD>", session)

        tiles = await api.async_get_tiles()

        for tile_uuid, tile in tiles.items():
            print(f"The Tile's name is {tile.name}")
            # ...


asyncio.run(main())
```

In addition to these properties, the `Tile` object comes with an `async_update` coroutine
which requests new data from the Tile cloud API for this Tile:

```python
import asyncio

from aiohttp import ClientSession

from pytile import async_login


async def main() -> None:
    """Run!"""
    async with ClientSession() as session:
        api = await async_login("<EMAIL>", "<PASSWORD>", session)

        tiles = await api.async_get_tiles()

        for tile_uuid, tile in tiles.items():
            await tile.async_update()


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
