import io
import requests
import numpy as np
import librosa
from vibe_profile import C4TimbreProfile, C6EnergyArc

def _load_preview_audio(url: str, sr: int = 22050):
    r = requests.get(url)
    r.raise_for_status()
    y, sr = librosa.load(io.BytesIO(r.content), sr=sr)
    return y, sr

def extract_c4_c6_from_preview(preview_url: str) -> tuple[C4TimbreProfile, C6EnergyArc]:
    y, sr = _load_preview_audio(preview_url)

    # Brightness via spectral centroid
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    brightness = float(np.clip((centroid.mean() - 2000.0) / 6000.0, 0.0, 1.0))

    # Warmth: energy in 200–800 Hz band
    S = np.abs(librosa.stft(y))
    freqs = librosa.fft_frequencies(sr=sr)
    warm_idx = (freqs >= 200) & (freqs <= 800)
    warmth_energy = S[warm_idx].mean()
    total_energy = S.mean()
    warmth = float(np.clip(warmth_energy / (total_energy + 1e-9), 0.0, 1.0))

    # Density: proportion of “active” bands
    threshold = S.mean() * 0.5
    band_activity = (S > threshold).mean(axis=1)
    density = float(np.clip(band_activity.mean(), 0.0, 1.0))

    # Width: unknown with mono preview, placeholder
    width = 0.5

    c4 = C4TimbreProfile(
        brightness=brightness,
        warmth=warmth,
        density=density,
        width=width,
    )

    # Energy arc: 5 RMS segments normalized so first ≈ 0.3
    segments = np.array_split(y, 5)
    rms_vals = np.array([np.sqrt(np.mean(seg**2)) for seg in segments])
    if rms_vals[0] == 0:
        scale = 1.0
    else:
        scale = 0.3 / rms_vals[0]
    arc = np.clip(rms_vals * scale, 0.0, 1.0)

    c6 = C6EnergyArc(
        v1=float(arc[0]),
        c1=float(arc[1]),
        v2=float(arc[2]),
        c2=float(arc[3]),
        b=float(arc[4]),
    )

    return c4, c6
