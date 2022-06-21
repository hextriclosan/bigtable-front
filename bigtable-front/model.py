from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtWidgets import QMessageBox
from plugins.plugin_factory import get_serializer


class Model(QAbstractTableModel):

    def __init__(self, *args, parent, schema=None, data=None, header, **kwargs):
        super(Model, self).__init__(*args, **kwargs)
        self.parent = parent
        self.schema = schema or ()
        self.formatted_data = ()
        self.data = data or ()
        self.header = header
        self.edits = {}

    def rowCount(self, index):
        return len(self.data)

    def columnCount(self, index):
        return len(self.header)

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.header[section]

        return QAbstractTableModel.headerData(self, section, orientation, role)

    def data(self, index, role):
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return self.data[index.row()][index.column()]

    def flags(self, index):
        flags = QAbstractTableModel.flags(self, index)
        if index.column() == 3:
            flags |= Qt.ItemFlag.ItemIsEditable

        return flags

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            try:
                if index.column() == 3:
                    cf = self.data[index.row()][0]
                    column = self.data[index.row()][1]
                    serializer_type = self.schema[cf][column]['type']
                    serializer = get_serializer(serializer_type)
                    binary_value = serializer.dump(value)
                    self.data[index.row()][2] = str(binary_value)

                    if cf not in self.edits:
                        self.edits[cf] = {}
                    self.edits[cf][column] = binary_value

                self.data[index.row()][index.column()] = value
                self.dataChanged.emit(index, index)
                return True
            except Exception as e:
                QMessageBox.warning(self.parent, "", "Error occurred: {}".format(str(e)))
                return False

    def set_schema(self, schema):
        self.schema = schema
        self.data = []
        self.edits = {}

        for cf_name, cf in self.schema.items():
            for column_name, _ in cf.items():
                self.data.append([cf_name, column_name, '', ''])

        self.layoutChanged.emit()

    def set_formatted_data(self, formatted_data):
        self.formatted_data = formatted_data
        self.data = []
        self.edits = {}

        column_families = self.formatted_data[1]
        for cf_name, cf in self.schema.items():
            if cf_name in column_families:
                family = column_families[cf_name]
                for column_name, converter_name in cf.items():
                    if column_name in family:
                        value = family[column_name]
                        serializer = get_serializer(converter_name['type'])
                        self.data.append([cf_name, column_name, str(value), serializer.load(value)])
                    else:
                        self.data.append([cf_name, column_name, '', ''])
            else:
                for column_name, _ in cf.items():
                    self.data.append([cf_name, column_name, '', ''])

        self.layoutChanged.emit()

    def get_formatted_data_to_store(self):
        return self.edits
