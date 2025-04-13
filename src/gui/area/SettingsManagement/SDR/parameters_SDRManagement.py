from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QFrame, 
                              QComboBox, QLabel, QLineEdit, QPushButton)
from PySide6.QtCore import Qt, Property, Signal

from src.gui.styles.settings_management import main_settings

class CollapsibleHeader(QPushButton):
    toggled = Signal(bool)

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._expanded = True
        self._update_style()
        
        self.setFlat(True)
        self.setCursor(Qt.PointingHandCursor)
        self.clicked.connect(self.toggle)


    def _update_style(self):
        icon = "arrow_down.svg" if self._expanded else "arrow_right.svg"
        self.setStyleSheet(f"""
            QPushButton {{
                color: #000000;
                text-align: left;
                border: none;
                padding: 5px;
                font: bold 14px;
                icon: url(src/resources/icons/{icon});
                padding-left: 5px;
                width: 100px;
                height: 20px;
            }}""")

    def toggle(self):
        self._expanded = not self._expanded
        self._update_style()
        self.toggled.emit(self._expanded)

    @Property(bool)
    def expanded(self):
        return self._expanded

    @expanded.setter
    def expanded(self, value):
        if self._expanded != value:
            self._expanded = value
            self._update_style()

class Parameters(QWidget):
    def __init__(self, action_handler = None):
        super().__init__()
        self.action_handler = action_handler
        self.setContentsMargins(0, 0, 0, 0)
        self._setup_ui()
        self._update_size()

    def _update_size(self):
        self.setFixedWidth(580)
        
    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_frame = QFrame()
        main_frame.setStyleSheet(main_settings)
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)

        # Создаем заголовок
        self.header = CollapsibleHeader("Показатели")
        self.header.clicked.connect(self.toggle_content)
        frame_layout.addWidget(self.header)

        # Контейнер для содержимого
        self.content_container = QWidget()
        content_layout = QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(20, 0, 0, 0)
        
        # Добавляем виджеты в контейнер
        content_layout.addWidget(self._create_temp_parameter())
        content_layout.addWidget(self._create_voltage_parameter())
        content_layout.addWidget(self._create_current_parameter())
        content_layout.addWidget(self._create_rssi_parameter())
        content_layout.addWidget(self._create_pll_parameter())

        frame_layout.addWidget(self.content_container)
        main_layout.addWidget(main_frame)
        main_layout.addStretch()

    def toggle_content(self):
        self.content_container.setVisible(not self.content_container.isVisible())
        self.header.toggle()
        self._update_size()
        self.parent().adjustSize() 
        
    def _create_temp_parameter(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Температура чипа:        "))

        self.data_temp_sdr = QLineEdit()
        self.data_temp_sdr.setFixedWidth(350)
        self.data_temp_sdr.setReadOnly(True)  # Для отображения только для чтения
        layout.addWidget(self.data_temp_sdr)
        layout.addWidget(QLabel("°C"))

        return container

    def _create_voltage_parameter(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Напряжение питания:  "))

        self.data_voltage_sdr = QLineEdit()
        self.data_voltage_sdr.setFixedWidth(350)
        self.data_voltage_sdr.setReadOnly(True)
        layout.addWidget(self.data_voltage_sdr)
        layout.addWidget(QLabel("В"))

        return container

    def _create_current_parameter(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Потребляемый ток:       "))

        self.data_current_sdr = QLineEdit()
        self.data_current_sdr.setFixedWidth(350)
        self.data_current_sdr.setReadOnly(True)
        layout.addWidget(self.data_current_sdr)
        layout.addWidget(QLabel("мА"))

        return container

    def _create_rssi_parameter(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Уровень сигнала:           "))

        self.data_rssi_sdr = QLineEdit()
        self.data_rssi_sdr.setFixedWidth(350)
        self.data_rssi_sdr.setReadOnly(True)
        layout.addWidget(self.data_rssi_sdr)
        layout.addWidget(QLabel("dBm"))

        return container

    def _create_pll_parameter(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Статус блокировки PLL:"))

        self.data_pll_sdr = QLineEdit()
        self.data_pll_sdr.setFixedWidth(350)
        self.data_pll_sdr.setReadOnly(True)
        layout.addWidget(self.data_pll_sdr)
        layout.addWidget(QLabel("           "))

        return container