from PyQt5.QtWidgets import QTabWidget

from widgets.plot_widget import PlotWidget

class ComparisonPlotsWidget(QTabWidget):
    def __init__(self, plots: dict):
        super().__init__()
        
        self.addTab(PlotWidget(plots['spectrum']), 'Spectrum')
        self.addTab(PlotWidget(plots['sftf']), 'sftf')
        self.addTab(PlotWidget(plots['mel_freq']), 'Mel Frequency')
        self.addTab(PlotWidget(plots['mel_norm']), 'Mel Normalized')
        self.addTab(PlotWidget(plots['betty']), 'Betty')
    
    