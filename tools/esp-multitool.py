#!/usr/bin/env python
#
# ESP-Multitool Uploader Script
# Copyright (C) 2021 James Bennion-Pedley
#
# Code based in part off the esptool.py project: https://github.com/espressif/esptool

import os
import sys
import argparse



__version__ = "0.0.1"

# Generic helper functions

def arg_auto_int(x):
    return int(x, 0)


class ESPMultitool():
    """
        Base class providing methods for interacting with the
        ESP-Multitool hardware.
    """

    BAUD_RATE = 115200

    # Sub-command functions

    def flash(args):
        pass


    def discover(args):
        pass



def main(argv=None):
    # Instantiate base class


    # Argument parser
    parser = argparse.ArgumentParser(description='esp-multitool.py v%s - \
        ESP-NOW based Upload/Debugging Utility' % __version__, prog='esp-multitool')

    # Global arguments
    parser.add_argument(
        '--port', '-p',
        help='Serial port device',
        default=os.environ.get('ESPTOOL_PORT', None))

    parser.add_argument('--chip', '-c',
        help='Target chip type',
        type=lambda c: c.lower().replace('-', ''),
        choices=['auto', 'esp8266', 'esp32', 'esp32s2', 'esp32s3beta2', 'esp32s3', 'esp32c3', 'esp32c6beta', 'esp32h2'],
        default=os.environ.get('ESPTOOL_CHIP', 'auto'))
        # here for future use, argument currently unused

    parser.add_argument(
        '--baud', '-b',
        help='Serial port baud rate used when flashing/reading',
        type=arg_auto_int,
        default=os.environ.get('ESPTOOL_BAUD', ESPMultitool.BAUD_RATE))

    # Subcommand arguments
    subparsers = parser.add_subparsers(
        dest='operation',
        help='Run esp-multitool {command} -h for additional help')





    args = parser.parse_args(argv)
    print('esp-multitool.py v%s' % __version__)

    # if args.operation is None:
    #     parser.print_help()
    #     sys.exit(1)



if __name__ == '__main__':
    main()
