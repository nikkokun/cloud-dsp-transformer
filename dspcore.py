import librosa
import soundfile as sf
import os

filename='testdata/Tüngtwist.wav'
path=os.path.join('./output',os.path.split(filename)[1])

y, sr = librosa.load(filename)

def stretch(factor):
   y_2 = librosa.effects.time_stretch(y, factor)
   return y_2

def pitchShift(cents):
   y_2 = librosa.effects.pitch_shift(y, sr, cents)
   return y_2

def percussive():
   y_2 = librosa.effects.percussive(y, margin=2.0)
   return y_2

def harmonic():
   y_2 = librosa.effects.harmonic(y, margin=2.0)
   return y_2

def dj(size):
   _, beat_frames = librosa.beat.beat_track(y=y, sr=sr,hop_length=512)
   beat_samples = librosa.frames_to_samples(beat_frames)
   intervals = librosa.util.frame(beat_samples, frame_length=2,hop_length=1).T
   y_2 = librosa.effects.remix(y, intervals[::size])
   return y_2

def write():
   
def main():
   dj(4)
   return

if __name__=='__main__':
   main()