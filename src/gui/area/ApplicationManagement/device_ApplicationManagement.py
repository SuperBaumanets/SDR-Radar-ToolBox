from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                              QPushButton, QLabel, QMenu, QWidgetAction, 
                              QComboBox, QLineEdit, QStackedWidget)
from PySide6.QtGui import QPixmap   
from PySide6.QtCore import Qt, Signal

from src.gui.styles.application_management import application, menu_btn, menu_item

class Device(QWidget):
    toggle_sdr_tab = Signal()

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
        
        # Контейнер для иконок и виджетов
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Добавляем элементы
        content_layout.addWidget(self._create_device_session())

        # Заголовок 
        title = QLabel("УСТРОЙСТВА")
        title.setAlignment(Qt.AlignCenter)
        
        # Собираем интерфейс
        frame_layout.addWidget(content_container)
        frame_layout.addWidget(title)

        main_layout.addWidget(main_frame)

        self.btn_metric.clicked.connect(self._handle_button_click)

    def _create_device_session(self) -> QWidget:
        container = QWidget()
        container.setStyleSheet("background: transparent;")

        self.btn_metric = QPushButton()
        self.btn_metric.setObjectName("metric_button")
        self.btn_metric.setStyleSheet(f"""
            {menu_btn}
            QPushButton#metric_button {{
                qproperty-iconSize: 40px;
                width: 60px;
                height: 100px;
            }}
            QPushButton::menu-indicator {{ image: none; }}
        """)

        layout = QVBoxLayout(self.btn_metric)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.icon_label = QLabel()
        self.icon_label.setPixmap(QPixmap(f"src/resources/icons/SDR_button.svg").scaled(40, 40))
        self.icon_label.setAlignment(Qt.AlignCenter)

        text_label = QLabel("Запуск на\nSDR")
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
    
    def _handle_button_click(self):
        self.toggle_sdr_tab.emit()