# custom_dialogs.py
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

class CustomSessionDialog(QDialog):
    save_and_continue = Signal()
    continue_without_saving = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Radar Simulator")
        self.setFixedSize(450, 120)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Текст сообщения
        self.label = QLabel("Сохранить сессию до создания новой сессии?")
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setStyleSheet("font-family: 'Roboto'; font-size: 14px; color: #000000;")
        
        # Кнопки
        btn_layout = QHBoxLayout()
        self.btn_yes = QPushButton("Да")
        self.btn_no = QPushButton("Нет")
        self.btn_cancel = QPushButton("Отмена")
        
        # Стилизация
        button_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #BEBEBE, stop:0.3 #D8D8D8, stop:0.7 #D8D8D8, stop:1 #BEBEBE);
                border: 1px solid #000000;
                border-radius: 2px;
                font-family: "Roboto";
                font-size: 14px;
                color: #000000;
                min-width: 90px;
                padding: 5px;
            }
            QPushButton:hover { background: #C8C8C8; }
        """
        for btn in [self.btn_yes, self.btn_no, self.btn_cancel]:
            btn.setStyleSheet(button_style)
        
        # Сигналы
        self.btn_yes.clicked.connect(self._on_yes)
        self.btn_no.clicked.connect(self._on_no)
        self.btn_cancel.clicked.connect(self.reject)
        
        # Сборка
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_yes)
        btn_layout.addWidget(self.btn_no)
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addStretch()
        
        layout.addWidget(self.label)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def _on_yes(self):
        self.save_and_continue.emit()
        self.accept()
    
    def _on_no(self):
        self.continue_without_saving.emit()
        self.accept()