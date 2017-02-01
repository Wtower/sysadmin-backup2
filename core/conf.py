""" Configuration parser from file """
import argparse


class Configuration(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for line in values.read().split('\n'):
            if line and line[0].isalpha():
                args = ('--' + line).split('=')
                # setattr(namespace, args[0], args[1])
                parser.parse_args(args, namespace)
