sysadmin-backup
===============

Console backup application. Intended mainly for server administration.

.. image:: https://img.shields.io/travis/Wtower/sysadmin-backup2/master.svg
  :target: https://travis-ci.org/Wtower/sysadmin-backup2

.. image:: https://img.shields.io/coveralls/Wtower/sysadmin-backup2/master.svg
  :target: https://coveralls.io/github/Wtower/sysadmin-backup2

Features
--------

- Configuration_ is YAML based
- Full logging_ capabilities with multiple handlers_ available
- Backup methods: tar and rsync
- Lock process so backup can execute after an existing backup finishes
- Auto-mount external device and open for encryption if encrypted
- Mysql and postgres dump

.. _Configuration: https://github.com/Wtower/sysadmin-backup2/blob/master/conf/sample.conf.yaml
.. _logging: https://docs.python.org/3/library/logging.config.html#dictionary-schema-details
.. _handlers: https://docs.python.org/3/library/logging.handlers.html#module-logging.handlers

Installation
------------

Download and extract::

  wget https://github.com/Wtower/sysadmin-backup2/archive/v2.0.0-beta.tar.gz
  tar xvzf v2.0.0-beta.tar.gz
  cd sysadmin-backup2-2.0.0-beta

Install python packages. You can use virtualenv (recommended) or system-wide (example on Ubuntu)::

  sudo apt install python3-pip
  sudo -H pip3 install -U pip setuptools
  sudo -H pip3 install -U -r requirements.txt

Usage
-----

Make sure to use python3::

    (sysadmin-backup2) gkarak@neil ~/w/p/sysadmin-backup2 (dev)> ./sysadmin-backup.py -h
    usage: sysadmin-backup.py [-h] [-v] [--version] conf_file

    sysadmin-backup

    positional arguments:
      conf_file   Configuration file

    optional arguments:
      -h, --help  show this help message and exit
      -v          Verbosity level
      --version   show program's version number and exit


For the configuration parameters see ``conf/sample.conf.yml``.

Cron entries sample::

    PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'

    # m h  dom mon dow   command
    0 5 * * * /root/sysadmin-backup2-2.0.0-beta/sysadmin-backup.py /etc/sysadmin-backup2/internal.conf.yml > /dev/null
    5 10-14/1 * * 1-5 /root/sysadmin-backup2-2.0.0-beta/sysadmin-backup.py /etc/sysadmin-backup2/external.conf.yml > /dev/null

Version note
------------

This is the Version 2 in Python 3. For Version 1.20 in C++ see `sysadmin-backup v1`_.

.. _sysadmin-backup v1: https://github.com/Wtower/sysadmin-backup
