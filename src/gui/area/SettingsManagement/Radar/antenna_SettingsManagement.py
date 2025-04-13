from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QFrame, 
                              QComboBox, QLabel, QLineEdit, QPushButton)
from PySide6.QtCore import Qt, Property, Signal
from src.gui.styles.settings_management import antenna_settings
import math

class CollapsibleHeader(QPushButton):
    toggled = Signal(bool)  # Добавляем сигнал
    
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
                width: 210px;
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

class Antenna(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self._setup_ui()
        self._update_size()
    
    def _update_size(self):
        self.setFixedWidth(580)
        
    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_frame = QFrame()
        main_frame.setStyleSheet(antenna_settings)
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)

        # Заголовок
        self.header = CollapsibleHeader("Антенна и сканирование")
        self.header.clicked.connect(self.toggle_content)
        frame_layout.addWidget(self.header)

        # Основной контейнер
        self.content_container = QWidget()
        content_layout = QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(20, 0, 0, 0)
        
        # Постоянные элементы
        content_layout.addWidget(self._create_height_antenna())
        content_layout.addWidget(self._create_tilt_angle_antenna())
        content_layout.addWidget(self._create_polarization_antenna())
        
        # Динамический блок для усиления
        self.gain_container = QWidget()
        gain_layout = QVBoxLayout(self.gain_container)
        gain_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self.gain_container)
        
        # Инициализация блоков усиления
        self._create_trnsmt_gain_antenna()
        
        frame_layout.addWidget(self.content_container)
        main_layout.addWidget(main_frame)
        #main_layout.addStretch()

    def toggle_content(self):
        self.content_container.setVisible(not self.content_container.isVisible())
        self.header.toggle()
        self._update_size()
        self.parent().adjustSize()  # Обновляем размер родительского контейнера

    def _create_height_antenna(self) -> QWidget:
        container = QWidget()
        self.layout = QHBoxLayout(container)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(QLabel("Высота антенны:                     "))

        self.data_height = QLineEdit()
        self.data_height.setFixedWidth(259)
        self.layout.addWidget(self.data_height)

        self.measurement_height = QComboBox()
        self.measurement_height.setObjectName("measurement")
        self.measurement_height.addItems(["м", "км"])

        self.layout.addWidget(self.measurement_height)

        return container
    
    def _create_tilt_angle_antenna(self) -> QWidget:
        container = QWidget()
        self.layout = QHBoxLayout(container)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(QLabel("Угол наклона антенны:         "))

        self.data_angle = QLineEdit()
        self.data_angle.setFixedWidth(259)
        self.layout.addWidget(self.data_angle)

        self.measurement_angle= QComboBox()
        self.measurement_angle.setObjectName("measurement")
        self.measurement_angle.addItems(["градус", "радианы"])

        self.layout.addWidget(self.measurement_angle)

        return container
    
    def _create_polarization_antenna(self) -> QWidget:
        container = QWidget()
        self.layout = QHBoxLayout(container)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(QLabel("Тип поляризации антенны:"))

        self.measurement_polarization= QComboBox()
        self.measurement_polarization.addItems(["Горизонтальная", "Вертикальная"])
        self.measurement_polarization.setStyleSheet("antenna_settings")

        self.layout.addWidget(self.measurement_polarization)

        return container
    
    def _create_trnsmt_gain_antenna(self) -> QWidget:
        # Основной контейнер для управления усилением
        main_gain_widget = QWidget()
        gain_layout = QVBoxLayout(main_gain_widget)
        gain_layout.setContentsMargins(0, 0, 0, 0)

        # Выбор режима
        mode_row = QWidget()
        mode_layout = QHBoxLayout(mode_row)
        mode_layout.setContentsMargins(0, 0, 0, 0)

        mode_layout.addWidget(QLabel("Входной КУ антенны:"))

        self.mode_trnsmt_gain = QComboBox()
        self.mode_trnsmt_gain.addItems(["Задать вручную", "От ширины луча"])
        self.mode_trnsmt_gain.setStyleSheet("antenna_settings")

        mode_layout.addWidget(self.mode_trnsmt_gain)
        gain_layout.addWidget(mode_row)

        # Контейнеры для разных режимов
        self.manual_widget = self._create_manual_gain()
        self.beam_widget = self._create_beam_gain()
        
        gain_layout.addWidget(self.manual_widget)
        gain_layout.addWidget(self.beam_widget)
        
        self.gain_container.layout().addWidget(main_gain_widget)
        
        # Инициализация состояния
        self._update_trnsmt_gain_units(self.mode_trnsmt_gain.currentText())
        self.mode_trnsmt_gain.currentTextChanged.connect(self._update_trnsmt_gain_units)

        # Связываем сигналы
        self.mode_trnsmt_gain.currentTextChanged.connect(self._update_trnsmt_gain_units)
    
    def _create_manual_gain(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(20, 0, 0, 0)

        layout.addWidget(QLabel("Gain:"))

        self.manual_gain_input = QLineEdit()
    
        layout.addWidget(self.manual_gain_input)
        layout.addWidget(QLabel("дБи"))

        return widget
    
    def _create_beam_gain(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 0, 0, 0)
        layout.setSpacing(0)

        # Азимут
        az_row = QWidget()
        az_layout = QHBoxLayout(az_row)
        az_layout.setContentsMargins(0, 0, 0, 0)

        az_layout.addWidget(QLabel("Ширина по азимуту:     "))

        self.azimuth_input = QLineEdit()
        az_layout.addWidget(self.azimuth_input)

        self.azimuth_units = QComboBox()
        self.azimuth_units.addItems(["градус", "радианы"])
        self.azimuth_units.setObjectName("measurement")

        az_layout.addWidget(self.azimuth_units)
        layout.addWidget(az_row)

        # Угол места
        el_row = QWidget()
        el_layout = QHBoxLayout(el_row)
        el_layout.setContentsMargins(0, 0, 0, 0)

        el_layout.addWidget(QLabel("Ширина по углу места:"))

        self.elevation_input = QLineEdit()
        el_layout.addWidget(self.elevation_input)
        
        self.elevation_units = QComboBox()
        self.elevation_units.addItems(["градус", "радианы"])
        self.elevation_units.setObjectName("measurement")

        el_layout.addWidget(self.elevation_units)
        layout.addWidget(el_row)

        self.azimuth_input.textChanged.connect(self._calculate_gain)
        self.elevation_input.textChanged.connect(self._calculate_gain)
        self.azimuth_units.currentTextChanged.connect(self._calculate_gain)
        self.elevation_units.currentTextChanged.connect(self._calculate_gain)

        # Результат
        res_row = QWidget()
        res_layout = QHBoxLayout(res_row)
        res_layout.setContentsMargins(0, 0, 0, 0)

        res_layout.addWidget(QLabel("Усиление:"))

        self.calculated_gain = QLabel("0.00")
        res_layout.addWidget(self.calculated_gain)
        res_layout.addWidget(QLabel("дБи"))

        layout.addWidget(res_row)

        return widget

    def _update_trnsmt_gain_units(self, text):
        is_manual = text == "Задать вручную"
        
        # Управление видимостью
        self.manual_widget.setVisible(is_manual)
        self.beam_widget.setVisible(not is_manual)
        
        # Фиксируем размеры
        self.manual_widget.setFixedHeight(30 if is_manual else 0)
        self.beam_widget.setFixedHeight(100 if not is_manual else 0)
        
        if not is_manual:
            self._calculate_gain()

    def _calculate_gain(self):
        if self.azimuth_input.text() == '' or self.elevation_input.text() == '':
            return

        az = float(self.azimuth_input.text())
        el = float(self.elevation_input.text())
        
        if self.azimuth_units.currentText() == "радианы":
            az = math.degrees(az)
        if self.elevation_units.currentText() == "радианы":
            el = math.degrees(el)
            
        gain = 10 * math.log10((41253) / (az * el))
        self.calculated_gain.setText(f"{gain:.2f}")