import os

from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QAudioRecorder, QAudioDeviceInfo
from PyQt5.QtCore import QUrl, QTimer, Qt, pyqtSignal

from settings import SVG_DIR

class AudioRecorderWidget(QDialog):
    finished = pyqtSignal()
    
    def __init__(self, path, parent=None):
        super().__init__(parent)
        
        self.path = path
        
        self.recorder = QAudioRecorder()
        self.recorder.setOutputLocation(QUrl.fromLocalFile(os.path.join(os.getcwd(), self.path)))
        self.recording = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer_interval = 1000
        self.seconds_elapsed = 0

        layout = QVBoxLayout()
        
        self.timer_label = QLabel("00:00")
        self.timer_label.setStyleSheet('font-size: 36px')
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_label)
        
        self.start_button = QPushButton()
        self.start_button.setIcon(QIcon(os.path.join(SVG_DIR, 'record.svg')))
        self.start_button.clicked.connect(self.toggle_recording)
        layout.addWidget(self.start_button)
        
        self.setLayout(layout)

        self.setMinimumSize(200, 150)

    def toggle_recording(self):
        if not self.recording:
            self.recorder.record()
            self.timer.start(self.timer_interval)
            self.start_button.setIcon(QIcon(os.path.join(SVG_DIR, 'stop.svg')))
        else:
            self.recorder.stop()
            self.timer.stop()
            self.seconds_elapsed = 0
            self.timer_label.setText("00:00")
            self.start_button.setIcon(QIcon(os.path.join(SVG_DIR, 'record.svg')))
            self.finished.emit()
            self.close()
            
        self.recording = not self.recording

    def update_timer(self):
        self.seconds_elapsed += 1
        minutes = self.seconds_elapsed // 60
        seconds = self.seconds_elapsed % 60
        self.timer_label.setText(f"{minutes:02}:{seconds:02}")

if __name__ == "__main__":
    app = QApplication([])
    widget = AudioRecorderWidget('audio.wav')
    widget.show()
    app.exec_()
