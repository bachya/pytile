📡 pytile: A simple Python API for Tile® Bluetooth trackers
===========================================================

.. image:: https://travis-ci.org/bachya/pytile.svg?branch=master
  :target: https://travis-ci.org/bachya/pytile

.. image:: https://img.shields.io/pypi/v/pytile.svg
  :target: https://pypi.python.org/pypi/pytile

.. image:: https://img.shields.io/pypi/pyversions/pytile.svg
  :target: https://pypi.python.org/pypi/pytile

.. image:: https://img.shields.io/pypi/l/pytile.svg
  :target: https://github.com/bachya/pytile/blob/master/LICENSE

.. image:: https://codecov.io/gh/bachya/pytile/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/bachya/pytile

.. image:: https://api.codeclimate.com/v1/badges/71eb642c735e33adcdfc/maintainability
   :target: https://codeclimate.com/github/bachya/pytile/maintainability

.. image:: https://img.shields.io/badge/SayThanks-!-1EAEDB.svg
  :target: https://saythanks.io/to/bachya

pytile is a simple Python library for retrieving information on
`Tile® Bluetooth trackers <https://www.thetileapp.com/en-us/>`_
(including last location and more).

This library is built on an unpublished, unofficial Tile API; it may alter or
cease operation at any point.

📡 PLEASE READ: 1.0.0 and Beyond
================================

Version 1.0.0 of pytile makes several breaking, but necessary changes:

* Moves the underlying library from
  `Requests <http://docs.python-requests.org/en/master/>`_ to
  `aiohttp <https://aiohttp.readthedocs.io/en/stable/>`_
* Changes the entire library to use :code:`asyncio`
* Makes 3.5 the minimum version of Python required

If you wish to continue using the previous, synchronous version of
pytile, make sure to pin version 1.1.2.

📡 Installation
===============

.. code-block:: bash

  $ pip install pytile

📡 Usage
========

.. code-block:: python

  import pytile

pytile starts within an
`aiohttp <https://aiohttp.readthedocs.io/en/stable/>`_ :code:`ClientSession`:

.. code-block:: python

  import asyncio

  from aiohttp import ClientSession

  from pytile import Client


  async def main() -> None:
      """Create the aiohttp session and run the example."""
      async with ClientSession() as websession:
          await run(websession)


  async def run(websession):
      """Run."""
      # YOUR CODE HERE

  asyncio.get_event_loop().run_until_complete(main())

Create a client and initialize it:

.. code-block:: python

  client = pytile.Client('<TILE EMAIL ADDRESS>', '<TILE_PASSWORD>', websession)
  await client.async_init()

Then, get to it!

.. code-block:: python

  # Get all Tiles associated with an account:
  await client.tiles.all()


📡 Contributing
===============

#. `Check for open features/bugs <https://github.com/bachya/pytile/issues>`_
   or `initiate a discussion on one <https://github.com/bachya/pytile/issues/new>`_.
#. `Fork the repository <https://github.com/bachya/pytile/fork>`_.
#. Install the dev environment: :code:`make init`.
#. Enter the virtual environment: :code:`pipenv shell`
#. Code your new feature or bug fix.
#. Write a test that covers your new functionality.
#. Run tests: :code:`make test`
#. Build new docs: :code:`make docs`
#. Add yourself to AUTHORS.rst.
#. Submit a pull request!
