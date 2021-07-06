#!/usr/bin/env python
#
# ESP-Multitool Uploader Script
# Copyright (C) 2021 James Bennion-Pedley
#
# Code based in part off the esptool.py project: https://github.com/espressif/esptool

#################################### Modules ###################################

import argparse
import struct
import sys
import os
import subprocess

import time

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

#################################### Globals ###################################

__version__ = "0.0.1"       # esp-multitool release version

DEFAULT_SERIAL_WRITE_TIMEOUT = 10   # timeout for serial port write
DEFAULT_CONNECT_ATTEMPTS = 7        # default number of times to try connection

# Struct layouts - see packet.h
ESPM_ENDIANNESS = '<'
ESPM_HEADER = 'IB'
ESPM_BUF = 'II237s'
ESPM_SRV_REQ = 'B'

# SLIP Encoding characters
SLIP_END = b'\xc0'
SLIP_ESC = b'\xdb'
SLIP_ESC_END = b'\xdb\xdc'
SLIP_ESC_ESC = b'\xdb\xdd'

############################ Generic Helper Functions ##########################

def arg_auto_int(x):
    return int(x, 0)

def get_port_list():
    if list_ports is None:
        raise Exception("Listing all serial ports is currently not available. Please try to specify the port when "
                         "running esp-multitool.py or update the pyserial package to the latest version")
    return sorted(ports.device for ports in list_ports.comports())

# # This function is also lifted from esptool.py
# def slip_reader(port):
#     """Generator to read SLIP packets from a serial port.
#     Yields one full SLIP packet at a time, raises exception on timeout or invalid data.

#     Designed to avoid too many calls to serial.read(1), which can bog
#     down on slow systems.
#     """
#     partial_packet = None
#     in_escape = False
#     while True:
#         waiting = port.inWaiting()
#         read_bytes = port.read(1 if waiting == 0 else waiting)
#         if read_bytes == b'':
#             waiting_for = "header" if partial_packet is None else "content"
#             raise Exception("Timed out waiting for packet %s" % waiting_for)
#         for b in read_bytes:
#             if type(b) is int:
#                 b = bytes([b])  # python 2/3 compat

#             if partial_packet is None:  # waiting for packet header
#                 if b == b'\xc0':
#                     partial_packet = b""
#                 else:
#                     raise Exception('Invalid head of packet (0x%s)' % hexify(b))
#             elif in_escape:  # part-way through escape sequence
#                 in_escape = False
#                 if b == b'\xdc':
#                     partial_packet += b'\xc0'
#                 elif b == b'\xdd':
#                     partial_packet += b'\xdb'
#                 else:
#                     raise Exception('Invalid SLIP escape (0xdb, 0x%s)' % (hexify(b)))
#             elif b == b'\xdb':  # start of escape sequence
#                 in_escape = True
#             elif b == b'\xc0':  # end of packet
#                 yield partial_packet
#                 partial_packet = None
#             else:  # normal byte in packet
#                 partial_packet += b

# # SLIP flush input and output buffers

# """ Write bytes to the serial port while performing SLIP escaping """
# def slip_write(self, packet):
#     buf = b'\xc0' \
#         + (packet.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc')) \
#         + b'\xc0'
#     self._port.write(buf)

################################ Class Definition ##############################

