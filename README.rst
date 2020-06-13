========
Overview
========

.. image:: https://travis-ci.org/bfolkens/py-market-profile.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/bfolkens/py-market-profile

A library to calculate Market Profile (Volume Profile) from a Pandas DataFrame.  This library expects the DataFrame to have an index of ``timestamp`` and columns for each of the OHLCV values.


* Free software: BSD license

Installation
============

::

    pip install marketprofile

Documentation
=============

[Example](https://github.com/stoictrader/py-market-profile/blob/master/examples/example_nf.py)


[What is Market Profile](https://medium.com/@beinghorizontal/bot-primer-part-2-market-profile-cc6d8fbc7769)

Development
===========

To run the all tests run::

    tox
