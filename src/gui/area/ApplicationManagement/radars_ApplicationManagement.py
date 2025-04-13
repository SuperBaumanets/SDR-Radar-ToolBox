from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                              QPushButton, QLabel, QComboBox)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize

from src.gui.styles.application_management import application, menu_btn
from src.core.processing.ApplicationManagement.radar_action import LocatorActionHandler

class Radars(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(220, 120)
        self._setup_ui()
        
    def _setup_ui(self):
        # Главный контейнер
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Основной фрейм
        main_frame = QFrame()
        main_frame.setStyleSheet(application)
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        
        # Контейнер для иконок
        icons_container = QWidget()
        icons_layout = QHBoxLayout(icons_container)
        icons_layout.setContentsMargins(0, 0, 0, 0)
        icons_layout.setSpacing(0)
        
        # Добавляем элементы
        icons_layout.addWidget(self._create_add_radar())
        icons_layout.addWidget(self._create_management_radar())
    
        # Заголовок 
        title = QLabel("РАДАРЫ")
        title.setAlignment(Qt.AlignCenter)
        
        # Собираем интерфейс
        frame_layout.addWidget(icons_container)
        frame_layout.addWidget(title)

        main_layout.addWidget(main_frame)

    def _create_add_radar(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 5, 0)
        layout.setSpacing(0)
        
        self.btn_add_locator = QPushButton()
        self.btn_add_locator.clicked.connect(lambda: self._add_new_locator_action())
        self.btn_add_locator.setStyleSheet(menu_btn)
        self.btn_add_locator.setIcon(QIcon(QPixmap("src/resources/icons/add_radar.svg")))
        self.btn_add_locator.setIconSize(QSize(40, 40))
        
        label = QLabel("Добавить\nРадар")
        label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.btn_add_locator, alignment=Qt.AlignCenter)
        layout.addWidget(label)

        layout.addStretch()

        return container

    def _create_management_radar(self) -> QWidget:
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(0, 5, 10, 5)
        main_layout.setSpacing(10)

        self.combo_open_session = QComboBox()
        self.combo_open_session.addItems(["Открыть\nСессию"])
        main_layout.addWidget(self.combo_open_session)

        duplicate = QWidget()
        duplicate_layout = QHBoxLayout(duplicate)
        duplicate_layout.setContentsMargins(10, 0, 0, 0)

        self.btn_duplicate = QPushButton("Дублировать")
        self.btn_duplicate.clicked.connect(lambda: self._duplicate_locator_action())
        self.btn_duplicate.setObjectName("delete_duplicate")
        self.btn_duplicate.setStyleSheet(menu_btn)
        self.btn_duplicate.setIcon(QIcon("src/resources/icons/duplicate_button.svg"))
        self.btn_duplicate.setIconSize(QSize(20, 20))

        duplicate_layout.addWidget(self.btn_duplicate)
        main_layout.addWidget(duplicate)
        duplicate_layout.addStretch()

        delete = QWidget()
        delete_layout = QHBoxLayout(delete)
        delete_layout.setContentsMargins(10, 0, 0, 0)

        self.btn_delete = QPushButton("Удалить          ")
        self.btn_delete.clicked.connect(lambda: self._delete_locator_action())
        self.btn_delete.setObjectName("delete_duplicate")
        self.btn_delete.setStyleSheet(menu_btn)
        self.btn_delete.setIcon(QIcon("src/resources/icons/delete_button.svg"))
        self.btn_delete.setIconSize(QSize(18, 18))

        delete_layout.addWidget(self.btn_delete, alignment=Qt.AlignLeft)
        main_layout.addWidget(delete)
        delete_layout.addStretch()

        main_layout.addStretch()

        return container
    
    def _add_new_locator_action(self):
        LocatorActionHandler.add_locator()

    def _duplicate_locator_action(self):
        LocatorActionHandler.duplicate_locator()

    def _delete_locator_action(self):
        LocatorActionHandler.delete_locator()
