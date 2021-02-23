.. trrex documentation master file, created by
   sphinx-quickstart on Mon Feb  8 23:15:03 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

trrex: Efficient keyword extraction with regex
==============================================

This package contains a function for efficiently representing a set of keywords as regex. This regex can be used to
replace keywords in sentences or extract keywords from sentences.

.. ipython:: python

    import re
    import trrex as tx

    pattern = tx.make(["baby", "bat", "bad"])
    re.findall(pattern, "The baby was scared by the bad bat.")

Installation
------------
First, obtain at least Python 3.6 and virtualenv if you do not already have them. Using a virtual environment is strongly
recommended, since it will help you to avoid clutter in your system-wide libraries. Once the requirements are met, you can use pip:

.. code-block:: bash

   pip install trrex


Documentation
-------------

**Getting Started**

* :doc:`quick-overview`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Getting Started

   quick-overview

**User Guide**

* :doc:`usage`
* :doc:`integration`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: User Guide

   usage
   integration

**Help & Reference**

* :doc:`api`


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Help & reference

   api
