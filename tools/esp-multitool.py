#!/usr/bin/env python
#
# ESP-Multitool Uploader Script
# Copyright (C) 2021 James Bennion-Pedley
#
# Code based in part off the esptool.py project: https://github.com/espressif/esptool

import os
import sys
import argparse
import cutie

# This block is taken straight from esptool.py
try:
    import serial
except ImportError:
    print("Pyserial is not installed for %s. Check the README for installation instructions." % (sys.executable))
    raise

# check 'serial' is 'pyserial' and not 'serial' https://github.com/espressif/esptool/issues/269
try:
    if "serialization" in serial.__doc__ and "deserialization" in serial.__doc__:
        raise ImportError("""
esp-multitool.py depends on pyserial, but there is a conflict with a currently installed package named 'serial'.""")
except TypeError:
    pass  # __doc__ returns None for pyserial

try:
    import serial.tools.list_ports as list_ports
except ImportError:
    print("The installed version (%s) of pyserial appears to be too old for esptool.py (Python interpreter %s). "
          "Check the README for installation instructions." % (sys.VERSION, sys.executable))
    raise
except Exception:
    if sys.platform == "darwin":
        # swallow the exception, this is a known issue in pyserial+macOS Big Sur preview ref https://github.com/espressif/esptool/issues/540
        list_ports = None
    else:
        raise


__version__ = "0.0.1"

# Generic helper functions

def arg_auto_int(x):
    return int(x, 0)


class ESPMultitool():
    """
        Base class providing methods for interacting with the
        ESP-Multitool hardware.
    """

    # When running this script as a module, disable any printout/interactive
    # shell behaviour by default. Only set true by argparse.
    TERMINAL = False

    BAUD_RATE = 115200                  # Serial communication baud rate:
                                        # can only be changed for OTA and Serial operations
    DEFAULT_SERIAL_WRITE_TIMEOUT = 10   # timeout for serial port write
    DEFAULT_CONNECT_ATTEMPTS = 7        # default number of times to try connection


    def __init__(self, port=None):
        self._port = None
        if port is not None:
            self.port(port)

    # Auto port-creation code. If port exists, it is re-used.
    def port(self, port=None):
        if self._port is None:
            print("Creating new Serial instance...")
            if port is None:
                # Show all ports and wait for user prompt (terminal only)
                portlist = list_ports.comports()
                ports = ([p.device for p in portlist])
                port = self._option_prompt("Select Serial Port:", ports)

                self._port = serial.Serial(port, self.BAUD_RATE)

            elif isinstance(port, serial.Serial):
                # Assign existing serial objet - for use as a module
                self._port = port

            elif isinstance(port, str):
                # Open port based on serial identifier string
                self._port = serial.Serial(port, self.BAUD_RATE)

        return self._port


    # For any settings that aren't preset, a terminal prompt is created. If
    # the class is used in a module, an exception will occur.
    def _option_prompt(self, msg, opts):
        if self.TERMINAL is False:
            raise Exception("Behaviour not explicit - Possible options: \n" + "\n".join(opts))
        else:
            print('\n' + msg + '\n')
            opt = opts[cutie.select(opts)]
            print('')
            return opt


    # Sub-command functions
    def control(self, args):
        port = self.port()

    def discover(self, args):
        port = self.port()

    def flash(self, args):
        port = self.port()

    def serial(self, args):
        port = self.port()

    def stats(self, args):
        port = self.port()



def main(argv=None):
    # Instantiate base class with interactive terminal behaviour
    espm = ESPMultitool()
    espm.TERMINAL = True

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

    # Call relevant command
    operation_func = getattr(espm, args.operation)
    operation_func(args)


if __name__ == '__main__':
    main()
