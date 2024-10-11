#%%
import socket, sys
from datetime import datetime
from PyQt6.QtWidgets import  QScrollArea, QListWidget, QMenuBar, QTabWidget, QCheckBox, QPushButton, QComboBox, QLineEdit, QHBoxLayout, QLabel, QErrorMessage, QApplication, QMenuBar, QMenu, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QGroupBox, QInputDialog, QFileDialog
from PyQt6.QtCore import QThreadPool, QRunnable, pyqtSignal, QObject
from PyQt6.QtGui import QIntValidator, QAction, QImage, QPixmap, QColor, QPalette, QMovie
from PyQt6.QtWidgets import  QMenuBar, QLineEdit, QHBoxLayout, QLabel, QErrorMessage, QApplication, QMenuBar, QMenu, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QGroupBox, QInputDialog, QFileDialog



class connectionSignals(QObject):
    connectionSuccess = pyqtSignal(str)
    connectionFailure = pyqtSignal(str)


class SOCKETWORKER(QRunnable):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals
        self.run()
    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('127.0.0.1', 12345))
                print("Connected to MATLAB server.")
                message = 'CAUTION LASER ACTIVE'
                sock.sendall(message.encode())
                self.signals.connectionSuccess.emit('CONNECTED TO MATLAB')
        except Exception:
            self.signals.connectionFailure.emit('MATLAB NOT OPEN')


# Set up the client to connect to the server on localhost and port 12345
class WAITFORSLAP2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Wait for SLAP2')
        self.threadingPool = QThreadPool()
        self.STATUS = False
        self.onTime = None
        self.initUI()
    def initUI(self):

        #Setting Central Widget
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout()
        centralWidget.setLayout(mainLayout)

        #Button starts out as inactive
        self.initialize = QPushButton('Check For Matlab')
        self.initialize.clicked.connect(self.runWorker)
        self.shutterPulseButton = QPushButton('DONT PUSH THE BUTTON', self)
        self.shutterPulseButton.clicked.connect(self.turnOnLaser)
        self.shutterPulseButton.setEnabled(self.STATUS)
        self.statusLabel = QLabel(f'Matlab is NOT open')
        self.statusLabel.setStyleSheet('color: red')
        self.onSince = QLabel('Laser has not been on yet')
        mainLayout.addWidget(self.initialize)
        mainLayout.addWidget(self.shutterPulseButton)
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addWidget(self.onSince)
        
        
        self.show()

    #run worker as long as ui is open
    def runWorker(self):
        signals = connectionSignals()
        signals.connectionSuccess.connect(self.connectionSuccess)
        signals.connectionFailure.connect(self.connectionFail)
        self.threadingPool.start(SOCKETWORKER(signals))

    def connectionSuccess(self, message):
        self.statusLabel.setText(f'{message}: {datetime.now().strftime("%H:%M:%S")}')
        self.STATUS = True
        self.shutterPulseButton.setEnabled(self.STATUS)
        self.shutterPulseButton.setText('OK to turn on pulse and open shutter')
        self.onTime = datetime.now().strftime("%H:%M:%S")
        self.statusLabel.setStyleSheet('color: green')
        self.onSince.setText(f'On Since: {datetime.now().strftime("%H:%M:%S")}')
    def connectionFail(self,message):
        self.statusLabel.setText(f'{message}: {datetime.now().strftime("%H:%M:%S")}')
        self.STATUS = False
        self.shutterPulseButton.setEnabled(self.STATUS)

    def turnOnLaser(self):
        print('Only now will the laser be turned on...')
                                 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainApp = WAITFORSLAP2()
    sys.exit(app.exec())
# %%
