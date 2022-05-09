from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QMessageBox, QPushButton, QVBoxLayout, QLineEdit, QWidget, QHBoxLayout, QTableView, \
    QFileDialog
from yaml import safe_load
from bigtable import get_formatted_data, write_formatted_data
from model import Model


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("hextriclosan", "bigtable-front")

        self.model = Model(parent=self, header=("Column Family", "Column Name", "Raw View", "Value"))

        self.project_id = QLineEdit()
        self.project_id.setPlaceholderText("projectId")
        self.project_id.setText(self.settings.value('project_id'))

        self.instance_id = QLineEdit()
        self.instance_id.setPlaceholderText("instanceId")
        self.instance_id.setText(self.settings.value('instance_id'))

        self.table_id = QLineEdit()
        self.table_id.setPlaceholderText("tableId")
        self.table_id.setText(self.settings.value('table_id'))

        self.settings_layout = QHBoxLayout()
        self.settings_layout.addWidget(self.project_id)
        self.settings_layout.addWidget(self.instance_id)
        self.settings_layout.addWidget(self.table_id)

        self.row_key = QLineEdit()
        self.row_key.setPlaceholderText("rowKey")
        self.row_key.setText(self.settings.value('row_key'))

        self.load_schema_button = QPushButton("Load Schema")
        self.load_schema_button.clicked.connect(self.load_schema_click)

        self.read_data_button = QPushButton("Look up by key")
        self.read_data_button.clicked.connect(self.read_data_click)

        self.table = QTableView()
        self.table.setModel(self.model)
        header = self.table.horizontalHeader()
        header.resizeSection(0, 100)
        header.resizeSection(1, 100)
        header.resizeSection(2, 450)
        header.resizeSection(3, 450)

        self.write_data_button = QPushButton("Write Data")
        self.write_data_button.clicked.connect(self.write_data_click)

        self.layout = QVBoxLayout(self)
        self.layout.addLayout(self.settings_layout)
        self.layout.addWidget(self.row_key)
        self.layout.addWidget(self.load_schema_button)
        self.layout.addWidget(self.read_data_button)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.write_data_button)

    def load_schema_click(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.FileMode.ExistingFile)
        dlg.setNameFilter("Schema files (*.yaml)")
        if dlg.exec():
            filenames = dlg.selectedFiles()
            with open(filenames[0], "r") as stream:
                try:
                    yaml = safe_load(stream)
                    self.model.set_schema(yaml)
                except Exception as e:
                    QMessageBox.warning(self, "", "Error occurred: {}".format(str(e)))

    def read_data_click(self):
        row_key = self.row_key.text()
        project_id = self.project_id.text()
        instance_id = self.instance_id.text()
        table_id = self.table_id.text()

        self.settings.setValue("project_id", project_id)
        self.settings.setValue("instance_id", instance_id)
        self.settings.setValue("table_id", table_id)
        self.settings.setValue("row_key", row_key)
        try:
            data = get_formatted_data(project_id, instance_id, table_id, row_key)
            self.model.set_formatted_data(data)
        except Exception as e:
            QMessageBox.warning(self, "", "Error occurred: {}".format(str(e)))

    def write_data_click(self):
        project_id = self.project_id.text()
        instance_id = self.instance_id.text()
        table_id = self.table_id.text()
        row_key = self.row_key.text()
        try:
            formatted_data = (row_key, self.model.get_formatted_data_to_store())
            if not self.confirm_save(formatted_data):
                return

            write_formatted_data(project_id, instance_id, table_id, formatted_data)
        except Exception as e:
            QMessageBox.warning(self, "", "Error occurred: {}".format(str(e)))

    def confirm_save(self, formatted_data):
        text = "Save data to {}:<pre>{{}}</pre>".format(self.table_id.text())
        text_data = "row_key={}\n".format(formatted_data[0])
        for cf_name, cf in formatted_data[1].items():
            for key, value in cf.items():
                text_data += "  {}:{}={}\n".format(cf_name, key, str(value))

        msg = QMessageBox(self)
        msg.setStandardButtons(QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard)
        msg.setDefaultButton(QMessageBox.StandardButton.Discard)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Confirm save")
        msg.setText(text.format(text_data))

        return QMessageBox.StandardButton.Save == msg.exec()
