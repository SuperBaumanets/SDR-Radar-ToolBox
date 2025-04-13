from PySide6.QtCore import QObject
from src.core.settings.target import target
from src.gui.area.SettingsManagement.SDR.control_SDRManagement import Control
from src.gui.area.SettingsManagement.SDR.parameters_SDRManagement import Parameters

class SDR_Control_Updater(QObject):
    def __init__(self, sdr_control_widget:Control, sdr_parameters_widget:Parameters):
        super().__init__()
        self.sdr_control = sdr_control_widget
        self.sdr_parameters = sdr_parameters_widget

    def update_connect(self, connect: bool):
        if connect == True:
            self.sdr_control.connection_indicator.setStyleSheet(
            f"background-color: green;"
            "border-radius: 10px;"
            "border: 2px solid darkgray;"
        )
        else:
            self.sdr_control.connection_indicator.setStyleSheet(
            f"background-color: red;"
            "border-radius: 10px;"
            "border: 2px solid darkgray;"
        )