from PySide6.QtCore import QObject
from src.core.updater.headline_updater import Headline_Updater
from src.core.updater.settings_update import Settings_Updater
from src.core.updater.range_updater import Range_Updater
from src.core.updater.table_updater import Table_Updater
from src.core.updater.charts_updater import Charts_Updater
from src.core.updater.sdr_control_updater import SDR_Control_Updater

class Generic_Updater(QObject):
    def __init__(self):
        super().__init__()
        self.updater_headline = None
        self.updater_settings = None
        self.updater_range = None
        self.updater_table = None
        self.updater_charts = None
        self.updater_sdr_control = None
        
    def init_handlers(self, updater_headline: Headline_Updater, 
                            updater_settings: Settings_Updater,
                            updater_range:Range_Updater,
                            updater_table: Table_Updater,
                            updater_charts: Charts_Updater,
                            updater_sdr_control: SDR_Control_Updater):
        self.updater_headline = updater_headline
        self.updater_settings = updater_settings
        self.updater_range = updater_range
        self.updater_table = updater_table
        self.updater_charts = updater_charts
        self.updater_sdr_control = updater_sdr_control

generic_updater = Generic_Updater()