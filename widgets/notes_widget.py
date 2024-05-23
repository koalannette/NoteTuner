import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QToolBar, QAction, QScrollArea, QSizePolicy, QLabel, QComboBox, QToolButton
from PyQt5.QtCore import QObject, QThread, QSize

from PyQt5.QtGui import QIcon

from widgets.note_table_widget import NoteTableWidget

from helpers.midi_manager import midi_manager

from settings import SOUNDFONTS_DIR, SVG_DIR

class Worker(QObject):
    def __init__(self, audio):
        super().__init__()
        
        self.audio = audio
        
    def play(self):
        midi_manager.play_notes(self.audio)

class NotesWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self._audio = None
        self.win_value = 1024
        self.hop_value = 512
        
        self._thread = QThread()
        
        self.init_ui()
        
    @property
    def audio(self):
        return self._audio
    
    @audio.setter
    def audio(self, value):
        self._audio = value
        self._audio.detect_notes(self.win_value, self.hop_value)
        
        self.note_table.audio = self._audio
    
    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.toolbar = QToolBar(self)
        self.toolbar.setStyleSheet('QToolBar {spacing: 5px }')
        
        self.note_table = NoteTableWidget(self)
        
        self.main_layout.addWidget(self.toolbar)
        self.main_layout.addWidget(self.note_table)
        
        self.play_btn = QToolButton()
        self.play_btn.setIcon(QIcon(os.path.join(SVG_DIR, 'play.svg')))
        self.play_btn.setIconSize(QSize(10, 10))
        self.play_btn.setFixedSize(20, 20)
        self.play_btn.triggered.connect(self.on_play_clicked)
        self.toolbar.addWidget(self.play_btn)

        self.stop_btn = QToolButton()
        self.stop_btn.setIcon(QIcon(os.path.join(SVG_DIR, 'stop.svg')))
        self.stop_btn.setIconSize(QSize(20, 20))
        self.stop_btn.setFixedSize(20, 20)
        self.stop_btn.triggered.connect(self.on_stop_clicked)
        self.toolbar.addWidget(self.stop_btn)
        
        self.toolbar.addWidget(QLabel('Soundfont: '))
        self.soundfont_combo = QComboBox()
        self.soundfont_combo.addItem('Piano')
        self.soundfont_combo.addItem('Violin')
        self.soundfont_combo.addItem('Guitar')
        self.soundfont_combo.setCurrentIndex(0)
        self.soundfont_combo.currentIndexChanged.connect(self.on_soundfont_changed)
        self.toolbar.addWidget(self.soundfont_combo)
        
        self.toolbar.addSeparator()
        
        self.win_combo = QComboBox()
        self.win_combo.addItems([str(2**i) for i in range(7, 13)])  # Range from 256 to 4096 (2**8 to 2**12)
        self.win_combo.setCurrentText(str(self.win_value))
        self.win_combo.currentTextChanged.connect(self.on_win_value_updated)

        self.hop_combo = QComboBox()
        self.hop_combo.addItems([str(2**i) for i in range(7, 13)])  # Range from 256 to 4096 (2**8 to 2**12)
        self.hop_combo.setCurrentText(str(self.hop_value))
        self.hop_combo.currentTextChanged.connect(self.on_hop_value_updated)
        
        self.toolbar.addWidget(QLabel('Win: '))
        self.toolbar.addWidget(self.win_combo)
        
        self.toolbar.addWidget(QLabel('Hop: '))
        self.toolbar.addWidget(self.hop_combo)
        
        self.main_layout.addStretch()
        
        self.setLayout(self.main_layout)

    def on_play_clicked(self):
        if not self._audio:
            return

        midi_manager.play_notes(self._audio)

    def on_stop_clicked(self):
        midi_manager.stop_playing()
        
    def on_win_value_updated(self, value):
        self.win_value = int(value) 
        
        if not self._audio:
            return
        
        self._audio.detect_notes(self.win_value, self.hop_value)
        self.note_table.draw_notes()
    
    def on_hop_value_updated(self, value):
        self.hop_value = int(value)
        
        if not self._audio:
            return
        
        self._audio.detect_notes(self.win_value, self.hop_value)
        self.note_table.draw_notes()
    
    def on_soundfont_changed(self, index):
        if index == 0:
            midi_manager.sound_font = os.path.join(SOUNDFONTS_DIR, 'piano.sf2')
        elif index == 1:
            midi_manager.sound_font = os.path.join(SOUNDFONTS_DIR, 'violin.sf2')
        elif index == 2:
            midi_manager.sound_font = os.path.join(SOUNDFONTS_DIR, 'guitar.sf2')