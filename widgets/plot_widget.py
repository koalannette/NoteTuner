from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

class PlotWidget(QWidget):
    def __init__(self, figure, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        
        self.figure = figure
        self.init_ui()
        
        self.setMinimumSize(300, 200)
    
    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        self.main_layout.addWidget(self.canvas)
        self.main_layout.addWidget(self.toolbar)
        
        self.setLayout(self.main_layout)