'''
Creates a simple GUI interface for flashing Kano Pixel Kit with MicroPython
and restoring the factory firmware (Kano Code).
'''
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QPushButton, QComboBox, QTextEdit)
from serial.tools.list_ports import comports as list_serial_ports
from serial import Serial
from .deviceflasher import DeviceFlasher
from .logger import setupLogger
import logging

class PixelKitFlasher(QWidget):
    comboSerialPorts = None
    btnRefreshPorts = None
    btnFlashMP = None
    btnFlashKC = None
    logArea = None
    flash_thread = None

    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.comboSerialPorts = QComboBox(self)
        self.comboSerialPorts.currentIndexChanged.connect(self.portChanged)
        self.comboSerialPorts.addItem('Select serial port...')
        self.btnRefreshPorts = QPushButton('Refresh ports', self)
        self.btnFlashMP = QPushButton('Flash MicroPython', self)
        self.btnFlashKC = QPushButton('Flash Kano Code', self)
        self.logArea = QTextEdit(self)
        self.logArea.setReadOnly(True)

        self.btnRefreshPorts.clicked.connect(self.refreshPorts)
        self.btnFlashMP.clicked.connect(self.flashMP)
        self.btnFlashKC.clicked.connect(self.flashKC)

        layout.addWidget(self.comboSerialPorts)
        layout.addWidget(self.btnRefreshPorts)
        layout.addWidget(self.btnFlashMP)
        layout.addWidget(self.btnFlashKC)
        layout.addWidget(self.logArea)

        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle('Kano Pixel Kit Flasher Tool')
        self.show()

        self.refreshPorts()

    def log(self, data):
        self.logArea.append(data)

    def enableFlashButtons(self, enabled=True):
        if not self.btnFlashKC or not self.btnFlashMP:
            return
        self.btnFlashMP.setEnabled(enabled)
        self.btnFlashKC.setEnabled(enabled)
        self.btnFlashMP.repaint()
        self.btnFlashKC.repaint()

    def updateButtonState(self):
        if self.flash_thread or\
           self.comboSerialPorts.currentIndex() < 1:
            self.enableFlashButtons(False)
        else:
            self.enableFlashButtons(True)

    def portChanged(self, i):
        self.updateButtonState()

    def refreshPorts(self):
        ports = list_serial_ports()
        rpks = list(filter(
            lambda port: (port.vid, port.pid) == (0x0403, 0x6015), ports
        ))
        self.comboSerialPorts.clear()
        self.comboSerialPorts.addItem('Select serial port...')
        self.comboSerialPorts.setCurrentIndex(0)
        for port in rpks:
            self.comboSerialPorts.addItem(port.device)
        self.comboSerialPorts.repaint()

    def flashMP(self):
        print('flash MicroPython', self.comboSerialPorts.currentText())
        self.flash_thread = DeviceFlasher(self.comboSerialPorts.currentText(),
                                          'micropython')
        self.flash_thread.finished.connect(self.flash_finished)
        self.flash_thread.on_flash_fail.connect(self.flash_failed)
        self.flash_thread.on_data.connect(self.on_flash_data)
        self.flash_thread.start()
        self.updateButtonState()

    def flashKC(self):
        self.flash_thread = DeviceFlasher(self.comboSerialPorts.currentText(),
                                          'kanocode')
        self.flash_thread.finished.connect(self.flash_finished)
        self.flash_thread.on_flash_fail.connect(self.flash_failed)
        self.flash_thread.on_data.connect(self.on_flash_data)
        self.flash_thread.start()
        self.updateButtonState()

    def flash_finished(self):
        self.log('Flash finished')
        self.flash_thread = None
        self.updateButtonState()

    def flash_failed(self, err):
        self.log(err)
        self.flash_thread = None
        self.updateButtonState()

    def on_flash_data(self, data):
        self.log(data)


def run():
    app = QApplication(sys.argv)
    flasher = PixelKitFlasher()
    sys.exit(app.exec_())
    setupLogger()
    logging.info('=========================')
    logging.info('         Started')
    logging.info('=========================')

if __name__ == '__main__':
    run()
