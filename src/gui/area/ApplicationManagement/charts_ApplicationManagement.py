from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                              QPushButton, QLabel)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal

from src.gui.styles.application_management import application, icon_button_style

class Charts(QWidget):
    buttonClicked = Signal(str, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(250, 120)
        self.buttons = {}
        self._setup_ui()
        
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        main_frame = QFrame()
        main_frame.setStyleSheet(application)
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setContentsMargins(5, 5, 5, 5)
        
        buttons_container = QWidget()
        buttons_container.setStyleSheet(icon_button_style)
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(5)

        buttons = [
            ("signal_button.svg", "Radar\nSignal", "radar_signal"),
            ("spectrum_button.svg", "Radar signal\nSpectrum", "radar_signal_spectrum"),
            ("snr_range_button.svg", "CNR vs\nRange", "snr_range")
        ]

        self.buttons = {}
        for icon, text, btn_id in buttons:
            btn = self._create_icon_button(icon, text, btn_id)
            self.buttons[btn_id] = btn
            buttons_layout.addWidget(btn)

        title = QLabel("АНАЛИЗ")
        title.setAlignment(Qt.AlignCenter)
        
        frame_layout.addWidget(buttons_container)
        frame_layout.addWidget(title)
        main_layout.addWidget(main_frame)

    def _create_icon_button(self, icon_path, text, button_id):
        container = QPushButton()
        container.setProperty("class", "icon_button")
        container.setObjectName(button_id)
        container.setCheckable(True)
        container.setFixedSize(70, 70)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 1, 0, 1)
        layout.setSpacing(5)

        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(f"src/resources/icons/{icon_path}").scaled(30, 30))
        icon_label.setAlignment(Qt.AlignCenter)

        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-family: "Roboto";
                font-size: 10px;
                font-weight: medium;
            }
        """)

        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()

        container.clicked.connect(lambda _, bid=button_id: self._handle_button_click(bid))
        return container

    def _handle_button_click(self, button_id):
        state = self.buttons[button_id].isChecked()
        self.buttonClicked.emit(button_id, state)