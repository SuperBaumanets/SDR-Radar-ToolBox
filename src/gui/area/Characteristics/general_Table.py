from typing import Dict
from PySide6.QtWidgets import (QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout,
                              QComboBox, QHeaderView, QLineEdit)
from PySide6.QtCore import Qt, Signal

from src.gui.styles.table import table_characterictics

class TableCharacteristics(QWidget):
    data_changed = Signal()
    
    def __init__(self, action_handler=None):
        super().__init__()
        self.action_handler = action_handler
        self.table = QTableWidget()
        self.table.setStyleSheet(table_characterictics)
        self._setup_ui()
        self._setup_table()
        self.locator_columns: Dict[str, int] = {}  # Словарь для хранения столбцов локаторов

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.table.setFixedSize(1290, 200)
        layout.addWidget(self.table)
        
    def _setup_table(self):
        self.table.setRowCount(2)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Метрика", 
            "Единицы", 
            "Порог", 
            "Цель"
        ])

        # Настройка внешнего вида
        header = self.table.horizontalHeader()
        # Столбец "Метрика" - подстраивается под содержимое
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # Столбец "Единицы" - фиксированный размер
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        self.table.setColumnWidth(1, 100)
        # Столбцы "Порог" и "Цель" - растягиваются
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(False)

        
        # Добавляем строки
        self._add_metrics()
        
    def _add_metrics(self):
        self._setup_range_row()
        self._setup_speed_row()
    
    def _setup_range_row(self):
        # Строка для дальности
        row = 0
        self.table.setItem(row, 0, QTableWidgetItem("Разрешающая способность по дальности"))

        # Комбобокс для единиц измерения
        self.measurement_range_resolution = QComboBox()
        self.measurement_range_resolution.addItems(["м", "км"])
        self.measurement_range_resolution.setFixedWidth(100)
        self.table.setCellWidget(row, 1, self.measurement_range_resolution)

        self.data_threshold_range_resolution = QLineEdit()
        self.data_threshold_range_resolution.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(row, 2, self.data_threshold_range_resolution)

        self.data_objective_range_resolution = QLineEdit()
        self.data_objective_range_resolution.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(row, 3, self.data_objective_range_resolution)

        if self.action_handler is not None:
            self.data_threshold_range_resolution.textChanged.connect(self.action_handler.update_range_resolution)
            self.data_objective_range_resolution.textChanged.connect(self.action_handler.update_range_resolution)
            self.measurement_range_resolution.currentTextChanged.connect(self.action_handler.update_range_resolution)
        else:
            print("Ошибка: action_handler не инициализирован !")

    def _setup_speed_row(self):
        # Строка для скорости
        row = 1
        self.table.setItem(row, 0, QTableWidgetItem("Разрешающая способность по скорости"))

        # Комбобокс для единиц измерения
        self.measurement_speed_resolution = QComboBox()
        self.measurement_speed_resolution.addItems(["м/c", "км/ч"])
        self.measurement_speed_resolution.setFixedWidth(100)
        self.table.setCellWidget(row, 1, self.measurement_speed_resolution)

        self.data_threshold_speed_resolution = QLineEdit()
        self.data_threshold_speed_resolution.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(row, 2, self.data_threshold_speed_resolution)

        self.data_objective_speed_resolution = QLineEdit()
        self.data_objective_speed_resolution.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(row, 3, self.data_objective_speed_resolution)

        if self.action_handler is not None:
            self.data_threshold_speed_resolution.textChanged.connect(self.action_handler.update_speed_resolution)
            self.data_objective_speed_resolution.textChanged.connect(self.action_handler.update_speed_resolution)
            self.measurement_speed_resolution.currentTextChanged.connect(self.action_handler.update_speed_resolution)
        else:
            print("Ошибка: action_handler не инициализирован !")

    def add_locator_column(self, locator_name: str):
        """Добавляет колонку для нового локатора и возвращает индекс столбца"""
        col = self.table.columnCount()
        self.locator_columns[locator_name] = col

        # Вставляем новый столбец
        self.table.insertColumn(col)

        # Устанавливаем режим растяжения для нового столбца
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(col, QHeaderView.Stretch)

        # Настраиваем заголовок
        self.table.setHorizontalHeaderItem(col, QTableWidgetItem(locator_name))

        # Добавляем ячейки
        for row in range(self.table.rowCount()):
            item = QTableWidgetItem("0.0")
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, col, item)

        # Восстанавливаем настройки основных столбцов
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        self.table.setColumnWidth(1, 100)

        self.data_changed.emit()
        
    def remove_locator_column(self, locator_name: str):
        """Удаляет столбец с указанным именем локатора"""
        col = self.get_locator_column_index(locator_name)
        if col == -1:
            print(f"Ошибка: столбец для локатора '{locator_name}' не найден")
            return

        # Удаляем столбец из таблицы
        self.table.removeColumn(col)

        # Удаляем запись из словаря
        del self.locator_columns[locator_name]

        # Обновляем индексы для столбцов, которые были правее удаленного
        for name in list(self.locator_columns.keys()):
            if self.locator_columns[name] > col:
                self.locator_columns[name] -= 1

        # Восстанавливаем настройки размеров
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        self.data_changed.emit()

    def clear_locator_columns(self):
        """Удаляет все добавленные столбцы локаторов"""
        for locator in list(self.locator_columns.keys()):
            self.remove_locator_column(locator)

    def rename_locator_column(self, old_name: str, new_name: str):
        """Переименовывает столбец локатора"""
        col = self.get_locator_column_index(old_name)
        if col == -1:
            print(f"Ошибка: столбец '{old_name}' не найден")
            return

        # Обновляем запись в словаре
        self.locator_columns[new_name] = self.locator_columns.pop(old_name)

        # Обновляем заголовок в таблице
        self.table.horizontalHeaderItem(col).setText(new_name)
        self.data_changed.emit()

    # Методы для доступа к данным извне
    def get_locator_column_index(self, locator_name: str) -> int:
        """Возвращает индекс столбца по имени локатора"""
        return self.locator_columns.get(locator_name, -1)

    def get_locator_value(self, locator_name: str, row: int) -> str:
        """Получить значение из конкретной ячейки"""
        col = self.get_locator_column_index(locator_name)
        if col != -1 and 0 <= row < self.table.rowCount():
            return self.table.item(row, col).text()
        return ""

    def set_locator_value(self, locator_name: str, row: int, value: str):
        """Установить значение в конкретную ячейку"""
        col = self.get_locator_column_index(locator_name)
        if col != -1 and 0 <= row < self.table.rowCount():
            item = self.table.item(row, col)
            if item:
                item.setText(str(value))

    def get_all_locator_data(self, locator_name: str) -> Dict[int, str]:
        """Получить все данные столбца в виде словаря {row: value}"""
        data = {}
        col = self.get_locator_column_index(locator_name)
        if col != -1:
            for row in range(self.table.rowCount()):
                item = self.table.item(row, col)
                if item:
                    data[row] = item.text()
        return data