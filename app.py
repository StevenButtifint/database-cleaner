from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import sys

from res.operations import *
from res.constants import *
from res.analysis import Analysis


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi(INTERFACE_DIR, self)
        self.main_page_stack = self.findChild(QStackedWidget, 'main_page_stack')
        self.analysis = Analysis()
        self.database_dir = ""
        self.database_name = ""
        self.output_dir = ""
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
        btn_select_database.clicked.connect(lambda: self.select_database())
        btn_select_output = self.findChild(QPushButton, 'btn_select_output')
        btn_select_output.clicked.connect(lambda: self.set_output_dir())
        btn_home_continue = self.findChild(QPushButton, 'btn_home_continue')
        btn_home_continue.clicked.connect(lambda: self.switch_operations_page())
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
        self.reset_analysis_page()

        btn_analysis_results_back = self.findChild(QPushButton, 'btn_analysis_results_back')
        btn_analysis_results_back.clicked.connect(lambda: self.main_page_stack.setCurrentWidget(self.findChild(QWidget, 'tools_page')))

    def reset_analysis_page(self):
        analysis_page_stack = self.findChild(QTabWidget, 'analysis_page_stack')
        analysis_page_stack.setCurrentWidget(self.findChild(QWidget, 'completeness'))

    def _setup_cleaning_page(self):
        btn_cleaning_back = self.findChild(QPushButton, 'btn_cleaning_back')
        btn_cleaning_back.clicked.connect(lambda: self.main_page_stack.setCurrentWidget(self.findChild(QWidget, 'tools_page')))

    def switch_operations_page(self):
        lbl_selected_database = self.findChild(QLabel, 'lbl_selected_database')
        lbl_selected_database.setText(str(self.database_name))
        self.main_page_stack.setCurrentWidget(self.findChild(QWidget, 'tools_page'))

    def select_database(self):
        self.set_database_dir()
        self.set_database_name()

    def set_database_name(self):
        database_name = self.database_dir.split("/")[-1]
        self.database_name = database_name

    def set_database_dir(self):
        self.database_dir = select_csv()
        qle_selected_database = self.findChild(QLineEdit, 'qle_selected_database')
        qle_selected_database.setText(self.database_dir)

    def set_output_dir(self):
        self.output_dir = select_file()
        qle_selected_output = self.findChild(QLineEdit, 'qle_selected_output')
        qle_selected_output.setText(self.output_dir)

    def start_database_analysis(self):
        self.main_page_stack.setCurrentWidget(self.findChild(QWidget, 'analysis_results_page'))
        self.reset_analysis_page()
        database = get_csv_data(self.database_dir)
        self.analysis.set_database(database)
        self.analysis_thread = OperationThread(self.analysis, self.analysis.calculate_completeness_stats)
        self.analysis_thread.completed.connect(self.show_completeness_stats)
        self.analysis_thread.start()

    def show_completeness_stats(self):
        self.update_overall_null_percent(self.analysis.completeness_stats.overall_null_percentage)
        self.update_null_count_columns_table(self.analysis.completeness_stats.null_count_per_column)
        self.update_null_over_time(self.analysis.completeness_stats.null_over_time)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    sys.exit(app.exec_())

