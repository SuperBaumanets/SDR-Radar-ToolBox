from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from src.gui.area.SettingsManagement.Radar.headline_SettingsManagement import Headline
from src.gui.area.SettingsManagement.Radar.main_SettingsManagement import Main
from src.gui.area.SettingsManagement.Radar.antenna_SettingsManagement import Antenna
from src.gui.area.SettingsManagement.SDR.control_SDRManagement import Control
from src.gui.area.SettingsManagement.SDR.parameters_SDRManagement import Parameters

from src.gui.area.SettingsManagement.Environment.atmosphere_SettingsManagement import Environment

from src.core.processing.SettingsManagement.main_action import MainActionHandler
from src.core.processing.SettingsManagement.headline_action import HeadlineActionHandler
from src.core.processing.ApplicationManagement.file_action import FileActionHandler
from src.core.processing.ApplicationManagement.radar_action import LocatorActionHandler
from src.core.processing.SDR.sdr_control_action import SDRControlHandler

from src.gui.styles.settings_management import tab_style

class SettingsPanel(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.main_handler = MainActionHandler()
        self.headline_handler = HeadlineActionHandler()
        self.sdr_control_handler = SDRControlHandler()
          
        self.main_widget = Main(self.main_handler)
        self.headline_widget = Headline(self.headline_handler)
        self.sdr_control_widget = Control(self.sdr_control_handler)
        self.sdr_parameters_widget = Parameters()

        self.file_handler = FileActionHandler()

        self.radar_handler = LocatorActionHandler()

        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._create_tabs())
        

    def _create_tabs(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(tab_style)

        # Вкладка Radar 
        radar_tab = QWidget()
        radar_tab.setFixedSize(600, 900)
        radar_layout = QVBoxLayout(radar_tab)
        radar_layout.setContentsMargins(5, 5, 5, 5)
        radar_layout.setSpacing(5)

        self.headline_widget.layout().setContentsMargins(0, 0, 0, 0)
        radar_layout.addWidget(self.headline_widget)

        self.main_widget.setContentsMargins(0, 0, 0, 0)
        radar_layout.addWidget(self.main_widget)
    
        antenna = Antenna()
        antenna.setContentsMargins(0, 0, 0, 0)
        radar_layout.addWidget(antenna)

        radar_layout.addStretch()
        
        # Вкладка Environment 
        environment_tab = QWidget()
        environment_tab.setFixedSize(600, 900)
        environment_layout = QVBoxLayout(environment_tab)
        environment_layout.setContentsMargins(5, 5, 5, 5)
        environment_layout.setSpacing(5)

        environment = Environment()
        environment.setContentsMargins(0, 0, 0, 0)
        environment_layout.addWidget(environment)

        environment_layout.addStretch()
        
        # Вкладка SDR
        sdr_tab = QWidget()
        sdr_tab.setFixedSize(600, 900)
        sdr_layout = QVBoxLayout(sdr_tab)
        sdr_layout.setContentsMargins(5, 5, 5, 5)
        sdr_layout.setSpacing(5)

        self.sdr_control_widget.setContentsMargins(0, 0, 0, 0)
        sdr_layout.addWidget(self.sdr_control_widget)
        
        self.sdr_parameters_widget.setContentsMargins(0, 0, 0, 0)
        sdr_layout.addWidget(self.sdr_parameters_widget)

        sdr_layout.addStretch()

        # Добавляем вкладки и сохраняем индекс
        self.tab_widget.addTab(radar_tab, "Параметры Радара")
        self.tab_widget.addTab(environment_tab, "Среда")
        self.sdr_tab_index = self.tab_widget.addTab(sdr_tab, "SDR устройства")

        # Скрываем вкладку по умолчанию
        self.tab_widget.setTabVisible(self.sdr_tab_index, False)
        
        return self.tab_widget
    
    def toggle_sdr_tab(self):
        if self.sdr_tab_index != -1:
            current_state = self.tab_widget.isTabVisible(self.sdr_tab_index)
            new_state = not current_state
            self.tab_widget.setTabVisible(self.sdr_tab_index, new_state)