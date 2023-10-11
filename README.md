# 📡 pytile: A simple Python API for Tile® Bluetooth trackers

[![CI][ci-badge]][ci]
[![PyPI][pypi-badge]][pypi]
[![Version][version-badge]][version]
[![License][license-badge]][license]
[![Code Coverage][codecov-badge]][codecov]
[![Maintainability][maintainability-badge]][maintainability]

<a href="https://www.buymeacoffee.com/bachya1208P" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

`pytile` is a simple Python library for retrieving information on
[Tile® Bluetooth trackers][tile] (including last location and more).

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

- Python 3.10
- Python 3.11
- Python 3.12

# Installation

```bash
pip install pytile
```

# Usage

## Getting an API Object

`pytile` usage starts with an [`aiohttp`][aiohttp] `ClientSession` – note that this
ClientSession is required to properly authenticate the library:

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

**Tile Premium Required: No**

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

- `accuracy`: the location accuracy of the Tile
- `altitude`: the altitude of the Tile
- `archetype`: the internal reference string that describes the Tile's "family"
- `dead`: whether the Tile is inactive
- `firmware_version`: the Tile's firmware version
- `hardware_version`: the Tile's hardware version
- `kind`: the kind of Tile (e.g., `TILE`, `PHONE`)
- `last_timestamp`: the timestamp at which the current attributes were received
- `latitude`: the latitude of the Tile
- `longitude`: the latitude of the Tile
- `lost`: whether the Tile has been marked as "lost"
- `lost_timestamp`: the timestamp at which the Tile was last marked as "lost"
- `name`: the name of the Tile
- `uuid`: the Tile UUID
- `visible`: whether the Tile is visible in the mobile app

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

## Getting Premium Tile's History

**Tile Premium Required: Yes**

You can retrieve a Tile's history by calling its `async_history` coroutine:

```python
import asyncio
from datetime import datetime

from aiohttp import ClientSession

from pytile import async_login


async def main() -> None:
    """Run!"""
    async with ClientSession() as session:
        api = await async_login("<EMAIL>", "<PASSWORD>", session)

        tiles = await api.async_get_tiles()

        for tile_uuid, tile in tiles.items():
            # Define a start and end datetime to get history for:
            start = datetime(2023, 1, 1, 0, 0, 0)
            end = datetime(2023, 1, 31, 0, 0, 0)
            history = await tile.async_history(start, end)
            # >>> { "version": 1, "revision": 1, ... }


asyncio.run(main())
```

# Contributing

Thanks to all of [our contributors][contributors] so far!

1. [Check for open features/bugs][issues] or [initiate a discussion on one][new-issue].
2. [Fork the repository][fork].
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix on a new branch.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `poetry run pytest --cov pytile tests`
9. Update `README.md` with any new documentation.
10. Submit a pull request!

[aiohttp]: https://github.com/aio-libs/aiohttp
[ci-badge]: https://github.com/bachya/pytile/workflows/CI/badge.svg
[ci]: https://github.com/bachya/pytile/actions
[codecov-badge]: https://codecov.io/gh/bachya/pytile/branch/dev/graph/badge.svg
[codecov]: https://codecov.io/gh/bachya/pytile
[contributors]: https://github.com/bachya/pytile/graphs/contributors
[fork]: https://github.com/bachya/pytile/fork
[issues]: https://github.com/bachya/pytile/issues
[license-badge]: https://img.shields.io/pypi/l/pytile.svg
[license]: https://github.com/bachya/pytile/blob/main/LICENSE
[maintainability-badge]: https://api.codeclimate.com/v1/badges/71eb642c735e33adcdfc/maintainability
[maintainability]: https://codeclimate.com/github/bachya/pytile/maintainability
[new-issue]: https://github.com/bachya/pytile/issues/new
[pypi-badge]: https://img.shields.io/pypi/v/pytile.svg
[pypi]: https://pypi.python.org/pypi/pytile
[tile]: https://www.thetileapp.com
[version-badge]: https://img.shields.io/pypi/pyversions/pytile.svg
[version]: https://pypi.python.org/pypi/pytile
