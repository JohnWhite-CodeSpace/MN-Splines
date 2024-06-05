from PyQt5.QtWidgets import QFileDialog, QTableWidget, QTableWidgetItem


class SpreadsheetLoader:
    def __init__(self, spreadsheet: QTableWidget):
        self.spreadsheet = spreadsheet

    def load_data_from_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Load Data File", "", "Text Files (*.txt)", options=options)

        if file_name:
            with open(file_name, 'r') as file:
                lines = file.readlines()

            self.spreadsheet.setRowCount(len(lines))

            for row, line in enumerate(lines):
                values = line.strip().split('\t')
                self.spreadsheet.setColumnCount(len(values))

                for col, value in enumerate(values):
                    item = QTableWidgetItem(value)
                    self.spreadsheet.setItem(row, col, item)

    def read_spreadsheet(self):
        num_rows = self.spreadsheet.rowCount()
        num_cols = self.spreadsheet.columnCount()
        columns_data = [[] for _ in range(num_cols)]
        for i in range(num_rows):
            for j in range(num_cols):
                item = self.spreadsheet.item(i, j)
                if item is not None:
                    try:
                        value = float(item.text())
                    except ValueError:
                        value = item.text()
                    columns_data[j].append(value)
        return columns_data
