import os
from .deviceflasher import DeviceFlasher
from .versions import (micropython as micropython_version,
                       pixel32 as pixel32_version)

class MicroPythonFlasher(DeviceFlasher):
    def run(self):
        micropython_path = os.path.join(
            os.path.dirname(__file__),
            'firmware',
            'esp32-{0}.bin'.format(micropython_version)
        )
        pixel32_path = os.path.join(
            os.path.dirname(__file__),
            'firmware',
            'pixel32-{0}.img'.format(pixel32_version)
        )
        addr_filename = self.get_addr_filename(
            [
                ("0x1000", micropython_path),
                ("0x200000", pixel32_path),
            ]
        )
        self.flash(addr_filename)
