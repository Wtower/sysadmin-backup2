sysadmin-backup
===============

Console backup application. Intended mainly for server administration.

Features
--------

- Configuration_ is YAML based
- Full logging_ capabilities with multiple handlers_ available
- Backup methods: tar and rsync
- Process lock so backup can execute after an existing backup finishes
- Auto-mount external device

.. _Configuration: https://github.com/Wtower/sysadmin-backup2/blob/master/conf/sample.conf.yaml
.. _logging: https://docs.python.org/3/library/logging.config.html#dictionary-schema-details
.. _handlers: https://docs.python.org/3/library/logging.handlers.html#module-logging.handlers

Usage
-----
::

    (sysadmin-backup2) gkarak@neil ~/w/p/sysadmin-backup2 (dev)> ./sysadmin-backup.py -h
    usage: sysadmin-backup.py [-h] [-v] [--version] conf_file

    sysadmin-backup

    positional arguments:
      conf_file   Configuration file

    optional arguments:
      -h, --help  show this help message and exit
      -v          Verbosity level
      --version   show program's version number and exit


Version note
------------

Currently under initial development.

This is the Version 2 in Python 3. For Version 1.20 in C++ see `sysadmin-backup v1`_.

.. _sysadmin-backup v1: https://github.com/Wtower/sysadmin-backup
