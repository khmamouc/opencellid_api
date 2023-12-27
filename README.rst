Opencellid API
==============


Install
-------

Install make to use

::

    $ apt install make   // In linux
    $ brew install make  // In macOs

Useful commands
---------------

**Build and run project with compose**

::

    $ make build

**Clean Reset project containers and volumes with compose**

::

    $ make clean

**Insert data in the principal database**

::

    $ make feed_db

**Format project code**

::

    $ make format

**Check for linting**

::

    $ make check_lint

**Makefile help**

::

    $ make help

**Run project tests**

You should build before testing

::

    $ make test

**Run project with compose**

::

    $ make up


Examples
--------

We can properly query the API


Available endpoints
-------------------

    - GET    /towers/

Towers can be filtered by cell, lat, lon, mcc, net, area, radio, range and unit
You can also get cell towers located within a circular boundary specified by
providing a conter_lat, a center_lon and radius.

::


                                 ****
                             *          *
                            *            *
                            *-----o       *
                            *            *
                             *          *
                                 ****
