# -*- coding: latin-1 -*-

import numpy as np
import thinkdsp
from matplotlib import pyplot

beep_wave = thinkdsp.read_wave("Sounds\\sine.wav")
noise_wave = thinkdsp.read_wave("noise_looped_22050.wav")

noise_wave.truncate(len(beep_wave.ys))

amps = np.zeros(len(beep_wave))

framerate = beep_wave.framerate


rel_tmp = 0.0
attack_factor = 1.001  # s
release_factor = 0.9999  # s

smooth_amp = 1.0

release = np.zeros(len(beep_wave))

buffer_size = 800

buffer_ys = np.zeros(buffer_size)

for i, y in enumerate(beep_wave.ys):
	buffer_ys = beep_wave[i-buffer_size/2:i+buffer_size/2]
	amps[i] = abs(np.sum(np.abs(buffer_ys))/buffer_size)

pyplot.plot(beep_wave.ts, beep_wave.ys, "b")
pyplot.plot(beep_wave.ts, amps, "g")
pyplot.show()

noise_wave = thinkdsp.Wave(noise_wave.ys*amps, framerate)
noise_wave.normalize()
noise_wave.write("noise_wave_amplified_22050.wav")
