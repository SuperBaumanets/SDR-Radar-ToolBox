from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
import pyqtgraph as pg
from pyqtgraph import PlotWidget
from collections import OrderedDict

from src.gui.styles.settings_management import tab_style

class BasePlotWidget(PlotWidget):
    def __init__(self, title, xlabel, ylabel):
        super().__init__()
        self.setBackground('w')
        self.setTitle(title, color='k')
        self.setLabel('left', ylabel)
        self.setLabel('bottom', xlabel)
        self.addLegend()
        self.showGrid(x=True, y=True)
        self.curves = OrderedDict()
        self.default_pen = pg.mkPen('b', width=2)

    def add_curve(self, curve_id, **kwargs):
        """Добавление новой кривой с уникальным идентификатором"""
        pen = kwargs.get('pen', self.default_pen)
        symbol = kwargs.get('symbol', None)
        symbol_size = kwargs.get('symbol_size', 7)
        name = kwargs.get('name', curve_id)
        
        self.curves[curve_id] = self.plot(
            [], [],
            pen=pen,
            symbol=symbol,
            symbolSize=symbol_size,
            name=name
        )

    def update_curve(self, curve_id, x, y):
        """Обновление данных конкретной кривой"""
        if curve_id not in self.curves:
            raise KeyError(f"Curve {curve_id} not found")
        self.curves[curve_id].setData(x, y)
        self.autoRange()

    def remove_curve(self, curve_id):
        """Удаление кривой"""
        if curve_id in self.curves:
            self.removeItem(self.curves[curve_id])
            del self.curves[curve_id]

class RadarSignalPlot(BasePlotWidget):
    def __init__(self):
        super().__init__("Radar Signal", "Time (s)", "Amplitude")
        self.default_pen = pg.mkPen('b', width=1.5)

    def add_signal_curve(self, curve_id):
        self.add_curve(curve_id, 
                      pen=pg.mkPen('b', width=1.5),
                      name=f"Signal {curve_id}")

class SpectrumPlot(BasePlotWidget):
    def __init__(self):
        super().__init__("Signal Spectrum", "Frequency (Hz)", "Power")
        self.default_pen = pg.mkPen('r', width=2)

    def add_spectrum_curve(self, curve_id):
        self.add_curve(curve_id,
                      pen=pg.mkPen('r', width=2, style=pg.QtCore.Qt.DashLine),
                      symbol='o',
                      symbol_size=5)

class SNRRangePlot(BasePlotWidget):
    def __init__(self):
        super().__init__("SNR vs Range", "Range (km)", "SNR (dB)")
        self.default_pen = pg.mkPen('g', width=2)

    def add_snr_curve(self, curve_id):
        self.add_curve(curve_id,
                      pen=pg.mkPen('g', width=2),
                      symbol='s',
                      symbol_size=8)

class RightCharts(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self.tabs = {}

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(tab_style)
        layout.addWidget(self.tab_widget)

    def update_tab(self, button_id, state):
        if state:
            self._add_tab(button_id)
        else:
            self._remove_tab(button_id)

    def _add_tab(self, tab_id):
        if tab_id in self.tabs:
            return

        if tab_id == "radar_signal":
            plot_widget = RadarSignalPlot()
            title = "Radar Signal"
        elif tab_id == "radar_signal_spectrum":
            plot_widget = SpectrumPlot()
            title = "Signal Spectrum"
        elif tab_id == "snr_range":
            plot_widget = SNRRangePlot()
            title = "SNR vs Range"
        else:
            return

        self.tabs[tab_id] = plot_widget
        self.tab_widget.addTab(plot_widget, title)
        self.tab_widget.setCurrentWidget(plot_widget)

    def _remove_tab(self, tab_id):
        if tab_id in self.tabs:
            index = self.tab_widget.indexOf(self.tabs[tab_id])
            self.tab_widget.removeTab(index)
            del self.tabs[tab_id]

    def get_plot_widget(self, tab_id):
        return self.tabs.get(tab_id)