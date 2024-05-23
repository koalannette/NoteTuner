from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QColor, QMouseEvent

from models.note import Note

from helpers.midi_manager import midi_manager

NOTE_HEIGHT = 40

class NoteWidget(QWidget):
    def __init__(self, note: Note, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.note = note
        
        self.init_ui()
        self.setFixedHeight(NOTE_HEIGHT - 2)
        
        self.setCursor(Qt.PointingHandCursor)
        
    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.note_label = QLabel()
        self.note_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.note_label.setText(self.note.note_str)
        
        note_index = self.note.note
        
        color = QColor(int(((note_index + 1) / 12.0) * 255), 
                       60, 
                       int(255 - ((note_index + 1) / 12.0) * 255))
        self.setStyleSheet("background-color: %s; border: 0px solid black; color: white; border-radius: 10px;" % color.name())
                
        self.main_layout.addWidget(self.note_label)
        self.setLayout(self.main_layout)
    
    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        midi_manager.play_note(self.note)
        return super().mousePressEvent(a0)
        