""" Main application """
import argparse
from core.conf import Configuration

__version__ = 'v2.0.0'


class Backup:
    def __init__(self):
        parser = argparse.ArgumentParser(description="sysadmin-backup")
        parser.add_argument('conf_file', type=open, action=Configuration, help="Configuration file")
        parser.add_argument('--excludes', required=True, help="A list of paths to exclude")
        args = parser.parse_args()
        print(args)
