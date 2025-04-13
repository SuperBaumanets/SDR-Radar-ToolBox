from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                              QPushButton, QLabel, QMenu, QWidgetAction)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize

from src.gui.styles.application_management import application, menu_btn, menu_item
from src.core.processing.ApplicationManagement.file_action import FileActionHandler

class File(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(240, 120)
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
        icons_layout.addWidget(self._create_new_session())
        icons_layout.addWidget(self._create_open_session())
        icons_layout.addWidget(self._create_save_session())

        # Заголовок 
        title = QLabel("ФАЙЛ")
        title.setAlignment(Qt.AlignCenter)
        
        # Собираем интерфейс
        frame_layout.addWidget(icons_container)
        frame_layout.addWidget(title)

        main_layout.addWidget(main_frame)

        # Создаем меню для каждой кнопки
        self._create_new_session_menu()
        self._create_open_session_menu()
        self._create_save_session_menu()

    def _create_new_session(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.btn_new_session = QPushButton()
        self.btn_new_session.clicked.connect(lambda: self._create_new_session_action(None))
        self.btn_new_session.setStyleSheet(menu_btn)
        self.btn_new_session.setIcon(QIcon(QPixmap("src/resources/icons/add_button.svg")))
        self.btn_new_session.setIconSize(QSize(40, 40))
        
        self.btn_new_menu = QPushButton("Новая\nСессия")
        self.btn_new_menu.setStyleSheet(menu_btn)
        self.btn_new_menu.setFixedSize(60, 40)
        
        layout.addWidget(self.btn_new_session, alignment=Qt.AlignCenter)
        layout.addWidget(self.btn_new_menu)

        layout.addStretch()

        return container
    
    def _create_new_session_menu(self):
        """Меню для кнопки 'Новая Сессия'"""
        menu = QMenu(self)
        menu.setObjectName("openNewSessionMenu")
        menu.setStyleSheet(menu_item)
        
        aeroport_locator_action = self._create_menu_item_label_svg("Аэродромный локатор", "aeroport_locator.svg")
        aeroport_locator_action.triggered.connect(lambda: self._create_new_session_action(0))
        
        menu.addAction(aeroport_locator_action)
        
        self.btn_new_menu.setMenu(menu)

    def _create_open_session(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.btn_open_session = QPushButton()
        self.btn_open_session.clicked.connect(lambda: self._create_open_session_action(None))
        self.btn_open_session.setStyleSheet(menu_btn)
        self.btn_open_session.setIcon(QIcon(QPixmap("src/resources/icons/folder_button.svg")))
        self.btn_open_session.setIconSize(QSize(40, 40))
        
        self.btn_open_menu = QPushButton("Открыть\nСессию")
        self.btn_open_menu.setStyleSheet(menu_btn)
        self.btn_open_menu.setFixedSize(65, 40)
        
        layout.addWidget(self.btn_open_session, alignment=Qt.AlignCenter)
        layout.addWidget(self.btn_open_menu)

        layout.addStretch()

        return container
    
    def _create_open_session_menu(self):
        menu = QMenu(self)
        menu.setObjectName("openSessionMenu")
        menu.setStyleSheet(menu_item)

        label_open_session = self._create_menu_item_label("  ОТКРЫТЬ                        ")
        
        action_open_session = self._create_menu_item_label_svg("Открыть файл", "folder_button.svg")
        action_open_session.triggered.connect(lambda: self._create_open_session_action(0))
        
        label_resent_files = self._create_menu_item_label("  НЕДАВНИЕ ФАЙЛЫ      ")

        menu.addAction(label_open_session)
        menu.addAction(action_open_session)
        menu.addAction(label_resent_files)

        recent_files = ["test1"]
        if recent_files:
            for index, file in enumerate(recent_files[:3]):
                action = self._create_recent_file_item(file)
                action.triggered.connect(lambda _, idx=index: self._create_open_session_action(idx))
                menu.addAction(action)

                self.btn_open_menu.setMenu(menu)


    def _create_save_session(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.btn_save_session = QPushButton()
        self.btn_save_session.clicked.connect(lambda: self._create_save_session_action(None))
        self.btn_save_session.setStyleSheet(menu_btn)
        self.btn_save_session.setIcon(QIcon(QPixmap("src/resources/icons/save_button.svg")))
        self.btn_save_session.setIconSize(QSize(75, 40))
        
        self.btn_save_menu = QPushButton("Сохранить\n Сессию")
        self.btn_save_menu.setStyleSheet(menu_btn)
        self.btn_save_menu.setFixedSize(75, 40)
        
        
        layout.addWidget(self.btn_save_session, alignment=Qt.AlignCenter)
        layout.addWidget(self.btn_save_menu)

        layout.addStretch()

        return container
    
    def _create_save_session_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet(menu_item)
        
        action_save = self._create_menu_item_label_svg("Сохранить", "save.svg")
        action_save.triggered.connect(lambda: self._create_save_session_action(None))
        
        action_save_as = self._create_menu_item_label_svg("Сохранить как...", "save_as.svg")
        action_save_as.triggered.connect(lambda: self._create_save_session_action(0))
        
        menu.addAction(action_save)
        menu.addAction(action_save_as)
        
        self.btn_save_menu.setMenu(menu)


    def _create_menu_item_label_svg(self, text, icon_path):
        widget_action = QWidgetAction(self)
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 5, 10, 5)
        
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(f"src/resources/icons/{icon_path}").scaled(20, 20))
        
        label = QLabel(text)
        
        layout.addWidget(icon_label)
        layout.addWidget(label)
        layout.addStretch()
        
        widget_action.setDefaultWidget(widget)
        return widget_action
    
    def _create_menu_item_label(self, text):
        widget_action = QWidgetAction(self)
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 5, 10, 5)
        
        label = QLabel(text)
        label.setObjectName("openSessionMenu")
        label.setStyleSheet(menu_item)
        
        layout.addWidget(label)
        layout.addStretch()
        
        widget_action.setDefaultWidget(widget)
        return widget_action

    def _create_recent_file_item(self, name: str) -> QWidgetAction:
        widget_action = QWidgetAction(self)
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(15, 5, 5, 5)

        icon_label = QLabel()
        icon_label.setPixmap(QPixmap("src/resources/icons/file.svg").scaled(20, 20))

        label = QLabel(name)
        
        layout.addWidget(icon_label)
        layout.addWidget(label)

        widget.mousePressEvent = lambda event: self.open_recent_file(name)

        widget_action.setDefaultWidget(widget)
        return widget_action

    def _create_new_session_action(self, action):
        FileActionHandler.new_session(action)

    def _create_open_session_action(self, action):
        FileActionHandler.open_session(action)

    def _create_save_session_action(self, action):
        FileActionHandler.save_session(action)