class ESPMultitool():
    """
        Base class providing methods for interacting with the
        ESP-Multitool hardware.
    """

    BAUD_RATE = 115200                  # Serial communication baud rate:
                                        # can only be changed for OTA and Serial operations

    def __init__(self, port=None, interactive=False, daemon=False):
        self._interactive = interactive

        # TODO note that the serial port should only be instantiated in the worker process

        # Each class instance is bound to a single port, which is fixed.
        if port is None:
            # Show all ports and wait for user prompt (terminal only)
            self._port = self._option_prompt("Select Serial Port:", get_port_list())
        elif isinstance(port, str):
            self._port = port
            # Open port based on serial identifier string
            # try:
            #     self._port = serial.Serial(port, self.BAUD_RATE)
            # except:
            #     sys.exit("Could not open serial port: %s\n" % port)
        else:
            raise Exception("Invalid Serial Port Type:")

        # Launch Daemon if not already running
        if daemon is False:
            if os.name == 'nt':
                proc = subprocess.Popen([sys.executable, __file__, '--port', port, 'daemon', 'start'],
                                        stdin=None, stdout=None, stderr=None, shell=True,
                                        creationflags=subprocess.DETACHED_PROCESS |
                                        subprocess.CREATE_NEW_PROCESS_GROUP)
            elif os.name == 'posix':
                proc = subprocess.Popen(['nohup', sys.executable, __file__, '--port', port ,'daemon', 'start'],
                                        shell=True, stdout=None, stderr=None, preexec_fn=os.setpgrp)
            else :
                sys.exit("Operating system is unsupported!\n")

            print(proc.pid)
        # Look for open processes that are connected to the same requested port.
        # This service should terminate if the port becomes unavailable. Somehow notify main thread?

        # Connect to that port, if it doesn't exist create that subprocess.

    def __del__(self):
        print('Goodbye')

        # If the port isn't required to be kept open, close the port.


    # For any settings that aren't preset, a terminal prompt is created. If
    # the class is used in a module, an exception will occur.
    def _option_prompt(self, msg, opts):
        if self._interactive is False:
            sys.exit("Behaviour not explicit - Possible options: \n\n" + "\n".join(opts))
        else:
            # Syntax is a bit verbose here: required for PlatformIO terminal input
            print('\n' + msg + '\n')
            for i, opt in enumerate(opts):
                print("  %d) %s" % (i, opt))
            print('\n' + 'Select Option: ')
            usr = input()
            while 1:
                try:
                    opt = opts[int(usr)]
                    return opt
                except:
                    print('Invalid Option - Select Again: ')
                    usr = input()

    def _slip_read(self):
        # self.port.read_until
        pass
        # Wait until bytes are in the buffer.

        # Read the header to see how long the message is:

        # for number of packets:
            # get packet length
            # read in block. Strip start and end characters

            # ack after each packet?

        # Remove SLIP encoding, return single buf containing any joined fragments

    def _slip_write(self, msg):
        self.port.write('test')
        pass
        # add in all SLIP-escaped characters

        # step over array, adding in slip frames. Break into sub-buffers

        # Pass these buffers to Serial.write

        # ack after each packet?


    # Sub-command functions
    def control(self, args):
        pass

    def discover(self, args):
        print(args)

    def daemon(self, args):
        if args['command'] == 'start':
            while(1):
                print('Daemon Running!')
                time.sleep(1)

                # Add graceful termination

        elif args['command'] == 'stop':
            print('Shutting down daemon...')

    def flash(self, args):
        pass

    def serial(self, args):
        pass

    def stats(self, args):
        pass


############################# Terminal Entry Point #############################

def main(argv=None):
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
        default=os.environ.get('ESPTOOL_BAUD', ESPMultitool.BAUD_RATE))

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


    # Daemon command
    parser_daemon = subparsers.add_parser(
        'daemon',
        help='Control the state of the handler daemon')

    parser_daemon.add_argument(
        'command',
        help='Start or stop the ESP-Multitool daemon',
        choices=['start', 'stop'])


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
    nsargs = parser.parse_args(argv)
    print('esp-multitool.py v%s' % __version__)

    if nsargs.operation is None:
        parser.print_help()
        sys.exit(0)

    args = vars(nsargs)

    # Instantiate base class with interactive terminal behaviour
    if (args['operation'] == 'daemon') and (args['command'] == 'start'):
        espm = ESPMultitool(port=args['port'], interactive=True, daemon=True)
    else:
        espm = ESPMultitool(port=args['port'], interactive=True)

    # Call relevant command
    operation_func = getattr(espm, args['operation'])
    operation_func(args)


if __name__ == '__main__':
    main()
