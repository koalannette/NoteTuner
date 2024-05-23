from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QToolBar, QStackedWidget, QPushButton, QAction, QLabel, QComboBox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from widgets.plot_widget import PlotWidget

from models.audio import Audio

class SpectrumWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self._audio: Audio | None = None
        
        self.init_ui()
    
    @property
    def audio(self):
        return self._audio
    
    @audio.setter
    def audio(self, value):
        self._audio = value
        
        self.create_plot()
    
    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        
        self.toolbar = QToolBar(self)
        self.toolbar.setStyleSheet("QToolBar { spacing: 5px; }")
        
        self.toolbar.addWidget(QLabel('Type:'))
        
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItem('Spectogram')
        self.plot_type_combo.addItem('Waveform')
        self.plot_type_combo.currentIndexChanged.connect(self.change_plot)
        self.toolbar.addWidget(self.plot_type_combo)
        
        self.main_layout.addWidget(self.toolbar)
        
        self.plot_stack = QStackedWidget()
        self.main_layout.addWidget(self.plot_stack)
        
        self.setLayout(self.main_layout)
        
    def create_plot(self):
        if not self._audio:
            return
        
        while self.plot_stack.count() > 0:
            widget = self.plot_stack.widget(0)
            self.plot_stack.removeWidget(widget)
            widget.deleteLater()
        
        fig1 = self._audio.get_spectogram_plot()
        fig2 = self._audio.get_waveform_plot()

        self.spectogram_widget = PlotWidget(fig1)
        self.waveform_widget = PlotWidget(fig2)

        self.plot_stack.addWidget(self.spectogram_widget)
        self.plot_stack.addWidget(self.waveform_widget)
        
        self.plot_type_combo.setCurrentIndex(0)
        self.plot_stack.setCurrentIndex(0)
    
    def change_plot(self, index: int):
        self.plot_stack.setCurrentIndex(index)
        
    def save_spectogram(self, path):
        self.spectogram_widget.figure.savefig(path)
    
    def save_waveform(self, path):
        self.waveform_widget.figure.savefig(path)