import os
import time
import threading

from mingus.midi import fluidsynth, midi_file_out
from mingus.containers import Note, Track, Bar
import mingus.extra.lilypond as LilyPond

from models.note import Note
from models.audio import Audio

from settings import SOUNDFONTS_DIR

class MidiManager:
    def __init__(self):
        self.sound_font = os.path.join(SOUNDFONTS_DIR, 'piano.sf2')
    
        fluidsynth.init(self.sound_font)
    
        self.is_playing = False
        self._thread = None
        self._stop_event = threading.Event()
    
    @property
    def sound_font(self):
        return self._sound_font

    @sound_font.setter
    def sound_font(self, val: str):
        self._sound_font = val
        
        r = fluidsynth.midi.load_sound_font(self._sound_font)
        fluidsynth.midi.fs.program_reset()
        # print(r)
    
    def save_midi_file(self, audio, path: str) -> bool:
        t = Track()
        for note in audio.notes:
            t + note.to_mingus_note()
            
        midi_file_out.write_Track(path, t)
    
    def play_note(self, note: Note):
        fluidsynth.play_Note(note.to_mingus_note(), channel=1)
    
    def play_notes(self, audio: Audio):
        if self.is_playing:
            return

        self.is_playing = True
        self._stop_event.clear()

        def play_audio():
            for note in audio.notes:
                if self._stop_event.is_set():
                    break
                self.play_note(note)
                time.sleep(note.duration)
                fluidsynth.stop_everything()

            self.is_playing = False

        self._thread = threading.Thread(target=play_audio)
        self._thread.start()

    def stop_playing(self):
        if self.is_playing:
            self._stop_event.set()
            self._thread.join()
            self.is_playing = False
    
    def save_sheet(self, audio: Audio, path: str) -> bool:
        t = Track()
        for note in audio.notes:
            t + note.to_mingus_note()
        
        pond = LilyPond.from_Track(t)
        LilyPond.to_pdf(pond, path)

midi_manager = MidiManager()