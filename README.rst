pytile: A Simple Python Library for Tile® Bluetooth trackers
============================================================

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
  :target: https://codeclimate.com/github/bachya/pytile

.. image:: https://img.shields.io/badge/SayThanks-!-1EAEDB.svg
  :target: https://saythanks.io/to/bachya

pytile is a simple Python library for retrieving information on `Tile® Bluetooth
trackers <https://www.thetileapp.com>`_ (including last location and more).

This library is built on an unpublished, unofficial Tile API; it may alter or
cease operation at any point.

Installation
============

.. code-block:: bash

  $ pip install pytile

Usage
=====

.. code-block:: python

  import pytile

  client = pytile.Client('email@address.com', 'password12345')
  client.get_tiles()

  # => {"version":1,"revision":1,"timestamp":"2017-11-03T20:21:48.855Z","timestamp_ms":1509740508855,"result_code":0,"result":{"12988abcd712":{"tileState":{"uuid":"1298add778","connectionStateCode": ....

Contributing
============

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
