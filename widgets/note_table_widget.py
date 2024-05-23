from typing import List
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt

from widgets.note_widget import NoteWidget

from models.audio import Audio

NOTES_COUNT = 12
NOTE_HEIGHT = 40

SECOND_WIDTH = 150

class NoteTableWidget(QScrollArea):
    audio_updated = pyqtSignal(Audio)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._audio = None
        self.note_widgets = []
        
        self.setFixedHeight(NOTE_HEIGHT * NOTES_COUNT + 20)
        
        self.init_ui()
        
    def init_ui(self):
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Ensure vertical scrollbar is always shown
        
        # Create a widget to contain the notes
        self.content_widget = QWidget()
        self.setWidget(self.content_widget)
        
        self.main_layout = QVBoxLayout(self.content_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.lines = []
        for i in range(NOTES_COUNT):
            line = QWidget()
            line.setObjectName('line')
            line.setFixedHeight(NOTE_HEIGHT)
            line.setStyleSheet('#line { background: #f5f5f5; border-top: 1px solid rgba(0, 0, 0, 0.5); }')
            
            self.lines.append(line)
            self.main_layout.addWidget(line)
    
    def draw_notes(self):
        if not self._audio:
            return
        
        for wid in self.note_widgets:
            wid.deleteLater()
        self.note_widgets.clear()
    
        for note in self._audio.notes:
            x = int(note.start_time * SECOND_WIDTH)
            w = int(note.duration   * SECOND_WIDTH)

            row = NOTES_COUNT - note.note - 1
            
            wid = NoteWidget(note)
            
            wid.setParent(self.lines[row])
            wid.setFixedWidth(w)
            wid.move(x, 1)
            wid.show()
            
            self.note_widgets.append(wid)
        
        if self.note_widgets:
            line_w = int(SECOND_WIDTH * (self._audio.notes[-1].start_time + self._audio.notes[-1].duration))
            for line in self.lines:
                line.setMinimumWidth(line_w)
            
    @property
    def audio(self):
        return self._audio
    
    @audio.setter
    def audio(self, val: Audio):
        self._audio = val
        self.draw_notes()