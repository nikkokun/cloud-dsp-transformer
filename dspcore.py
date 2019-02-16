import librosa
import soundfile as sf
import os
import numpy as np

def loadFile(filepath):
   y, sr = librosa.load(filepath)
   return y,sr


def stretch(filename, factor):
   y,sr= loadFile(filename)
   y_2 = librosa.effects.time_stretch(y, factor)
   output_path=os.path.join('./output',os.path.split(filename)[1])
   sf.write(output_path,y_2,sr)
   return output_path

def pitchShift(filename, cents):
   y,sr= loadFile(filename)
   y_2 = librosa.effects.pitch_shift(y, sr, cents)
   output_path=os.path.join('./output',os.path.split(filename)[1])
   sf.write(output_path,y_2,sr)
   return output_path

def percussive(filename, x):
   y,sr= loadFile(filename)
   y_2 = librosa.effects.percussive(y, margin=x)
   output_path=os.path.join('./output',os.path.split(filename)[1])
   sf.write(output_path,y_2,sr)
   return output_path

def harmonic(filename, x):
   y,sr= loadFile(filename)
   y_2 = librosa.effects.harmonic(y, margin=x)
   output_path=os.path.join('./output',os.path.split(filename)[1])
   sf.write(output_path,y_2,sr)
   return output_path

def dj(filename, size):
   y,sr= loadFile(filename)
   _, beat_frames = librosa.beat.beat_track(y=y, sr=sr,hop_length=512)
   beat_samples = librosa.frames_to_samples(beat_frames)
   intervals = librosa.util.frame(beat_samples, frame_length=2,hop_length=1).T
   y_2 = librosa.effects.remix(y, intervals[::size])
   output_path=os.path.join('./output',os.path.split(filename)[1])
   sf.write(output_path,y_2,sr)
   return output_path

percussive('testdata/04_Sexy_and_I_Know_It.wav',10.0)