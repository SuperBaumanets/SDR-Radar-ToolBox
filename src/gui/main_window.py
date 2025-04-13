from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout

from src.gui.styles.main_panel import main

from src.gui.area.ApplicationManagement.general_ApplicationManagement import TopPanel
from src.gui.area.SettingsManagement.general_SettingsManagement import SettingsPanel
from src.gui.area.Сharts.general_Charts import GeneralCharts
from src.gui.area.Characteristics.general_Table import TableCharacteristics

from src.core.processing.Characteristics.table_action import TableActionHandler

from src.core.updater.generic_updater import generic_updater
from src.core.updater.headline_updater import Headline_Updater
from src.core.updater.settings_update import Settings_Updater
from src.core.updater.range_updater import Range_Updater
from src.core.updater.table_updater import Table_Updater
from src.core.updater.charts_updater import Charts_Updater
from src.core.updater.sdr_control_updater import SDR_Control_Updater

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Radar Simulator")
        self.setStyleSheet(main)
        
        # Установка полноэкранного режима
        self.showMaximized()
        
        # Главный контейнер
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Верхняя панель настроек
        self.top_panel = TopPanel()
        main_layout.addWidget(self.top_panel)

        # Основная рабочая область
        workspace = QWidget()
        workspace_layout = QHBoxLayout(workspace)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setSpacing(0)

        workspace_characteristics = QWidget()
        workspace_characteristics_layout = QVBoxLayout(workspace_characteristics)

        # Нижняя часть с таблицей
        self.table_handler = TableActionHandler()  
        self.table_widget = TableCharacteristics(self.table_handler)  
    
        # Левая панель настроек
        self.settings_panel = SettingsPanel(self) 
        self.settings_panel.setFixedWidth(600)
        workspace_layout.addWidget(self.settings_panel)

        self.chart_widget = GeneralCharts(self.top_panel.charts_widget)
        workspace_characteristics_layout.addWidget(self.chart_widget)

        workspace_characteristics_layout.addWidget(self.table_widget)

        workspace_layout.addWidget(workspace_characteristics)
    
        main_layout.addWidget(workspace, stretch=1)
        self.setCentralWidget(main_widget)

        self.headline_updater = Headline_Updater(self.settings_panel.headline_widget)
        self.settigs_updater = Settings_Updater(self.settings_panel.main_widget)
        self.metric_updater = Range_Updater(self.top_panel.metric_widget)
        self.table_updater = Table_Updater(self.table_widget)
        self.charts_updater = Charts_Updater(self.chart_widget)
        self.sdr_control_updater = SDR_Control_Updater(self.settings_panel.sdr_control_widget, self.settings_panel.sdr_parameters_widget)

        generic_updater.init_handlers(self.headline_updater, self.settigs_updater, self.metric_updater, self.table_updater, self.charts_updater, self.sdr_control_updater)

        self.settings_panel.main_handler.set_main_widget(generic_updater)
        self.settings_panel.headline_handler.set_main_widget(generic_updater)
        self.settings_panel.file_handler.set_main_action(generic_updater)
        self.settings_panel.radar_handler.set_main_action(generic_updater)
        self.top_panel.metric_handler.set_main_widget(generic_updater)
        self.table_handler.set_main_widget(generic_updater)
        self.settings_panel.sdr_control_handler.set_main_widget(generic_updater)
    
        # Настраиваем соединения
        self._connect_signals()

    def _connect_signals(self):
        # Связь кнопки SDR с вкладкой
        self.top_panel.device_widget.toggle_sdr_tab.connect(
            self.settings_panel.toggle_sdr_tab
        )
        
        # Связь кнопок графиков с обновлением charts_panel
        self.top_panel.charts_widget.buttonClicked.connect(
            self.chart_widget.right_charts.update_tab
        )

    def get_table_characteristics(self):
        return self.table_characteristics
    
    