from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import sys

from res.operations import *
from res.constants import *
from res.analysis import Analysis
from res.database import Database


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi(INTERFACE_DIR, self)
        self.main_page_stack = self.findChild(QStackedWidget, 'main_page_stack')
        self.database = Database()
        self.analysis = None
        self.setup()
        self.show()

    def setup(self):
        self.main_page_stack.setCurrentWidget(self.findChild(QWidget, 'home_page'))
        self._setup_home_page()
        self._setup_tools_page()
        self._setup_analysis_page()
        self._setup_analysis_results_page()
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

    def _setup_analysis_results_page(self):
        combo_data_types = self.findChild(QComboBox, 'combo_data_types')
        combo_data_types.currentIndexChanged.connect(self.change_consistency_data_type)
        btn_consistency_calculate = self.findChild(QPushButton, 'btn_consistency_calculate')
        btn_consistency_calculate.clicked.connect(lambda: self.process_consistency_analysis())

    def process_consistency_analysis(self):
        combo_attribute_list = self.findChild(QComboBox, 'combo_attribute_list')
        combo_data_types = self.findChild(QComboBox, 'combo_data_types')
        database_attribute = combo_attribute_list.currentText()
        selected_data_type_index = combo_data_types.currentIndex()
        if selected_data_type_index == 0:
            numeric_min_value = self.findChild(QLineEdit, 'numeric_min').text()
            numeric_max_value = self.findChild(QLineEdit, 'numeric_max').text()
            self.analysis.consistency.calculate_numeric_invalid_records(database_attribute, numeric_min_value, numeric_max_value)
        invalid_record_count = self.findChild(QLabel, 'invalid_record_count')
        invalid_record_count.setText(str(self.analysis.consistency.get_invalid_record_count()))
        invalid_record_percentage = self.findChild(QLabel, 'invalid_record_percentage')
        invalid_record_percentage.setText(self.analysis.consistency.get_invalid_record_percentage_string())


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
        self.database.select_database()
        qle_selected_database = self.findChild(QLineEdit, 'qle_selected_database')
        qle_selected_database.setText(self.database.get_current_directory())

    def set_output_dir(self):
        self.database.set_output_directory()
        qle_selected_output = self.findChild(QLineEdit, 'qle_selected_output')
        qle_selected_output.setText(self.database.get_output_directory())

    def start_database_analysis(self):
        self.main_page_stack.setCurrentWidget(self.findChild(QWidget, 'analysis_results_page'))
        self.reset_analysis_page()
        self.analysis = Analysis(self.database)
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

