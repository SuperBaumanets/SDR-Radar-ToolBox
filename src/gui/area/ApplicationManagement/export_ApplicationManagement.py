from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                              QPushButton, QLabel, QMenu, QWidgetAction)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize

from src.gui.styles.application_management import application, menu_btn, menu_item

class Export(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 120)
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
        icons_layout.addWidget(self._create_export_session())

        # Заголовок 
        title = QLabel("ЭКСПОРТ")
        title.setAlignment(Qt.AlignCenter)
        
        # Собираем интерфейс
        frame_layout.addWidget(icons_container)
        frame_layout.addWidget(title)

        main_layout.addWidget(main_frame)

        # Создаем меню для каждой кнопки
        self._create_export_session_menu()

    def _create_export_session(self) -> QWidget:
        container = QWidget()
        container.setStyleSheet("background: transparent;")

        self.btn_metric = QPushButton()
        self.btn_metric.setObjectName("metric_button")
        self.btn_metric.setStyleSheet(f"""
            {menu_btn}
            QPushButton#metric_button {{
                qproperty-iconSize: 40px;
                width: 40px;
                height: 100px;
            }}
            QPushButton::menu-indicator {{ image: none; }}
        """)

        layout = QVBoxLayout(self.btn_metric)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.icon_label = QLabel()
        self.icon_label.setPixmap(QPixmap(f"src/resources/icons/export.svg").scaled(40, 40))
        self.icon_label.setAlignment(Qt.AlignCenter)

        text_label = QLabel("Экспорт")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-family: "Roboto";
                font-size: 12px;
            }
        """)

        layout.addWidget(self.icon_label)
        layout.addWidget(text_label)

        container_layout = QVBoxLayout(container)
        container_layout.addWidget(self.btn_metric)

        return container
    
    def _create_export_session_menu(self):
        menu = QMenu(self)
        menu.setObjectName("ExportTitle")
        menu.setStyleSheet(menu_item)

        # Создаем действия меню
        export_python = self._create_menu_item_label(
            "Экспортировать локатор как класс Python", 
            "Создание Python-класса локатора с полученными\n характеристиками. Класс обеспечит интеграцию в скрипты и\nподдержку быстрого прототипирования"
        )
        export_cpp = self._create_menu_item_label(
            "Экспортировать локатор как класс C++", 
            "Создание С++ класса локатора с полученными\n характеристиками. Класс обеспечит интеграцию в различные\nстенды и поддержку быстрого прототипирования"
        )
        
        menu.addAction(export_python)
        menu.addAction(export_cpp)

        self.btn_metric.setMenu(menu)

    def _create_menu_item_label(self, title, text):
        widget_action = QWidgetAction(self)
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 10, 5)

        label_title = QLabel(title)
        label_title.setObjectName("metricTitle")
        label_title.setStyleSheet(menu_item)
        
        label_text = QLabel(text)
        label_text.setStyleSheet(menu_item)
        
        layout.addWidget(label_title)
        layout.addWidget(label_text)
        layout.addStretch()
        
        widget_action.setDefaultWidget(widget)
        return widget_action
