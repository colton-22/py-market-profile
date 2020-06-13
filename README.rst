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

Check my Medium post for details. Market Profile Value Area Calculations With Nifty Future As An Example https://link.medium.com/X8ThgRNYE2

What is `Market Profile <http://eminimind.com/the-ultimate-guide-to-market-profile/>`_ and `How are these calculated <https://www.sierrachart.com/index.php?page=doc/StudiesReference/TimePriceOpportunityCharts.html#Calculations>`_?

Development
===========

To run the all tests run::

    tox
