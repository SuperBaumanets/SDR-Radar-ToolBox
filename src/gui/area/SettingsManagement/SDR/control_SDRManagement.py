from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QFrame, 
                               QLabel, QLineEdit, QPushButton)
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
                width: 120px;
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

class Control(QWidget):
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
        self.header = CollapsibleHeader("Управление")
        self.header.clicked.connect(self.toggle_content)
        frame_layout.addWidget(self.header)

        # Контейнер для содержимого
        self.content_container = QWidget()
        content_layout = QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(20, 0, 0, 0)
        
        # Добавляем виджеты в контейнер
        content_layout.addWidget(self._create_connect_sdr())
        content_layout.addWidget(self._create_run_signal_sdr())
        content_layout.addWidget(self._create_stop_signal_sdr())

        frame_layout.addWidget(self.content_container)
        main_layout.addWidget(main_frame)
        main_layout.addStretch()

    def toggle_content(self):
        self.content_container.setVisible(not self.content_container.isVisible())
        self.header.toggle()
        self._update_size()
        self.parent().adjustSize() 
        
    def _create_connect_sdr(self) -> QWidget:
        container = QWidget()
        self.layout = QHBoxLayout(container)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(QLabel("Стандартный IP-адрес PlutoSDR:"))
        self.data_sdr = QLineEdit()
        self.layout.addWidget(self.data_sdr)

        self.connection_indicator = QLabel()
        self.connection_indicator.setFixedSize(20, 20)  
        self.status_connect = "red"
        self.connection_indicator.setStyleSheet(
            f"background-color: {self.status_connect};"
            "border-radius: 10px;"
            "border: 2px solid darkgray;"
        )
        self.layout.addWidget(self.connection_indicator)

        if self.action_handler is not None:
            self.data_sdr.textChanged.connect(self.action_handler.setup_ip_sdr)
        else:
            print("Ошибка: action_handler не инициализирован!")

        return container
 
    def _create_run_signal_sdr(self) -> QWidget:
        container = QWidget()
        self.layout = QHBoxLayout(container)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(QLabel("Запуск передачи сигнала:"))

        self.start_button = QPushButton("Старт")
        self.start_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #BEBEBE, stop:0.3 #D8D8D8, stop:0.7 #D8D8D8, stop:1 #BEBEBE);
                border: 1px solid #000000;
                border-radius: 2px;
                font-family: "Roboto";
                font-size: 14px;
                color: #000000;
                width: 30px;
                height: 18px;
                padding: 2px;
            }
            QPushButton:hover { background: #C8C8C8; }
        """)
        self.layout.addWidget(self.start_button)

        if self.action_handler is not None:
            self.start_button.clicked.connect(self.action_handler.start_transmission)
        else:
            print("Ошибка: action_handler не инициализирован!")

        return container
    
    def _create_stop_signal_sdr(self) -> QWidget:
        container = QWidget()
        self.layout = QHBoxLayout(container)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(QLabel("Остановка передачи сигнала:"))

        self.stop_button = QPushButton("Стоп")
        self.stop_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #BEBEBE, stop:0.3 #D8D8D8, stop:0.7 #D8D8D8, stop:1 #BEBEBE);
                border: 1px solid #000000;
                border-radius: 2px;
                font-family: "Roboto";
                font-size: 14px;
                color: #000000;
                width: 30px;
                height: 18px;
                padding: 2px;
            }
            QPushButton:hover { background: #C8C8C8; }
        """)
        self.layout.addWidget(self.stop_button)

        if self.action_handler is not None:
            self.stop_button.clicked.connect(self.action_handler.stop_transmission)
        else:
            print("Ошибка: action_handler не инициализирован!")

        return container