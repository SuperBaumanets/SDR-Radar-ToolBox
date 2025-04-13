from PySide6.QtWidgets import QWidget, QHBoxLayout

from src.gui.area.ApplicationManagement.file_ApplicationManagement import File
from src.gui.area.ApplicationManagement.radars_ApplicationManagement import Radars
from src.gui.area.ApplicationManagement.metric_ApplicationManagement import Metric
from src.gui.area.ApplicationManagement.charts_ApplicationManagement import Charts
from src.gui.area.ApplicationManagement.device_ApplicationManagement import Device
from src.gui.area.ApplicationManagement.export_ApplicationManagement import Export

from src.core.processing.ApplicationManagement.metric_action import MetricActionHandler

from src.core.updater.generic_updater import generic_updater

class TopPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.charts_widget = Charts()
        self.device_widget = Device()
        self.radar_widget = Radars()

        self.metric_handler = MetricActionHandler()  
        self.metric_widget = Metric(None, self.metric_handler)

        self._setup_ui()
        
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._add_widgets())
        layout.addStretch()

    def _add_widgets(self):
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        container_layout.addWidget(File())
        container_layout.addWidget(self.radar_widget )
        container_layout.addWidget(self.metric_widget)
        container_layout.addWidget(self.charts_widget)
        container_layout.addWidget(self.device_widget)
        container_layout.addWidget(Export())
        container_layout.addSpacing(0)
        container_layout.addStretch()

        return container