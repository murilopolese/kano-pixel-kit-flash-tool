"""
Creates a simple GUI interface for flashing Kano Pixel Kit with MicroPython
and restoring the factory firmware (Kano Code).
"""
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QPushButton, QComboBox, QTextEdit)
from serial.tools.list_ports import comports as list_serial_ports
from serial import Serial
from .micropythonflasher import MicroPythonFlasher
from .kanocodeflasher import KanoCodeFlasher
from .logger import setupLogger
import logging
from .versions import (micropython as micropython_version,
                       pixel32 as pixel32_version,
                       kanocode as kanocode_version)

class App(QWidget):
    # References for the UI elements
    comboSerialPorts = None
    btnRefreshPorts = None
    btnFlashMicroPython = None
    btnFlashKanoCode = None
    logArea = None
    # Reference for the thread which will run the flash process
    flash_thread = None

    def __init__(self):
        super().__init__()
        # Initializes the UI elements
        self.initUi()
        # Populate the `comboSerialPorts` with current serial connections
        self.refreshPorts()

    def initUi(self):
        """
        Initializes the UI elements
        """
        # Create and set a layout to stack the components
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create UI elements:
        # List of ports (dropdown/combo box)
        self.comboSerialPorts = QComboBox(self)
        self.comboSerialPorts.currentIndexChanged.connect(self.portChanged)
        self.comboSerialPorts.addItem('Select serial port...')
        # Button to refresh ports
        self.btnRefreshPorts = QPushButton('Refresh ports', self)
        # Button to flash MicroPython and Kano Code firmwares
        self.btnFlashMicroPython = QPushButton('Flash MicroPython + Pixel32', self)
        self.btnFlashKanoCode = QPushButton('Flash Kano Code', self)
        # Text area for printing the logs (not editable)
        self.logArea = QTextEdit(self)
        self.logArea.setReadOnly(True)

        # Bind the clicks to its methods
        self.btnRefreshPorts.clicked.connect(self.refreshPorts)
        self.btnFlashMicroPython.clicked.connect(self.flashMicroPython)
        self.btnFlashKanoCode.clicked.connect(self.flashKanoCode)

        # Adding the UI components to the layout
        layout.addWidget(self.comboSerialPorts)
        layout.addWidget(self.btnRefreshPorts)
        layout.addWidget(self.btnFlashMicroPython)
        layout.addWidget(self.btnFlashKanoCode)
        layout.addWidget(self.logArea)

        # Set the window properties
        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle('Kano Pixel Kit Flasher Tool')
        self.show()

    def log(self, data):
        """
        Writes to text area on the UI
        """
        self.logArea.append(data)
        # Repaint will make sure it does change the textarea looks are updated
        self.logArea.repaint()

    def enableFlashButtons(self, enabled=True):
        """
        Enable buttons related to flashing firmwares
        """
        # If there are no buttons, skip it
        if not self.btnFlashKanoCode or not self.btnFlashMicroPython:
            return
        self.btnFlashMicroPython.setEnabled(enabled)
        self.btnFlashKanoCode.setEnabled(enabled)
        # Repaint will make sure it does change the button looks are updated
        self.btnFlashMicroPython.repaint()
        self.btnFlashKanoCode.repaint()

    def updateButtonState(self):
        """
        Check if buttons should be enabled or disabled and update them
        """
        if self.flash_thread or\
           self.comboSerialPorts.currentIndex() < 1:
            self.enableFlashButtons(False)
        else:
            self.enableFlashButtons(True)

    def portChanged(self, i):
        """
        Once the ports are changed, update button states
        """
        self.updateButtonState()

    def refreshPorts(self):
        """
        Scan the available serial ports for Pixel Kits and update the combo
        box that list them.
        """
        ports = list_serial_ports()
        # Filter the ports by Pixel Kit's vendor and product ids.
        rpks = list(filter(
            lambda port: (port.vid, port.pid) == (0x0403, 0x6015), ports
        ))
        # Reset the combo box
        self.comboSerialPorts.clear()
        self.comboSerialPorts.addItem('Select serial port...')
        self.comboSerialPorts.setCurrentIndex(0)
        # Add ports to the combo box and update its looks
        for port in rpks:
            self.comboSerialPorts.addItem(port.device)
        self.comboSerialPorts.repaint()

    def flashMicroPython(self):
        """
        Start thread for flashing MicroPython
        """
        msg = 'Flashing MicroPython (version {0}) and Pixel32 (version {1})'
        self.log(msg.format(micropython_version, pixel32_version))
        selectedPort = self.comboSerialPorts.currentText()
        self.flash_thread = MicroPythonFlasher(selectedPort)
        self.startFlashing()

    def flashKanoCode(self):
        """
        Start thread for flashing Kano Code firmware
        """
        msg = 'Flashing Kano Code firmware (version {0})'
        self.log(msg.format(kanocode_version))
        selectedPort = self.comboSerialPorts.currentText()
        self.flash_thread = KanoCodeFlasher(selectedPort)
        self.startFlashing()

    def startFlashing(self):
        """
        Bind flash thread signals, start it and update UI
        """
        self.flash_thread.finished.connect(self.flash_finished)
        self.flash_thread.on_flash_fail.connect(self.flash_failed)
        self.flash_thread.on_data.connect(self.on_flash_data)
        self.flash_thread.on_progress.connect(self.on_flash_data)
        self.flash_thread.start()
        self.updateButtonState()

    def flash_finished(self):
        """
        Called when flash is finished
        """
        self.log('Flash finished')
        self.flash_thread = None
        self.updateButtonState()

    def flash_failed(self, err):
        """
        Called when flash fails
        """
        self.log("ERROR: " + err)
        self.flash_thread = None
        self.updateButtonState()

    def on_flash_data(self, data):
        """
        Called when the thread running the flasher process emits a signal
        """
        self.log(data)



def run():
    app = QApplication(sys.argv)
    flasher = App()
    sys.exit(app.exec_())
    setupLogger()
    logging.info('=========================')
    logging.info('         Started')
    logging.info('=========================')

if __name__ == '__main__':
    run()
