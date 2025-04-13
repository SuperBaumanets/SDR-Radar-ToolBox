from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                              QComboBox, QLabel, QLineEdit)

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QComboBox, QLineEdit

from src.gui.styles.settings_management import headline_settings

class Headline(QWidget):
    def __init__(self,  action_handler = None):
        super().__init__()
        self.action_handler = action_handler
        self.setFixedSize(580, 50)
        self._setup_ui()
        
    def _setup_ui(self):
        # Главный контейнер
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Основной фрейм
        main_frame = QFrame()
        main_frame.setStyleSheet(headline_settings)
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)

        # Добавляем компоненты
        frame_layout.addWidget(self._create_current_locator())
        frame_layout.addWidget(self._create_name_locator())

        main_layout.addWidget(main_frame)

    def _create_current_locator(self) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        layout.addWidget(QLabel("Текущий локатор:"))
        self.mode_locator = QComboBox()
        self.mode_locator.addItems([])
        layout.addWidget(self.mode_locator)

        if self.action_handler is not None:
            self.mode_locator.currentTextChanged.connect(self.action_handler.on_locator_selected)
        else:
            print("Ошибка: action_handler не инициализирован!")
        
        return container

    def _create_name_locator(self) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        layout.addWidget(QLabel("Имя:                          "))
        self.name_locator = QLineEdit()
        layout.addWidget(self.name_locator)

        if self.action_handler is not None:
            self.name_locator.textChanged.connect(self.action_handler.update_locator_name)
        else:
            print("Ошибка: action_handler не инициализирован!")
        
        return container