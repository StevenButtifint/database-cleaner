import sys
import time
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal

from res.analysis import Analysis


class OperationThread(QThread):

    def __init__(self, instance, operation):
        super().__init__()
        self.instance = instance
        self.operation = operation

