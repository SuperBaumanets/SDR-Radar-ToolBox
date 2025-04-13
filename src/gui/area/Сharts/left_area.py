from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
import pyqtgraph as pg
from pyqtgraph import PlotWidget
from collections import defaultdict

from src.gui.styles.settings_management import tab_style

class MultiCurvePlot(PlotWidget):
    def __init__(self):
        super().__init__()
        self.setBackground('w')
        self.showGrid(x=True, y=True)
        self.curves = defaultdict(dict)
        
        # Настройки по умолчанию
        self.default_pen = pg.mkPen(color='b', width=2)
        self.default_symbol = 'o'
        self.default_symbol_size = 7

    def add_curve(self, id_curve, **kwargs):
        pen = kwargs.get('pen', self.default_pen)
        symbol = kwargs.get('symbol', self.default_symbol)
        symbol_size = kwargs.get('symbol_size', self.default_symbol_size)
        
        self.curves[id_curve] = {
            'plot': self.plot([], [], 
                            pen=pen, 
                            symbol=symbol,
                            symbolSize=symbol_size,
                            name=str(id_curve)),
            'x_data': [],
            'y_data': []
        }

    def update_curve(self, id_curve, x, y):
        """Обновление данных кривой"""
        if id_curve not in self.curves:
            raise ValueError(f"Curve {id_curve} not found")
        
        self.curves[id_curve]['x_data'] = x
        self.curves[id_curve]['y_data'] = y
        self.curves[id_curve]['plot'].setData(x, y)
        self.autoRange()

    def remove_curve(self, id_curve):
        """Удаление кривой"""
        if id_curve in self.curves:
            self.removeItem(self.curves[id_curve]['plot'])
            del self.curves[id_curve]

class LeftCharts(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(tab_style)
        
        # Основной график
        self.plot = MultiCurvePlot()
        self.plot.setLogMode(x=False, y=False) 
        self.plot.setTitle("SNR vs Range", color='k')
        self.plot.setLabel('left', 'SNR (dB)')
        self.plot.setLabel('bottom', 'Range (km)')
    
        self.tab_widget.addTab(self.plot, "Main Plot")
        layout.addWidget(self.tab_widget)