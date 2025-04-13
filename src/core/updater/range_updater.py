from PySide6.QtCore import QObject
from src.core.settings.target import target
from src.gui.area.ApplicationManagement.metric_ApplicationManagement import Metric

class Range_Updater(QObject):
    def __init__(self, metric_widget:Metric):
        super().__init__()
        self.metric = metric_widget

    def update_range_target(self):
        range = target.range
        self._update_edit(self.metric.data_range, f"{range}")
        self._update_combo(self.metric.measurement_range, "м")

    def _update_edit(self, field, value):
        field.blockSignals(True)
        field.setText(value)
        field.blockSignals(False) 

    def _update_combo(self, field, value):
        field.blockSignals(True)
        field.setCurrentText(value)
        field.blockSignals(False)