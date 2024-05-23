import aubio

import numpy as np
import matplotlib.pyplot as plt
from typing import List

from pydub import AudioSegment

from models.note import Note

def chunks(arr, chunk_size):
    remainder = len(arr) % chunk_size
    if remainder > 0:
        pad_length = chunk_size - remainder
        arr = np.pad(arr, (0, pad_length), mode='constant')
    
    for i in range(0, len(arr), chunk_size):
        yield arr[i:i + chunk_size]

class Audio:
    def __init__(self, path: str):
        self.path = path
        
        self._notes: List[Note] = []
   
    @property
    def notes(self):
        return self._notes
    
    def detect_notes(self, win_s=1024, hop_s=512) -> None:
        audio = AudioSegment.from_file(self.path)
        audio = audio.set_channels(1)
        samplerate = audio.frame_rate
        
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        samples = samples / 2 ** (audio.sample_width * 8 - 1)
        
        total_frames = 0
        notes_o = aubio.notes("default", win_s, hop_s, samplerate)
        
        self._notes.clear()
        
        for sample in chunks(samples, hop_s):
            new_note = notes_o(sample)
            
            if (new_note[0] != 0):
                start_time = total_frames / samplerate
                
                note = Note(new_note[0], start_time=start_time)
                
                if self._notes:
                    self._notes[-1].duration = note.start_time - self._notes[-1].start_time
                    
                self._notes.append(note)
                
            total_frames += len(sample)
        
        if len(self._notes) > 2:
            self._notes[-1].duration = self._notes[-2].duration
        elif len(self.notes) == 1:
            self._notes[-1].duration = 1
    
    def get_spectogram_plot(self):
        audio = AudioSegment.from_file(self.path)
        audio = audio.set_channels(1)
        samplerate = audio.frame_rate
        
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        samples = samples / 2 ** (audio.sample_width * 8 - 1)
        
        fig, plot_b = plt.subplots()
        plot_b.specgram(samples, NFFT=4096, Fs=samplerate, noverlap=900)
        plot_b.set_xlabel('Time')
        plot_b.set_ylabel('Frequency')
        
        fig.patch.set_alpha(0)
        
        return fig
    
    def get_waveform_plot(self):
        audio = AudioSegment.from_file(self.path)
        audio = audio.set_channels(1)
        samplerate = audio.frame_rate
        
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        samples = samples / 2 ** (audio.sample_width * 8 - 1)
        
        fig, plot_a = plt.subplots()
        plot_a.plot(samples)
        plot_a.set_xlabel('sample rate * time')
        plot_a.set_ylabel('energy')
        
        return fig
