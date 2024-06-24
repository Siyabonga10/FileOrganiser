from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QFont, QIcon
from FileManagmentUtils import sort_by_name
from StatusCodes import FileFilterModes, StatusCodes
import sys


class SortByTextMenu(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setFont(QFont("arial", 15))
        self.font_smaller = QFont("arial", 12)
        self.folder_icon = QIcon('./assets/icons/folder.png')
        self.layout = QtWidgets.QVBoxLayout(self)

        self.original_folder_widget = QtWidgets.QLineEdit(self)
        self.original_folder_widget.setPlaceholderText("Enter the original file path")

        self.original_folder_widget.setFixedWidth(500)
        self.original_folder_label = QtWidgets.QLabel("Original File Path:")

        self.folder_button1 = QtWidgets.QPushButton()
        self.folder_button1.setIcon(self.folder_icon)
        self.folder_button1.clicked.connect(self.find_first_folder)

        row_layout = QtWidgets.QHBoxLayout(self)
        row_layout.addWidget(self.original_folder_label, alignment=QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        row_layout.addWidget(self.original_folder_widget, alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop, stretch=2)
        row_layout.addWidget(self.folder_button1, alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(row_layout)

        self.substring_input = QtWidgets.QLineEdit(self)
        self.substring_input.setPlaceholderText("Enter a substring")

        self.substring_input.setFixedWidth(500)
        self.substring_input_label = QtWidgets.QLabel("Text to look for")

        row_layout = QtWidgets.QHBoxLayout(self)
        row_layout.addWidget(self.substring_input_label, alignment=QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        row_layout.addWidget(self.substring_input, alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(row_layout)

        # Add radio buttons
        self.starts_with_radio_button = QtWidgets.QRadioButton(self)
        self.starts_with_radio_button.setText("Starts With")
        self.starts_with_radio_button.setFont(self.font_smaller)
        self.starts_with_radio_button.click()

        self.ends_with_radio_button = QtWidgets.QRadioButton(self)
        self.ends_with_radio_button.setText("Ends With")
        self.ends_with_radio_button.setFont(self.font_smaller)

        self.contains_radio_button = QtWidgets.QRadioButton(self)
        self.contains_radio_button.setText("Contains")
        self.contains_radio_button.setFont(self.font_smaller)

        # Group the buttons
        self.filter_mode_group = QtWidgets.QButtonGroup()
        self.filter_mode_group.addButton(self.contains_radio_button)
        self.filter_mode_group.addButton(self.ends_with_radio_button)
        self.filter_mode_group.addButton(self.starts_with_radio_button)

        # Map to the appropriate casing mode
        self.filter_modes = {
            self.starts_with_radio_button: FileFilterModes.STARTS_WITH,
            self.ends_with_radio_button: FileFilterModes.ENDS_WITH,
            self.contains_radio_button: FileFilterModes.CONTAINS
        }

        row_layout = QtWidgets.QHBoxLayout()
        row_layout.addWidget(self.starts_with_radio_button, alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop, stretch=20)
        row_layout.addWidget(self.ends_with_radio_button, alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)
        row_layout.addWidget(self.contains_radio_button, alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(row_layout)

        self.new_file_path = QtWidgets.QLineEdit(self)
        self.new_file_path.setPlaceholderText("Enter a new file path")

        self.new_file_path.setFixedWidth(500)
        self.new_file_path_label = QtWidgets.QLabel("New File Path")

        self.folder_button2 = QtWidgets.QPushButton()
        self.folder_button2.setIcon(self.folder_icon)
        self.folder_button2.clicked.connect(self.find_second_folder)

        row_layout = QtWidgets.QHBoxLayout(self)
        row_layout.addWidget(self.new_file_path_label, alignment=QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        row_layout.addWidget(self.new_file_path, alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop, stretch=2)
        row_layout.addWidget(self.folder_button2, alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(row_layout)

        self.submit_button = QtWidgets.QPushButton("Sort")

        self.submit_button.setFixedWidth(100)
        self.layout.addWidget(self.submit_button, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight, stretch=1)
        self.submit_button.clicked.connect(self.user_submit)

    @QtCore.Slot()
    def find_first_folder(self):
        self.original_folder_widget.setText(QtWidgets.QFileDialog.getExistingDirectory(self, "Select the original folder"))

    @QtCore.Slot()
    def find_second_folder(self):
        self.new_file_path.setText(QtWidgets.QFileDialog.getExistingDirectory(self, "Select the new folder"))

    @QtCore.Slot()
    def user_submit(self):
        filter_mode = self.filter_mode_group.checkedButton()
        filter_mode = self.filter_modes.get(filter_mode, -1)

        # Validate the input
        base_file_path = self.original_folder_widget.text()
        new_file_path = self.new_file_path.text()
        sub_string = self.substring_input.text()
        code = sort_by_name(base_file_path, sub_string, new_file_path, filter_mode)

        # notify the user
        msg = QtWidgets.QMessageBox(self)
        msg.setText(StatusCodes.get_message(code))
        msg.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = SortByTextMenu()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
