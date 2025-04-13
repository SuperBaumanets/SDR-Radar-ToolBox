from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                              QPushButton, QLabel, QMenu, QWidgetAction, 
                              QComboBox, QLineEdit, QStackedWidget)
from PySide6.QtGui import QPixmap   
from PySide6.QtCore import Qt

from src.gui.styles.application_management import application, menu_btn, menu_item

class Metric(QWidget):
    def __init__(self, parent=None, action_handler = None):
        super().__init__(parent)
        self.setFixedSize(265, 120)
        self.action_handler = action_handler
        self.icon_metric = "distance_button.svg"
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
        
        # Cтековый виджет для переключения
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                border: 0px;
                background: transparent;
            }
        """)
        
        # Инициализация виджетов
        self.probability_widget = self._create_probability_detection()
        self.maximum_range_widget = self._create_maximum_range()
        self.stacked_widget.addWidget(self.probability_widget)
        self.stacked_widget.addWidget(self.maximum_range_widget)
        
        # Добавляем элементы
        content_layout.addWidget(self._create_metric_session())
        content_layout.addWidget(self.stacked_widget)

        # Заголовок 
        title = QLabel("МЕТРИКА")
        title.setAlignment(Qt.AlignCenter)
        
        # Собираем интерфейс
        frame_layout.addWidget(content_container)
        frame_layout.addWidget(title)

        main_layout.addWidget(main_frame)

        # Создаем меню и настраиваем виджет по умолчанию
        self._create_metric_menu()
        self.stacked_widget.setCurrentIndex(0)

    def _create_metric_session(self) -> QWidget:
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
        self.icon_label.setPixmap(QPixmap(f"src/resources/icons/{self.icon_metric}").scaled(40, 40))
        self.icon_label.setAlignment(Qt.AlignCenter)

        text_label = QLabel("Метрика")
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

    def _create_metric_menu(self):
        menu = QMenu(self)
        menu.setObjectName("metricTitle")
        menu.setStyleSheet(menu_item)

        # Создаем действия меню
        action_probability = self._create_menu_item_label(
            "Вычисление вероятности обнаружения", 
            "Вычислить вероятность обнаружения и другие\nпоказатели с ограничением максимального диапазона"
        )
        action_maximum = self._create_menu_item_label(
            "Вычисление максимальной дальности", 
            "Вычислить максимальную дальность и другие показатели с вероятностью обнаружения"
        )
        
        # Подключаем переключение виджетов
        action_probability.triggered.connect(
            lambda: [
                self.stacked_widget.setCurrentWidget(self.probability_widget),
                self._update_icon("distance_button.svg")
            ]
        )
        action_maximum.triggered.connect(
            lambda: [
                self.stacked_widget.setCurrentWidget(self.maximum_range_widget),
                self._update_icon("ruler.svg")
            ]
        )
        
        menu.addAction(action_probability)
        menu.addAction(action_maximum)
        self.btn_metric.setMenu(menu)

    def _create_probability_detection(self) -> QWidget:
        container = QWidget()
    
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(0, 5, 10, 0)
        main_layout.setSpacing(3)

        label = QLabel("Максимальная дальность")
        main_layout.addWidget(label)

        self.data_range = QLineEdit()
        self.data_range.setPlaceholderText("Введите значение...")
        main_layout.addWidget(self.data_range)
        
        self.measurement_range = QComboBox()
        self.measurement_range.addItems(["км", "м"])
        main_layout.addWidget(self.measurement_range)

        main_layout.addStretch()

        if self.action_handler is not None:
            self.measurement_range.currentTextChanged.connect(self.action_handler.update_maximum_range)
            self.data_range.textChanged.connect(self.action_handler.update_maximum_range)
        else:
            print("Ошибка: action_handler не инициализирован!")

        return container
    
    def _create_maximum_range(self) -> QWidget:
        container = QWidget()

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(0, 5, 10, 0)
        main_layout.setSpacing(3)

        label = QLabel("Вероятность обнаружения")
        main_layout.addWidget(label)

        self.edit_probability_detection = QLineEdit()
        self.edit_probability_detection.setPlaceholderText("Введите значение...")
        main_layout.addWidget(self.edit_probability_detection)
        
        self.combo_change_unit = QComboBox()
        self.combo_change_unit.addItems(["Decimal"])
        main_layout.addWidget(self.combo_change_unit)

        main_layout.addStretch()

        return container

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
    
    def _update_icon(self, icon_name: str):
        """Обновление иконки кнопки"""
        self.icon_label.setPixmap(QPixmap(f"src/resources/icons/{icon_name}").scaled(40, 40))