import librosa
import soundfile as sf

filename='testdata/BlueSea_A024.wav'

y, sr = librosa.load(filename)

def stretch():
   y_2 = librosa.effects.time_stretch(y, 0.5)
   sf.write(filename,y_2,sr)

def pitchShift():
   y_2 = librosa.effects.pitch_shift(y, sr, n_steps=4)
   sf.write(filename,y_2,sr)

pitchShift()