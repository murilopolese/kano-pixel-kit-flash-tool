import os
from .deviceflasher import DeviceFlasher
from .versions import kanocode as kanocode_version

class KanoCodeFlasher(DeviceFlasher):
    def run(self):
        firmware_path = os.path.join(
            os.path.dirname(__file__),
            'firmware',
            'rpk_{0}.bin'.format(kanocode_version)
        )
        print('rpk_{0}.bin'.format(kanocode_version))
        addr_filename = self.get_addr_filename([("0x0", firmware_path)])
        self.flash(addr_filename)
