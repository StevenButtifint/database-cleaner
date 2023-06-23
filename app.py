from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import sys

from res.operations import *
from res.constants import *


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi(INTERFACE_DIR, self)

        self.main_page_stack = self.findChild(QStackedWidget, 'main_page_stack')

        self.setup()
        self.show()

    def _setup_home_page(self):
        btn_select_database = self.findChild(QPushButton, 'btn_select_database')
        btn_select_database.clicked.connect(lambda: self._select_database())
        btn_home_continue = self.findChild(QPushButton, 'btn_home_continue')
        btn_home_continue.clicked.connect(lambda: self.main_page_stack.setCurrentWidget(self.findChild(QWidget, 'tools_page')))
        btn_exit = self.findChild(QPushButton, 'btn_exit')
        btn_exit.clicked.connect(lambda: self.close())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    sys.exit(app.exec_())

