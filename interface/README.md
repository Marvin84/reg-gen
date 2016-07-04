Experiment Browser Interface
===================

This interface provides a convenient way for browsing and searching experiments in a local database including metadata and sample information. Selected experiments can easily be exported in an *experimental matrix* to be used with RGT.

Data
-------------

The interface comes with a script to create your own database by crawling data from the [DeepBlue API](http://deepblue.mpi-inf.mpg.de). Just execute `deepBlueData.py` in the `db` subfolder to create a SQLite3 database named `deepBlue.db` and fill it.

As an alternative, we also provide a pre-filled database in the repository. Just extract `db/deepBlue.db.tar.bz2` into the `db` folder to obtain it.


Interface
-------------------

> **Requirements:**
> The interface is based on [QT](http://www.qt.io/) and its Python wrapper PyQT. Please ensure you installed the latest version [PyQT](https://www.riverbankcomputing.com/software/pyqt/download) which depends on [SIP](https://www.riverbankcomputing.com/software/sip/download). We tested PyQT 4.11.4 and SIP 4.18.
>
> In addition, please install the SQLite driver for QT:
> For Linux: `sudo apt-get install libqt4-sql-sqlite`
> For Mac: `sudo port install qt4-mac-sqlite3-plugin`

To run the interface, execute `python mainInt.py`. If you do not see any data in the tables, ensure that your `db/deepBlue.db` is accessible and contains data (see above).

