import os
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTabWidget, QAction, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDir, pyqtSlot

from widgets.notes_widget import NotesWidget
from widgets.spectrum_widget import SpectrumWidget

from models.audio import Audio

from helpers.midi_manager import midi_manager

from widgets.recorder_widget import AudioRecorderWidget
from widgets.fingerprint_widget import FingerprintWidget

from settings import TEMP_DIR

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.audio = None
        self.record_path = os.path.join(TEMP_DIR, 'temp.wav')
        
        self.init_ui()
        self.init_menu()
        
        self.setWindowTitle("Note Tuner")
        self.setMinimumSize(600, 400)

    def init_ui(self):
        self.tab_widget = QTabWidget(self)
        
        self.notes_widget = NotesWidget()
        self.spectrum_widget = SpectrumWidget()
        self.fingerprint_widget = FingerprintWidget()
        
        self.tab_widget.addTab(self.notes_widget, 'Notes')
        self.tab_widget.addTab(self.spectrum_widget, 'Spectograms')
        self.tab_widget.addTab(self.fingerprint_widget, 'Fingerprint Comparison')
        
        self.setCentralWidget(self.tab_widget)

    def init_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')

        load_action = QAction('Open file', self)
        load_action.setShortcut('Ctrl+O')
        load_action.triggered.connect(self.on_load_file)
        file_menu.addAction(load_action)
        
        record_action = QAction('Record audio', self)
        record_action.setShortcut('Ctrl+R')
        record_action.triggered.connect(self.on_recorder_requested)
        file_menu.addAction(record_action)

        file_menu.addSeparator()
        
        self.export_actions = []
        
        export_midi_action = QAction('Export MIDI', self)
        export_midi_action.triggered.connect(self.on_export_midi)
        file_menu.addAction(export_midi_action)

        export_sheet_action = QAction('Export Note Sheet', self)
        export_sheet_action.triggered.connect(self.on_export_sheet)
        file_menu.addAction(export_sheet_action)

        export_waveform_action = QAction('Export Waveform', self)
        export_waveform_action.triggered.connect(self.on_export_waveform)
        file_menu.addAction(export_waveform_action)
        
        export_spectrogram_action = QAction('Export Spectrogram', self)
        export_spectrogram_action.triggered.connect(self.on_export_spectogram)
        file_menu.addAction(export_spectrogram_action)

        self.export_actions.append(export_midi_action)
        self.export_actions.append(export_sheet_action)
        self.export_actions.append(export_waveform_action)
        self.export_actions.append(export_spectrogram_action)

        for action in self.export_actions:
            action.setEnabled(False)

        file_menu.addSeparator()

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu('Help')

        about_action = QAction('About', self)
        about_action.triggered.connect(self.on_show_about_dialog)
        help_menu.addAction(about_action)

    def update_title(self):
        self.setWindowTitle(f"Note Tuner - {self.filename}")

    @pyqtSlot()
    def on_show_about_dialog(self):
        about_text = "Note Tuner\nVersion 1.0\n\nA simple note tuning application."
        QMessageBox.about(self, "About Note Tuner", about_text)

    @pyqtSlot()
    def on_recorder_requested(self):
        # print('SHOW')
        self.recorder = AudioRecorderWidget(self.record_path, self)
        self.recorder.finished.connect(self.on_audio_recorded)
        self.recorder.show()

    def on_audio_recorded(self):
        self.audio = Audio(self.record_path)
        
        self.notes_widget.audio = self.audio
        self.spectrum_widget.audio = self.audio
        
        for action in self.export_actions:
            action.setEnabled(True)
            
        self.filepath = self.record_path
        self.filename = os.path.basename(self.record_path)
        
        self.update_title()

    @pyqtSlot()
    def on_load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Select audio file', '', 'Audio Files (*.mp3 *.wav *.ogg)')
        if not path:
            return        
        
        self.audio = Audio(path)
        
        self.notes_widget.audio = self.audio
        self.spectrum_widget.audio = self.audio
        
        for action in self.export_actions:
            action.setEnabled(True)
            
        self.filepath = path
        self.filename = os.path.basename(path)
        
        self.update_title()

    @pyqtSlot()
    def on_export_sheet(self):
        if not self.audio:
            return
        
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix('pdf')
        filename, _ = file_dialog.getSaveFileName(
            self,
            "Save Note Sheet",
            '',
            'PDF Files (*.pdf)'
        )
        if filename:
            print(filename)
            # midi_manager.save_sheet(self.audio, filename)

    @pyqtSlot()
    def on_export_waveform(self):
        if not self.audio:
            return
        
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix('png')
        filename, _ = file_dialog.getSaveFileName(
            self,
            "Save Waveform",
            '',
            'PNG Image (*.png)'
        )
        if filename:
            self.spectrum_widget.save_waveform(filename)

    @pyqtSlot()
    def on_export_spectogram(self):
        if not self.audio:
            return
        
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix('png')
        filename, _ = file_dialog.getSaveFileName(
            self,
            "Save Spectogram",
            '',
            'PNG Image (*.png)'
        )
        if filename:
            self.spectrum_widget.save_spectogram(filename)

    @pyqtSlot()
    def on_export_midi(self):
        if not self.audio:
            return
        
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix('mid')
        filename, _ = file_dialog.getSaveFileName(
            self,
            "Save MIDI File",
            '',
            'MIDI Files (*.mid)'
        )
        if filename:
            midi_manager.save_midi_file(self.audio, filename)

