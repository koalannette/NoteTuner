from aubio import midi2note
from mingus.containers import Note as MingusNote

class Note:
    def __init__(self, midi_note, duration = 0, start_time = 0):
        self.midi_note = midi_note
        
        self.octave = int(midi_note // 12 - 1)
        self.note = int(midi_note % 12)
        self.note_str = midi2note(int(midi_note))
        
        self.duration = duration
        self.start_time = start_time
    
    def to_mingus_note(self):
        name = self.note_str[:-1]
        octave = int(self.note_str[-1:])
        
        return MingusNote(name, octave, velocity=127)