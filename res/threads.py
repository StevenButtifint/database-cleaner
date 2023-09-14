import sys
import time
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal


class OperationThread(QThread):
    completed = pyqtSignal()

    def __init__(self, instance, operation):
        super().__init__()
        self.instance = instance
        self.operation = operation

    def run(self):
        self.operation()
        self.completed.emit()
