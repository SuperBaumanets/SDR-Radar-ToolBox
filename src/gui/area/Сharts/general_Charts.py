from PySide6.QtWidgets import QWidget, QHBoxLayout
from src.gui.area.Сharts.left_area import LeftCharts
from src.gui.area.Сharts.right_area import RightCharts

class GeneralCharts(QWidget):
    def __init__(self, charts_handler):
        super().__init__()
        self.charts_handler = charts_handler
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Левая часть с постоянным графиком
        self.left_charts = LeftCharts()
        self.left_charts.setFixedSize(650, 700)
        layout.addWidget(self.left_charts, stretch=1)

        # Правая часть с динамическими графиками
        self.right_charts = RightCharts()
        self.right_charts.setFixedSize(650, 700)
        layout.addWidget(self.right_charts, stretch=2)

    def _connect_signals(self):
        """Соединение сигналов от Charts с обработчиками"""
        self.charts_handler.buttonClicked.connect(
            lambda bid, state: self.right_charts.update_tab(bid, state)
        )