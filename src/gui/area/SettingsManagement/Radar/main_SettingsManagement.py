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

class Main(QWidget):
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
        self.header = CollapsibleHeader("Главная")
        self.header.clicked.connect(self.toggle_content)
        frame_layout.addWidget(self.header)

        # Контейнер для содержимого
        self.content_container = QWidget()
        content_layout = QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(20, 0, 0, 0)
        
        # Добавляем виджеты в контейнер
        content_layout.addWidget(self._create_freq_wavelength_locator())
        content_layout.addWidget(self._create_pulse_bandwidth_locator())
        content_layout.addWidget(self._create_power_locator())
        content_layout.addWidget(self._create_pulse_duty_locator())
        content_layout.addWidget(self._create_PRI_PRF_locator())

        frame_layout.addWidget(self.content_container)
        main_layout.addWidget(main_frame)
        main_layout.addStretch()

    def toggle_content(self):
        self.content_container.setVisible(not self.content_container.isVisible())
        self.header.toggle()
        self._update_size()
        self.parent().adjustSize() 
        
    def _create_freq_wavelength_locator(self) -> QWidget:
        container = QWidget()
        self.layout = QHBoxLayout(container)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.mode_freq_wavelength = QComboBox()
        self.mode_freq_wavelength.addItems(["Длина волны", "Частота"])
        self.mode_freq_wavelength.currentTextChanged.connect(self._update_freq_wavelength_units)
        self.layout.addWidget(self.mode_freq_wavelength)

        self.data_freq_period = QLineEdit()
        self.layout.addWidget(self.data_freq_period)

        self.measurement_wavelength = QComboBox()
        self.measurement_wavelength.setObjectName("measurement")
        self.measurement_wavelength.addItems(["м", "см", "мм"])
        
        self.measurement_freq = QComboBox()
        self.measurement_freq.setObjectName("measurement")
        self.measurement_freq.addItems(["Гц", "кГц", "МГц", "ГГц"])

        self.layout.addWidget(self.measurement_wavelength)
        self.layout.addWidget(self.measurement_freq)
        self.measurement_wavelength.hide()

        if self.action_handler is not None:
            self.mode_freq_wavelength.currentTextChanged.connect(self.action_handler.update_freq_wavelength)
            self.measurement_wavelength.currentTextChanged.connect(self.action_handler.update_freq_wavelength)
            self.measurement_freq.currentTextChanged.connect(self.action_handler.update_freq_wavelength)
            self.data_freq_period.textChanged.connect(self.action_handler.update_freq_wavelength)
        else:
            print("Ошибка: action_handler не инициализирован!")

        return container
    
    def _create_pulse_bandwidth_locator(self) -> QWidget:
        container = QWidget()
        self.layout = QHBoxLayout(container)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(QLabel("Полоса пропускания:           "))

        self.data_bandwidth = QLineEdit()
        self.layout.addWidget(self.data_bandwidth)

        self.measurement_bandwidth = QComboBox()
        self.measurement_bandwidth.setObjectName("measurement")
        self.measurement_bandwidth.addItems(["Гц", "кГц", "МГц", "ГГц"])

        self.layout.addWidget(self.measurement_bandwidth)

        if self.action_handler is not None:
            self.data_bandwidth.textChanged.connect(self.action_handler.update_bandwidth)
            self.measurement_bandwidth.currentTextChanged.connect(self.action_handler.update_bandwidth)
        else:
            print("Ошибка: action_handler не инициализирован!")

        return container
    
    def _create_power_locator(self) -> QWidget:
        container = QWidget()
        self.layout = QHBoxLayout(container)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.mode_power = QComboBox()

        self.mode_power.addItems(["Пиковая мощность", "Средняя мощность"])
        self.layout.addWidget(self.mode_power)

        self.data_power = QLineEdit()
        self.layout.addWidget(self.data_power)

        self.measurement_power = QComboBox()
        self.measurement_power.setObjectName("measurement")
        self.measurement_power.addItems(["Вт", "кВт", "МВт", "дБВт", "дБм"])

        if self.action_handler is not None:
            self.mode_power.currentTextChanged.connect(self.action_handler.update_power)
            self.measurement_power.currentTextChanged.connect(self.action_handler.update_power)
            self.data_power.textChanged.connect(self.action_handler.update_power)
        else:
            print("Ошибка: action_handler не инициализирован!")

        self.layout.addWidget(self.measurement_power)

        return container
    
    def _create_pulse_duty_locator(self) -> QWidget:
        container = QWidget()
        self.layout = QHBoxLayout(container)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.mode_pulse_duty = QComboBox()
        self.mode_pulse_duty.addItems(["Ширина импульса", "Скважность"])
        self.mode_pulse_duty.currentTextChanged.connect(self._update_pulse_duty_units)
        self.layout.addWidget(self.mode_pulse_duty)

        self.data_pulse_duty = QLineEdit()
        self.layout.addWidget(self.data_pulse_duty)

        self.measurement_pulse = QComboBox()
        self.measurement_pulse.setObjectName("measurement")
        self.measurement_pulse.addItems(["с", "мс", "мкс"])

        self.church = QLabel("                          ")
        self.layout.addWidget(self.church)
        self.church.hide()

        self.layout.addWidget(self.measurement_pulse)

        if self.action_handler is not None:
            self.mode_pulse_duty.currentTextChanged.connect(self.action_handler.update_pulse_duty)
            self.measurement_pulse.currentTextChanged.connect(self.action_handler.update_pulse_duty)
            self.data_pulse_duty.textChanged.connect(self.action_handler.update_pulse_duty)
        else:
            print("Ошибка: action_handler не инициализирован!")

        return container
    
    def _create_PRI_PRF_locator(self) -> QWidget:
        container = QWidget()
        self.layout = QHBoxLayout(container)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.mode_freq_period = QComboBox()
        self.mode_freq_period.addItems(["PRI", "PRF"])
        self.mode_freq_period.currentTextChanged.connect(self._update_freq_period_units)
        self.layout.addWidget(self.mode_freq_period)

        self.data_PRI_PRF = QLineEdit()
        self.layout.addWidget(self.data_PRI_PRF)

        self.measurement_period_repeat = QComboBox()
        self.measurement_period_repeat.setObjectName("measurement")
        self.measurement_period_repeat.addItems(["с", "мс", "мкс"])
        
        self.measurement_freq_repeat = QComboBox()
        self.measurement_freq_repeat.setObjectName("measurement")
        self.measurement_freq_repeat.addItems(["Гц", "кГц", "МГц"])

        self.layout.addWidget(self.measurement_period_repeat)
        self.layout.addWidget(self.measurement_freq_repeat)
        self.measurement_period_repeat.hide()

        if self.action_handler is not None:
            self.mode_freq_period.currentTextChanged.connect(self.action_handler.update_pri_prf)
            self.measurement_period_repeat.currentTextChanged.connect(self.action_handler.update_pri_prf)
            self.measurement_freq_repeat.currentTextChanged.connect(self.action_handler.update_pri_prf)
            self.data_PRI_PRF.textChanged.connect(self.action_handler.update_pri_prf)
        else:
            print("Ошибка: action_handler не инициализирован!")

        return container

    def _update_freq_wavelength_units(self, text):
        if text == "Длина волны":
            self.measurement_wavelength.show()
            self.measurement_freq.hide()
        else:
            self.measurement_wavelength.hide()
            self.measurement_freq.show()

    def _update_pulse_duty_units(self, text):
        if text == "Скважность":
            self.measurement_pulse.hide()
            self.church.show()
        else:
            self.measurement_pulse.show()
            self.church.hide()

    def _update_freq_period_units(self, text):
        if text == "PRI":
            self.measurement_period_repeat.show()
            self.measurement_freq_repeat.hide()
        else:
            self.measurement_period_repeat.hide()
            self.measurement_freq_repeat.show()
