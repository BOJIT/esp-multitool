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

    def control(args):
        pass


    def discover(args):
        pass


    def flash(args):
        pass


    def serial(args):
        pass


    def stats(args):
        pass



def main(argv=None):
    # Instantiate base class
    espm = ESPMultitool()

    # Argument parser
    parser = argparse.ArgumentParser(description='esp-multitool.py v%s - \
        ESP-NOW based Upload/Debugging Utility' % __version__, prog='esp-multitool')

    # Global arguments
    parser.add_argument(
        '--port', '-p',
        help='Serial port device',
        default=os.environ.get('ESPTOOL_PORT', None))

    parser.add_argument(
        '--chip', '-c',
        help='Target chip type',
        type=lambda c: c.lower().replace('-', ''),
        choices=['auto', 'esp8266', 'esp32', 'esp32s2', 'esp32s3beta2', 'esp32s3', 'esp32c3', 'esp32c6beta', 'esp32h2'],
        default=os.environ.get('ESPTOOL_CHIP', 'auto'))
        # here for future use, argument currently unused

    parser.add_argument(
        '--baud', '-b',
        help='Serial port baud rate used when flashing/reading',
        type=arg_auto_int,
        default=os.environ.get('ESPTOOL_BAUD', espm.BAUD_RATE))

    # Subcommand arguments
    subparsers = parser.add_subparsers(
        dest='operation',
        help='Run esp-multitool {command} -h for additional help')


    # Control command
    parser_control = subparsers.add_parser(
        'control',
        help='Send control parameter information to target')

    parser_control.add_argument(
        'json',
        help='Literal JSON control string or path to JSON file')

    parser_control.add_argument(
        '--file', '-f',
        help='Flag indicating if filepath has been passed in',
        action='store_true')


    # Discover command
    parser_discover = subparsers.add_parser(
        'discover',
        help='Discover esp-multitool slaves in the vicinity')

    parser_discover.add_argument(
        '--locked', '-l',
        help='Show devices that declare themselves as "locked", i.e. connected to another master',
        action='store_true')


    # Flash command
    parser_flash = subparsers.add_parser(
        'flash',
        help='Flash target board over ESP-NOW')

    parser_flash.add_argument(
        'source',
        help='Source binary to flash')

    parser_flash.add_argument(
        '--target', '-t',
        help='Target MAC Address or Short Name')


    # Serial command
    parser_serial = subparsers.add_parser(
        'serial',
        help='Establish serial connection with target')

    parser_serial.add_argument(
        'command',
        help='Serial command to execute',
        choices=['connect', 'disconnect'])

    parser_serial.add_argument(
        '--target', '-t',
        help='Target MAC Address or Short Name')


    # Stats command
    parser_stats = subparsers.add_parser(
        'stats',
        help='Query stats information from target')

    parser_stats.add_argument(
        'key',
        help='key in JSON file to query. If unset, all keys are returned',
        default=None)

    parser_stats.add_argument(
        '--filename', '-f',
        help='Dump output to a file: path given as parameter')


    # Parse argument tree
    args = parser.parse_args(argv)
    print('esp-multitool.py v%s' % __version__)

    if args.operation is None:
        parser.print_help()
        sys.exit(0)



if __name__ == '__main__':
    main()
