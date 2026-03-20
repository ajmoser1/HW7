"""
Procedural synth audio system for Vaporwave Terminal Defense.
Generates all sounds at runtime using numpy - no external audio files needed.
"""
import numpy as np
import pygame


class AudioManager:
    def __init__(self):
        self.enabled = True
        self._sounds = {}
        try:
            # pygame.mixer should already be initialized via pygame.init()
            self._generate_sounds()
        except Exception:
            self.enabled = False

    def _make_sound(self, samples):
        """Convert a numpy array of float samples [-1, 1] to a pygame Sound."""
        # Stereo, 16-bit signed
        samples = np.clip(samples, -1.0, 1.0)
        int_samples = (samples * 32767).astype(np.int16)
        stereo = np.column_stack((int_samples, int_samples))
        return pygame.sndarray.make_sound(stereo)

    def _sine(self, freq, duration, sample_rate=44100):
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        return np.sin(2 * np.pi * freq * t)

    def _generate_sounds(self):
        sr = 44100

        # --- Tower placement: ascending chime ---
        dur = 0.15
        t = np.linspace(0, dur, int(sr * dur), endpoint=False)
        chime = 0.3 * np.sin(2 * np.pi * 880 * t) * np.exp(-t * 15)
        chime += 0.2 * np.sin(2 * np.pi * 1320 * t) * np.exp(-t * 12)
        self._sounds["place"] = self._make_sound(chime)

        # --- Shoot: quick zap ---
        dur = 0.08
        t = np.linspace(0, dur, int(sr * dur), endpoint=False)
        freq_sweep = np.linspace(2000, 400, len(t))
        zap = 0.2 * np.sin(2 * np.pi * freq_sweep * t / sr * sr) * np.exp(-t * 30)
        self._sounds["shoot"] = self._make_sound(zap)

        # --- Enemy death: descending burst ---
        dur = 0.2
        t = np.linspace(0, dur, int(sr * dur), endpoint=False)
        freq_sweep = np.linspace(600, 100, len(t))
        death = 0.25 * np.sin(2 * np.pi * freq_sweep * t / sr * sr) * np.exp(-t * 12)
        death += 0.1 * np.random.uniform(-1, 1, len(t)) * np.exp(-t * 20)
        self._sounds["death"] = self._make_sound(death)

        # --- Wave start: rising arpeggio ---
        notes = [440, 554, 659, 880]
        arp = np.array([], dtype=np.float64)
        for note in notes:
            dur = 0.1
            t = np.linspace(0, dur, int(sr * dur), endpoint=False)
            tone = 0.25 * np.sin(2 * np.pi * note * t) * np.exp(-t * 8)
            arp = np.concatenate([arp, tone])
        self._sounds["wave"] = self._make_sound(arp)

        # --- Game over: low doom chord ---
        dur = 0.8
        t = np.linspace(0, dur, int(sr * dur), endpoint=False)
        doom = 0.2 * np.sin(2 * np.pi * 110 * t) * np.exp(-t * 3)
        doom += 0.15 * np.sin(2 * np.pi * 138.59 * t) * np.exp(-t * 3)
        doom += 0.1 * np.sin(2 * np.pi * 164.81 * t) * np.exp(-t * 4)
        self._sounds["gameover"] = self._make_sound(doom)

        # --- BGM: simple synthwave loop ---
        self._generate_bgm(sr)

    def _generate_bgm(self, sr):
        """Generate a short synthwave loop."""
        bpm = 100
        beat = 60.0 / bpm
        bar = beat * 4
        duration = bar * 4  # 4 bars

        t = np.linspace(0, duration, int(sr * duration), endpoint=False)

        # Bass line (root notes of chord progression: Am - F - C - G)
        bass_freqs = [110, 87.31, 130.81, 98.0]
        bass = np.zeros_like(t)
        for i, freq in enumerate(bass_freqs):
            start = int(i * bar * sr)
            end = int((i + 1) * bar * sr)
            seg_t = t[start:end] - t[start]
            # Saw-like bass with envelope per beat
            seg = np.zeros(end - start)
            for b in range(4):
                b_start = int(b * beat * sr)
                b_end = min(int((b + 0.8) * beat * sr), len(seg))
                if b_start < len(seg):
                    bt = np.arange(b_end - b_start) / sr
                    env = np.exp(-bt * 4)
                    seg[b_start:b_end] += 0.15 * np.sign(np.sin(2 * np.pi * freq * bt)) * env
            bass[start:end] = seg

        # Pad (soft chords)
        pad_chords = [
            [220, 261.63, 329.63],  # Am
            [174.61, 220, 261.63],  # F
            [261.63, 329.63, 392],  # C
            [196, 246.94, 293.66],  # G
        ]
        pad = np.zeros_like(t)
        for i, chord in enumerate(pad_chords):
            start = int(i * bar * sr)
            end = int((i + 1) * bar * sr)
            seg_t = t[start:end] - t[start]
            env = 0.5 * (1 - np.exp(-seg_t * 2)) * np.exp(-seg_t * 0.3)
            for freq in chord:
                pad[start:end] += 0.04 * np.sin(2 * np.pi * freq * seg_t) * env

        bgm = bass + pad
        # Normalize
        peak = np.max(np.abs(bgm))
        if peak > 0:
            bgm = bgm / peak * 0.3

        self._sounds["bgm"] = self._make_sound(bgm)

    def toggle(self):
        self.enabled = not self.enabled
        if not self.enabled:
            pygame.mixer.stop()

    def play(self, name):
        if self.enabled and name in self._sounds:
            self._sounds[name].play()

    def play_bgm(self):
        if self.enabled and "bgm" in self._sounds:
            self._sounds["bgm"].play(loops=-1)

    def stop_bgm(self):
        if "bgm" in self._sounds:
            self._sounds["bgm"].stop()
