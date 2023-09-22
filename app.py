from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt
import sys

from res.operations import *
from res.constants import *
from res.threads import OperationThread
from res.database import Database
from res.validity import Validity
from res.uniformity import Uniformity
from res.consistency import Consistency
from res.cleaning import Cleaning


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi(INTERFACE_DIR, self)
        self.main_page_stack = self.findChild(QStackedWidget, 'main_page_stack')
        self.database = Database()
        self.completeness = None
        self.validity = None
        self.uniformity = None
        self.consistency = None
        self.cleaning = None
        self.uniformity_thread = None
        self.validity_thread = None
        self.completeness_thread = None
        self.consistency_thread = None
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
        btn_cleaning_page.clicked.connect(lambda: self.use_cleaning_page())

    def _setup_analysis_page(self):
        self.reset_analysis_page()
        btn_analysis_results_back = self.findChild(QPushButton, 'btn_analysis_results_back')
        btn_analysis_results_back.clicked.connect(lambda: self.main_page_stack.setCurrentWidget(self.findChild(QWidget, 'tools_page')))

    def _setup_analysis_results_page(self):
        btn_uniformity_calculate = self.findChild(QPushButton, 'btn_uniformity_calculate')
        btn_uniformity_calculate.clicked.connect(lambda: self.process_uniformity_analysis())
        btn_validity_calculate = self.findChild(QPushButton, 'btn_validity_calculate')
        btn_validity_calculate.clicked.connect(lambda: self.process_validity_analysis())
        combo_data_types = self.findChild(QComboBox, 'combo_data_types')
        combo_data_types.currentIndexChanged.connect(self.change_consistency_data_type)
        btn_consistency_calculate = self.findChild(QPushButton, 'btn_consistency_calculate')
        btn_consistency_calculate.clicked.connect(lambda: self.process_consistency_analysis())

    def use_cleaning_page(self):
        self.reset_cleaning_page()
        self.main_page_stack.setCurrentWidget(self.findChild(QWidget, 'cleaning_page'))

    def reset_cleaning_page(self):
        self.findChild(QLabel, 'lbl_output_notice').setText("")
        output_location = self.get_output_location()
        self.show_output_location(output_location)
        attributes = self.database.get_attributes()
        self.refresh_combo_attribute_list('com_numerical_attribute', attributes)
        self.refresh_combo_attribute_list('com_date_attribute', attributes)
        self.refresh_combo_attribute_list('com_syntax_attribute', attributes)

    def show_output_location(self, raw_output_location):
        if raw_output_location == "":
            self.findChild(QLabel, 'lbl_output_location').setText("Output Location: Current Location")
        else:
            if len(raw_output_location) > 40:
                raw_output_location = raw_output_location[-40:]
            self.findChild(QLabel, 'lbl_output_location').setText("Output Location:   ..."+str(raw_output_location))

    def process_consistency_analysis(self):
        combo_attribute_list = self.findChild(QComboBox, 'combo_attribute_list')
        combo_data_types = self.findChild(QComboBox, 'combo_data_types')
        database_attribute = combo_attribute_list.currentText()
        selected_data_type_index = combo_data_types.currentIndex()
        self.consistency = Consistency(self.database)
        if selected_data_type_index == 0:
            numeric_min_value = self.findChild(QLineEdit, 'numeric_min').text()
            numeric_max_value = self.findChild(QLineEdit, 'numeric_max').text()
            self.consistency_thread = OperationThread(self.consistency, lambda: self.consistency.calculate_numeric_invalid_records(database_attribute, numeric_min_value, numeric_max_value))
        elif selected_data_type_index == 1:
            date_min_value = self.findChild(QLineEdit, 'date_min').text()
            date_max_value = self.findChild(QLineEdit, 'date_max').text()
            self.consistency_thread = OperationThread(self.consistency, lambda: self.consistency.calculate_date_invalid_records(database_attribute, date_min_value, date_max_value))
        self.consistency_thread.completed.connect(self.show_consistency_stats)
        self.consistency_thread.start()

    def process_uniformity_analysis(self):
        database_attribute = self.findChild(QComboBox, 'uniformity_attribute_list').currentText()
        self.uniformity = Uniformity(self.database.table[database_attribute])
        self.uniformity_thread = OperationThread(self.uniformity, lambda: self.uniformity.calculate_uniformity_stats())
        self.uniformity_thread.completed.connect(self.show_uniformity_stats)
        self.uniformity_thread.start()

    def process_validity_analysis(self):
        database_attribute = self.findChild(QComboBox, 'validity_attribute_list').currentText()
        validity_format_entry = self.findChild(QLineEdit, 'validity_format_entry').text()
        self.validity = Validity(self.database.table[database_attribute])
        self.validity_thread = OperationThread(self.validity, lambda: self.validity.calculate_validity_stats(validity_format_entry))
        self.validity_thread.completed.connect(self.show_validity_stats)
        self.validity_thread.start()

    def show_uniformity_stats(self):
        unique_percentage_count = self.findChild(QLabel, 'unique_percentage_count')
        unique_percentage_count.setText(self.uniformity.get_unique_percentage_string())
        unique_count = self.findChild(QLabel, 'unique_count')
        unique_count.setText(str(self.uniformity.get_unique_count()))
        database_attribute = self.findChild(QComboBox, 'uniformity_attribute_list').currentText()
        database_column = self.database.table[database_attribute]
        boxplot_notice_lbl = self.findChild(QLabel, 'boxplot_notice_lbl')
        boxplot_notice_lbl.setText("")
        try:
            self.show_uniformity_boxplot(database_column)
        except:
            boxplot_notice_lbl.setText("No Plot Shown,\nAttribute is not Numeric")

    def show_uniformity_boxplot(self, database_attribute):
        central_widget = self.findChild(QWidget, 'uniformity_boxplot')
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        figure, ax = plt.subplots(facecolor='none')
        figure.patch.set_alpha(0)
        ax.patch.set_alpha(0)
        canvas = FigureCanvas(figure)
        layout.addWidget(canvas)
        create_boxplot_graph(canvas, ax, database_attribute)

    def show_validity_stats(self):
        invalid_count_validity = self.findChild(QLabel, 'invalid_count_validity')
        invalid_percentage_validity = self.findChild(QLabel, 'invalid_percentage_validity')
        invalid_count_validity.setText(str(self.validity.get_invalid_count()))
        invalid_percentage_validity.setText(self.validity.get_invalid_percentage_string())

    def show_consistency_stats(self):
        invalid_record_count = self.findChild(QLabel, 'invalid_record_count')
        invalid_record_count.setText(str(self.consistency.get_invalid_record_count()))
        invalid_record_percentage = self.findChild(QLabel, 'invalid_record_percentage')
        invalid_record_percentage.setText(self.consistency.get_invalid_record_percentage_string())

    def change_consistency_data_type(self):
        combo_data_types = self.findChild(QComboBox, 'combo_data_types')
        combo_data_types.currentIndex()
        consistency_stacked_widget = self.findChild(QStackedWidget, 'consistency_stacked_widget')
        consistency_stacked_widget.setCurrentIndex(combo_data_types.currentIndex())

    def reset_analysis_page(self):
        analysis_page_stack = self.findChild(QTabWidget, 'analysis_page_stack')
        analysis_page_stack.setCurrentWidget(self.findChild(QWidget, 'completeness'))

    def _setup_cleaning_page(self):
        btn_cleaning_back = self.findChild(QPushButton, 'btn_cleaning_back')
        btn_cleaning_back.clicked.connect(lambda: self.main_page_stack.setCurrentWidget(self.findChild(QWidget, 'tools_page')))

    def switch_operations_page(self):
        if self.check_database_selected():
            lbl_selected_database = self.findChild(QLabel, 'lbl_selected_database')
            lbl_selected_database.setText(str(self.database.name))
            self.main_page_stack.setCurrentWidget(self.findChild(QWidget, 'tools_page'))

    def check_database_selected(self):
        is_selected = False
        if len(self.findChild(QLineEdit, 'qle_selected_database').text()) > 0:
            self.findChild(QLabel, 'home_notice_lbl').setText("")
            is_selected = True
        else:
            self.findChild(QLabel, 'home_notice_lbl').setText("Please select a database first.")
        return is_selected

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
        self.completeness = Completeness(self.database)
        self.set_cleaning_operations()
        self.completeness_thread = OperationThread(self.completeness, lambda: self.completeness.calculate_stats())
        self.completeness_thread.completed.connect(self.show_completeness_stats)
        self.completeness_thread.start()


    def show_completeness_stats(self):
        self.update_overall_null_percent(self.completeness.get_overall_null_percentage())
        self.update_null_count_columns_table(self.completeness.get_null_count_per_column())
        self.update_null_over_time(self.completeness.get_null_over_time())
        self.reset_uniformity_page(self.database.get_attributes())
        self.reset_consistency_page(self.database.get_attributes())
        self.reset_validity_page(self.database.get_attributes())

    def update_overall_null_percent(self, percent_value):
        lbl_overall_null_percent = self.findChild(QLabel, 'lbl_overall_null_percent')
        lbl_overall_null_percent.setText("Overall Null Percentage: "+str(percent_value)+"%")

    def update_null_count_columns_table(self, nulls_per_column):
        tbl_null_per_column = self.findChild(QTableWidget, 'tbl_null_per_column')
        tbl_null_per_column.setRowCount(0)
        for attribute in range(len(nulls_per_column)):
            tbl_null_per_column.insertRow(attribute)
            tbl_null_per_column.setItem(attribute, 0, QTableWidgetItem(str(nulls_per_column.index[attribute])))
            tbl_null_per_column.setItem(attribute, 1, QTableWidgetItem(str(nulls_per_column[attribute])))

    def update_null_over_time(self, null_over_time_data):
        central_widget = self.findChild(QWidget, 'frm_null_over_time')
        layout_t = QVBoxLayout(central_widget)
        frame = QFrame(self)
        layout_t.addWidget(frame)
        figure, axis = plt.subplots()
        axis.patch.set_alpha(0)
        figure.patch.set_alpha(0)
        canvas = FigureCanvas(figure)
        layout_t = QVBoxLayout(frame)
        layout_t.addWidget(canvas)
        create_null_over_time_graph(canvas, axis, null_over_time_data)

    def reset_consistency_page(self, column_names):
        self.refresh_combo_attribute_list('combo_attribute_list', column_names)
        self.reset_consistency_data_types()

    def reset_validity_page(self, column_names):
        self.refresh_combo_attribute_list('validity_attribute_list', column_names)

    def reset_uniformity_page(self, column_names):
        self.refresh_combo_attribute_list('uniformity_attribute_list', column_names)

    def refresh_combo_attribute_list(self, combo_box, column_names):
        combo_attribute_list = self.findChild(QComboBox, combo_box)
        combo_attribute_list.clear()
        combo_attribute_list.addItems(column_names)

    def reset_consistency_data_types(self):
        combo_data_types = self.findChild(QComboBox, 'combo_data_types')
        combo_data_types.setCurrentIndex(0)
        consistency_stacked_widget = self.findChild(QStackedWidget, 'consistency_stacked_widget')
        consistency_stacked_widget.setCurrentIndex(0)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    sys.exit(app.exec_())

