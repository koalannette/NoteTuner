from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton, QFormLayout, QVBoxLayout, QLabel, QHBoxLayout, QMessageBox, QLineEdit

from widgets.plot_widget import PlotWidget
from widgets.comparison_plots_widget import ComparisonPlotsWidget

from helpers.fingerprint_manager import FingerprintManager

def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

def open_audio_file():
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    file_filter = "Audio Files (*.mp3 *.wav *.flac *.aac *.ogg);;All Files (*)"
    file_path, _ = QFileDialog.getOpenFileName(None, "Open Audio File", "", file_filter, options=options)
    if file_path:
        return file_path
    return None

class FingerprintWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.path1 = ''
        self.path2 = ''

        self.manager = FingerprintManager()

        self.main_layout = QVBoxLayout(self)
        
        self.form_layout = QFormLayout()
        
        self.compare_btn = QPushButton('Compare fingerprints')
        self.compare_btn.clicked.connect(self.on_compare)
        
        self.error_matching_edit = QLineEdit()
        self.error_matching_edit.setText('0.0')
        self.error_matching_edit.setReadOnly(True)
        
        self.left_file_button  = QPushButton('Open file')
        self.right_file_button = QPushButton('Open file')
        self.left_file_button.clicked.connect(self.on_load_path1)
        self.right_file_button.clicked.connect(self.on_load_path2)
        
        self.left_path_label = QLabel()
        self.right_path_label = QLabel()
        
        self.form_layout.addRow(self.left_file_button,  self.left_path_label)
        self.form_layout.addRow(self.right_file_button, self.right_path_label)
        
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.compare_btn)
    
        self.plots_layout = QHBoxLayout()
        self.result_layout = QHBoxLayout()
        
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.plots_layout,  1)
        self.main_layout.addLayout(self.result_layout, 1)
        
        self.similarity_edit = QLineEdit('0.0')
        self.similarity_edit.setReadOnly(True)
        
        error_layout = QFormLayout()
        error_layout.addRow(QLabel('Error matching: '), self.error_matching_edit)
        error_layout.addRow(QLabel('Similarity percent:'), self.similarity_edit)
        self.main_layout.addLayout(error_layout)
    
    def on_compare(self):
        if not self.path1 or not self.path2:
            self.show_error_message("Error", "Both file paths must be set before comparison.")
            return
        
        self.manager.process(self.path1, self.path2)
        
        self.load_plots()
        self.error_matching_edit.setText(str(self.manager.error_matching))
        self.similarity_edit.setText(str((1 - self.manager.error_matching) * 100))
    
    def show_error_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
    
    def on_load_path1(self):
        self.path1 = open_audio_file()
        self.left_path_label.setText(self.path1)
        
    def on_load_path2(self):
        self.path2 = open_audio_file()
        self.right_path_label.setText(self.path2)
    
    def load_plots(self):
        clearLayout(self.plots_layout)
        clearLayout(self.result_layout)
        
        self.plots_layout.addWidget(
            ComparisonPlotsWidget(self.manager.plots1)
        )
        self.plots_layout.addWidget(
            ComparisonPlotsWidget(self.manager.plots2)
        )
        
        self.result_layout.addStretch()
        self.result_layout.addWidget(
            PlotWidget(self.manager.cost_mat_plt)
        )
        self.result_layout.addWidget(
            PlotWidget(self.manager.match_plt)
        )
        self.result_layout.addStretch()