import re 
import numpy as np
from itertools import product
import matplotlib.pyplot as plt

from audioId.core import audio, spectrogram
from audioId.pipeline import window_to_ph_vector
from audioId.pipeline import fingerprint_audio, compare_audios, get_matrix_from_dict, get_windows_from_audio
from audioId.pipeline.match import get_delta_t_matching, get_error_from_matching

from audioId.ph import filtrations, ph
from audioId.ph.vectorization import BettiCurveExact
from audioId.transformations.transformation import MyTransformer, NoiseTransformer

from scipy.ndimage import median_filter
from scipy.stats import pearsonr

class FingerprintManager:
    def __init__(self):
        self.plots1 = {}
        self.plots2 = {}
    
    def process(self, file1: str, file2: str):
        self.track1 = audio.Audio.from_file(file1)
        self.track2 = audio.Audio.from_file(file2)
        
        try:
            self.clip1 = self.track1.extract(0, 30)
        except AssertionError:
            self.clip1 = self.track1
        
        try:
            self.clip2 = self.track2.extract(0, 30)
        except AssertionError:
            self.clip2 = self.track2
        
        self.windows1 = get_windows_from_audio(self.clip1, spectrogram.MelSpectrogram)
        self.windows2 = get_windows_from_audio(self.clip2, spectrogram.MelSpectrogram)

        fingerprint_params = dict(
            spectrogramFct=spectrogram.MelSpectrogram,
            filter_fct=filtrations.intensity,
            compute_ph=ph.compute_ph_super_level,
            vect={0: BettiCurveExact(True), 1: BettiCurveExact(True)}
        )
        
        self.plots1 = self._process_file(self.clip1, self.windows1)
        self.plots2 = self._process_file(self.clip2, self.windows2)

        comparison_12 = compare_audios(self.clip1, self.clip2, **fingerprint_params)
        
        distances, keys_1, keys_2 = get_matrix_from_dict(comparison_12, self.windows1, self.windows2)
        d = {'distances': distances, 'keys_1': keys_1, 'keys_2': keys_2}
        lambda_value = 0.3; weights = np.array([lambda_value, 1.-lambda_value])
        
        dist = np.array(d["distances"])
        cost = np.dot(dist, weights)

        self.cost_mat_plt, ax1 = plt.subplots(figsize=(5, 4))
        cax1 = ax1.imshow(cost)
        ax1.set_title('The cost matrix $C$', fontsize=11)
        ax1.set_xlabel('Window index in $s$', fontsize=10)
        ax1.set_ylabel('Window index in $s\'$', fontsize=10)
        cbar1 = self.cost_mat_plt.colorbar(cax1, ax=ax1)
        ax1.tick_params(axis='x', labelsize=8)
        ax1.tick_params(axis='y', labelsize=8)
        self.cost_mat_plt.tight_layout()
        
        # Create figure and subplot for the matching delta t plot
        matching_delta_t = get_delta_t_matching(d)
        
        self.match_plt, ax2 = plt.subplots(figsize=(5, 5))
        ax2.scatter(matching_delta_t[0], matching_delta_t[1], s=60, marker='o', edgecolors='b', facecolors='none')
        ax2.set_xlabel("t1", fontsize=10)
        ax2.set_ylabel("t2", fontsize=10)
        ax2.tick_params(axis='x', labelsize=8)
        ax2.tick_params(axis='y', labelsize=8)
        self.match_plt.tight_layout()

        x, y = matching_delta_t[0], matching_delta_t[1]
        smoothed = median_filter(y, mode="nearest", size=(5,))
        self.error_matching = 1 - pearsonr(x, smoothed)[0]

    def _process_file(self, clip, windows):
        t0, t1 = 0., 30.; arr = clip.values
        spectrum_plt, ax = plt.subplots(figsize=(12, 8))
        ax.clear()
        ax.plot(np.linspace(t0, t1, arr.shape[0]), arr, linewidth=0.05)
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Amplitude')
        
        spec_stft = spectrogram.STFT.from_audio(clip)
        sftf_plt = spec_stft.display()[0].get_figure()
        
        mel_norm_plt = spectrogram.MelSpectrogram.from_audio(clip).amplitude_to_db().normalize().display()[0].get_figure()
        
        fingerprint_params = dict(
            spectrogramFct=spectrogram.MelSpectrogram,
            filter_fct=filtrations.intensity,
            compute_ph=ph.compute_ph_super_level,
            vect={0: BettiCurveExact(True), 1: BettiCurveExact(True)}
        )
        lambda_value = 0.3; weights = np.array([lambda_value, 1.-lambda_value])
        
        # windows = get_windows_from_audio(clip, spectrogram.MelSpectrogram)
        key = (2.4,3.4)
        mel_freq_plt = windows[key].amplitude_to_db().normalize().display()[0].get_figure()
        
        bc = window_to_ph_vector(windows[key], compute_ph=fingerprint_params["compute_ph"],
                                filter_fct=fingerprint_params["filter_fct"],
                                vect=fingerprint_params["vect"])
        betty_plt, ax = plt.subplots(1, 1, figsize=(12,8),)
        for dim, s in zip(range(2), ['-', '-']):
            ax.semilogy(bc[dim][0], bc[dim][1], s, label = 'dim {0}'.format(dim))
        ax.set_ylim(top=1000)
        ax.set_ylabel('Betti number')
        ax.set_xlabel('Intensity level')
        ax.legend(fontsize='xx-large')

        return {
            'sftf': sftf_plt,
            'spectrum': spectrum_plt,
            'mel_norm': mel_norm_plt,
            'mel_freq': mel_freq_plt,
            'betty': betty_plt
        }


        # return (sftf_plt, spectrum_plt, mel_norm_plt, mel_freq_plt, betty_plt)


if __name__ == '__main__':
    mgr = FingerprintManager()
    mgr.process(r'C:\Users\Home\Desktop\top_audio_id\data\jazzy-abstract-beat-11254.mp3', 
                r'C:\Users\Home\Desktop\top_audio_id\data\jazzy-abstract-beat-11254.mp3')
    # fig = mgr.left_plot1()
    print('SHOW')
    fig = mgr.cost_mat_plt
    
    fig.show()
    input()