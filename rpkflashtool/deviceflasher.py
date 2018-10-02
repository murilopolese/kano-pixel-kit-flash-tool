import os
import appdirs
from argparse import Namespace
import esptool
import tempfile
import tarfile
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
    # Serial port to flash
    port = None
    # What kind of firmware to flash
    firmware_type = "micropython"

    def __init__(self, port, firmware_type="micropython"):
        QThread.__init__(self)
        self.port = port
        self.firmware_type = firmware_type

    def run(self):
        """
        Flash the device.
        """
        if self.firmware_type == "micropython":
            self.flash_micropython()
        elif self.firmware_type == "kanocode":
            self.flash_kanocode()
        else:
            msg = "Unknown firmware type: {0}".format(self.firmware_type)
            print(msg)
            logging.error(msg)
            self.on_flash_fail.emit(msg)

    def get_addr_filename(self, values):
        """
        Given a list of tuples containing the memory address and file to
        write at that address, return another list of tuples containing
        the address and a file object.
        """
        if not isinstance(values, list):
            print('Values must be a list')
            self.on_flash_fail.emit('Values must be a list.')
            return
        if any(not isinstance(value, tuple) for value in values):
            print('Values items must be tuples')
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
            print(ex)
            logging.error(ex)
            self.on_flash_fail.emit('Could not open file.')

    def write_flash(self, addr_filename):
        self.on_data.emit("Preparing to flash memory. This can take a while.")
        args = Namespace()
        args.flash_freq = "40m"
        args.flash_mode = "dio"
        args.flash_size = "detect"
        args.no_progress = False
        args.compress = False
        args.no_stub = False
        args.trace = False
        args.verify = False
        args.addr_filename = addr_filename
        try:
            esp32loader = esptool.ESPLoader.detect_chip(
                self.port, 115200, False
            )
            esp = esp32loader.run_stub()
            esp.change_baud(921600)
            esptool.detect_flash_size(esp, args)
            esp.flash_set_parameters(esptool.flash_size_bytes(args.flash_size))
            self.on_data.emit('Erasing flash memory.')
            esptool.erase_flash(esp, args)
            self.on_data.emit('Writing flash memory.')
            esptool.write_flash(esp, args)
            esp.hard_reset()
        except Exception as ex:
            print(ex)
            logging.error(ex)
            self.on_flash_fail.emit("Could not write to flash memory.")

    def flash_micropython(self):
        # firmware_path = os.path.relpath(
        #     'rpkflashtool/firmware/esp32-20180511-v1.9.4.bin'
        # )
        firmware_path = os.path.join(
            os.path.dirname(__file__),
            'firmware',
            'pixel32-v0.1.0.bin'
        )
        addr_filename = self.get_addr_filename([("0x0", firmware_path)])
        self.write_flash(addr_filename)

    def flash_kanocode(self):
        # firmware_path = os.path.relpath(
        #     'rpkflashtool/firmware/rpk_1.0.2_dump.bin'
        # )
        firmware_path = os.path.join(
            os.path.dirname(__file__),
            'firmware',
            'rpk_1.0.2_dump.bin'
        )
        addr_filename = self.get_addr_filename([("0x0", firmware_path)])
        self.write_flash(addr_filename)
