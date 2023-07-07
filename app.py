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

    def setup(self):
        self.main_page_stack.setCurrentWidget(self.findChild(QWidget, 'home_page'))
        self._setup_home_page()
        self._setup_tools_page()
        self._setup_analysis_page()
        self._setup_cleaning_page()

    def _setup_home_page(self):
        btn_select_database = self.findChild(QPushButton, 'btn_select_database')
        btn_select_database.clicked.connect(lambda: self._select_database())
        btn_home_continue = self.findChild(QPushButton, 'btn_home_continue')
        btn_home_continue.clicked.connect(lambda: self.main_page_stack.setCurrentWidget(self.findChild(QWidget, 'tools_page')))
        btn_exit = self.findChild(QPushButton, 'btn_exit')
        btn_exit.clicked.connect(lambda: self.close())

    def _setup_tools_page(self):
        btn_tools_back = self.findChild(QPushButton, 'btn_tools_back')
        btn_tools_back.clicked.connect(lambda: self.main_page_stack.setCurrentWidget(self.findChild(QWidget, 'home_page')))
        btn_analysis_page = self.findChild(QPushButton, 'btn_analysis_page')
        btn_analysis_page.clicked.connect(lambda: self.start_database_analysis())
        btn_cleaning_page = self.findChild(QPushButton, 'btn_cleaning_page')
        btn_cleaning_page.clicked.connect(lambda: self.main_page_stack.setCurrentWidget(self.findChild(QWidget, 'cleaning_page')))

    def _setup_analysis_page(self):
        analysis_page_stack = self.findChild(QTabWidget, 'analysis_page_stack')
        analysis_page_stack.setCurrentWidget(self.findChild(QWidget, 'completeness'))


    def _setup_cleaning_page(self):
        btn_cleaning_back = self.findChild(QPushButton, 'btn_cleaning_back')
        btn_cleaning_back.clicked.connect(lambda: self.main_page_stack.setCurrentWidget(self.findChild(QWidget, 'tools_page')))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    sys.exit(app.exec_())

