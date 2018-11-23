import os
import sys
from argparse import Namespace
import esptool
import urllib.request
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from .logger import setupLogger
import logging

setupLogger()

class DeviceFlasher(QThread):
    """
    Used to flash the Pixel Kit in a non-blocking manner.
    """
    # Emitted when flashing the Pixel Kit fails for any reason.
    on_flash_fail = pyqtSignal(str)
    # Emitted when flasher outputs data
    on_data = pyqtSignal(str)
    # Emitted when flasher outputs progress status
    on_progress = pyqtSignal(str)
    # Serial port to flash
    port = None
    # What kind of firmware to flash
    firmware_type = "micropython"

    def __init__(self, port):
        QThread.__init__(self)
        self.port = port

    def run(self):
        """
        Flash the device.
        """
        msg = "Unknown firmware type"
        logging.error(msg)
        self.on_flash_fail.emit(msg)

    def get_addr_filename(self, values):
        """
        Given a list of tuples containing the memory address and file addresses
        to write at that address, return another list of tuples containing
        the address and a file (stream) object.
        """
        if not isinstance(values, list):
            self.on_flash_fail.emit('Values must be a list.')
            return
        if any(not isinstance(value, tuple) for value in values):
            self.on_flash_fail.emit('Values items must be tuples.')
            return
        addr_filename = []
        try:
            for value in values:
                addr = int(value[0], 0)
                file = open(value[1], 'rb')
                addr_filename.append((addr, file))
            return addr_filename
        except Exception as ex:
            logging.error(ex)
            self.on_flash_fail.emit('Could not open file.')

    def flash(self, addr_filename=[]):
        """
        Flash firmware to the board using esptool
        """
        self.on_data.emit("Preparing to flash memory. This can take a while.")
        # Esptool is a command line tool and expects arguments that can be
        # emulated by creating manually a `Namespace` object
        args = Namespace()
        args.flash_freq = "40m"
        args.flash_mode = "dio"
        args.flash_size = "detect"
        args.no_progress = False
        args.compress = False
        args.no_stub = False
        args.trace = False
        args.verify = False
        # This is the most important bit: It must be an list of tuples each
        # tuple containing the memory address and an file object. Generate
        # this list with `get_addr_filename`
        args.addr_filename = addr_filename
        try:
            # Detects which board is being used. We already know what bard we
            # are flashing (ESP32) but this will also does a lot of other
            # setup automatically for us
            esp32loader = esptool.ESPLoader.detect_chip(
                self.port, 115200, False
            )
            # Loads the program bootloader to ESP32 internal RAM
            esp = esp32loader.run_stub()
            # Change baudrate to flash the board faster
            esp.change_baud(921600)
            # We already know the flash size but asking esptool to autodetect
            # it will save us some more setup
            esptool.detect_flash_size(esp, args)
            esp.flash_set_parameters(esptool.flash_size_bytes(args.flash_size))
            # Erase the current flash memory first
            self.on_data.emit('Erasing flash memory.')
            esptool.erase_flash(esp, args)
            self.on_data.emit('Writing on flash memory.')
            # Intercept what esptool prints out by replacing the `sys.stdout`
            # by
            old_stdout = sys.stdout
            sys.stdout = WritingProgressStdout(self.on_progress)
            # Write to flash memory
            esptool.write_flash(esp, args)
            # Restore old `sys.stdout`
            sys.stdout = old_stdout
            # Reset the board so we don't have to turn the Pixel Kit on and off
            # again using its terrible power switch that looks like a button
            esp.hard_reset()
        except Exception as ex:
            logging.error(ex)
            self.on_flash_fail.emit("Could not write to flash memory.")

class WritingProgressStdout:
    """
    Replacement for `sys.stdout` that parses the esptool writing progress to
    emit only the progress percentage
    """
    def __init__(self, on_data):
        self.on_data = on_data
        self.status = ''

    def write(self, string):
        is_writing = string.find('Writing at')
        if is_writing != -1:
            status = string[string.find('(')+1:string.find(')')]
            if status != self.status:
                self.on_data.emit(status)
            if status == '100 %':
                self.on_data.emit('Wait for it!')
            self.status = status

    def flush(self):
        None
