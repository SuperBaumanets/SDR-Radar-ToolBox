from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QFrame, 
                              QComboBox, QLabel, QLineEdit, QPushButton, QCheckBox)
from PySide6.QtCore import Qt, Property, Signal
from src.gui.styles.settings_management import antenna_settings

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

class Environment(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self._setup_ui()
        self._update_size()
    
    def _update_size(self):
        self.setFixedWidth(580)
    
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_frame = QFrame()
        main_frame.setStyleSheet(antenna_settings)
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)

        # Заголовок
        self.header = CollapsibleHeader("Атмосфера и поверхность")
        self.header.clicked.connect(self.toggle_content)
        frame_layout.addWidget(self.header)

        # Основной контент
        self.content_container = QWidget()
        content_layout = QVBoxLayout(self.content_container)
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(20, 0, 0, 0)

        # Постоянные элементы
        content_layout.addWidget(self._create_free_space_surface())

        # Контейнер для модели Земли
        self.earth_model_container = QWidget()
        self.earth_model_layout = QVBoxLayout(self.earth_model_container)
        self.earth_model_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self.earth_model_container)

        # Инициализация блока для модели Земли
        self._create_earth_model()

        frame_layout.addWidget(self.content_container)
        main_layout.addWidget(main_frame)

        # Инициализация видимости
        self._update_earth_visibility()

    def toggle_content(self):
        self.content_container.setVisible(not self.content_container.isVisible())
        self.header.toggle()
        self._update_size()
        self.parent().adjustSize() if self.parent() else None

    def _create_free_space_surface(self) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.free_space_check = QCheckBox("Свободное пространство")
        self.free_space_check.setChecked(True)
        self.free_space_check.toggled.connect(self._update_earth_visibility)
        layout.addWidget(self.free_space_check)

        return container

    def _create_earth_model(self):
        # Основной контейнер
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Выбор модели Земли
        mode_row = QWidget()
        mode_layout = QHBoxLayout(mode_row)
        mode_layout.addWidget(QLabel("Модель Земли:"))
        
        self.mode_earth_model = QComboBox()
        self.mode_earth_model.addItems(["Плоская", "Сферическая"])
        mode_layout.addWidget(self.mode_earth_model)
        
        main_layout.addWidget(mode_row)

        # Контейнер для сферической модели
        self.spherical_widget = self._create_curved()
        main_layout.addWidget(self.spherical_widget)

        self.earth_model_layout.addWidget(main_widget)

        # Связываем сигналы
        self.mode_earth_model.currentTextChanged.connect(self._update_earth_mode)
        self._update_earth_mode()

    def _create_curved(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 0, 0, 0)
        layout.setSpacing(0)

        # Выбор типа радиуса
        radius_row = QWidget()
        radius_layout = QHBoxLayout(radius_row)
        radius_layout.addWidget(QLabel("Эффективный радиус:"))
        
        self.mode_curved = QComboBox()
        self.mode_curved.addItems(["Автоматический", "Пользовательский"])
        radius_layout.addWidget(self.mode_curved)
        
        layout.addWidget(radius_row)

        # Автоматический радиус
        self.auto_widget = self._create_auto_curved()
        layout.addWidget(self.auto_widget)

        # Пользовательский радиус
        self.custom_widget = self._create_custom_curved()
        layout.addWidget(self.custom_widget)

        # Инициализация
        self.mode_curved.currentTextChanged.connect(self._update_radius_mode)
        self._update_radius_mode()

        return widget

    def _create_custom_curved(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(40, 0, 10, 0)

        layout.addWidget(QLabel("Эффективный радиус:"))
        self.manual_curved_input = QLineEdit()
        self.manual_curved_input.setFixedWidth(230)
        self.radius_unit = QComboBox()
        self.radius_unit.addItems(["м", "км"])
        self.radius_unit.setObjectName("measurement")
        
        layout.addWidget(self.manual_curved_input)
        layout.addWidget(self.radius_unit)

        return widget

    def _create_auto_curved(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(40, 0, 0, 0)
        layout.addWidget(QLabel("Эффективный радиус  6371                                                         км"))
        return widget

    def _update_earth_visibility(self):
        """Скрываем/показываем блок модели Земли"""
        self.earth_model_container.setVisible(not self.free_space_check.isChecked())
        self.parent().adjustSize() if self.parent() else None

    def _update_earth_mode(self):
        """Обновление видимости сферической модели"""
        is_spherical = self.mode_earth_model.currentText() == "Сферическая"
        self.spherical_widget.setVisible(is_spherical)
        self.parent().adjustSize() if self.parent() else None

    def _update_radius_mode(self):
        """Переключение между автоматическим и ручным радиусом"""
        is_auto = self.mode_curved.currentText() == "Автоматический"
        self.auto_widget.setVisible(is_auto)
        self.custom_widget.setVisible(not is_auto)
        self.parent().adjustSize() if self.parent() else None