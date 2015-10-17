# -*- coding: latin-1 -*-

import numpy as np
from matplotlib import pyplot
import thinkdsp
import toolset

sin, cos, pi = np.sin, np.cos, np.pi


length = 1  # s
framerate = 11050  # fps


########
to_deg = lambda x: x*np.pi*2
ts = np.arange(0, length, 1.0/framerate)

def nyquist_4_graphs():
	framerate_2 = 20
	ts_2 = np.arange(0, length, 1.0/framerate_2)
	freq_1 = 4
	freq_2 = 12

	ys_1 = thinkdsp.Wave(sin(to_deg(ts)*freq_1), framerate)
	ys_2 = thinkdsp.Wave(sin(to_deg(ts_2)*freq_1), framerate_2)
	ys_3 = thinkdsp.Wave(sin(to_deg(ts)*freq_2), framerate)
	ys_4 = thinkdsp.Wave(sin(to_deg(ts_2)*freq_2), framerate_2)

	spect_1 = ys_1.make_spectrum()
	spect_2 = ys_2.make_spectrum()
	spect_3 = ys_3.make_spectrum()
	spect_4 = ys_4.make_spectrum()

	_, plotarr = pyplot.subplots(2, 2)
	plotarr[0, 0].plot(ts, ys_1.ys, "b")
	plotarr[0, 0].plot(ts_2, ys_2.ys, "r")
	plotarr[0, 0].set_xlabel("Zeit t in s")
	plotarr[0, 0].set_ylabel("Amplitude")

	plotarr[0, 1].plot(ts, ys_3.ys, "b")
	plotarr[0, 1].plot(ts_2, ys_4.ys, "r")
	plotarr[0, 1].set_xlabel("Zeit t in s")
	plotarr[0, 1].set_ylabel("Amplitude")

	max_f = framerate_2
	plotarr[1, 0].plot(spect_1.fs[:max_f], spect_1.amps[:max_f]/5500, "b")
	plotarr[1, 0].plot(spect_2.fs[:max_f], spect_2.amps[:max_f]/10, "r")
	plotarr[1, 0].set_xlabel("Frequenz in Hz")
	plotarr[1, 0].set_ylabel("Amplitude")
	plotarr[1, 0].annotate('Nyquist-Frequenz', xy=(10, 0), xytext=(10, 0.2),
				arrowprops=dict(facecolor='black', shrink=0.5))

	plotarr[1, 1].plot(spect_3.fs[:max_f], spect_3.amps[:max_f]/5500, "b")
	plotarr[1, 1].plot(spect_4.fs[:max_f], spect_4.amps[:max_f]/10, "r")
	plotarr[1, 1].set_xlabel("Frequenz in Hz")
	plotarr[1, 1].set_ylabel("Amplitude")
	plotarr[1, 1].annotate('Nyquist-Frequenz', xy=(10, 0), xytext=(10, 0.2),
				arrowprops=dict(facecolor='black', shrink=0.5))

def fourier_demo():
	freq_1 = 1
	freq_2 = 10

	ys_1 = sin(to_deg(ts)*freq_1)
	ys_2 = sin(to_deg(ts)*freq_2)
	ys_sum = ys_1 + ys_2

	spectrum = (thinkdsp.Wave(ys_sum, framerate)).make_spectrum()

	_, plotarr = pyplot.subplots(2, 1)

	plotarr[0].plot(ts, ys_1, "r")
	plotarr[0].plot(ts, ys_2, "g")
	plotarr[0].plot(ts, ys_sum, "b")
	plotarr[0].set_xlabel("Zeit t in s")
	plotarr[0].set_ylabel("Amplitudde")

	freq = 40
	plotarr[1].plot(spectrum.fs[:freq], spectrum.amps[:freq]/5500)
	plotarr[1].set_xlabel("Frequenz in Hz")
	plotarr[1].set_ylabel("Amplitude")

def two_waves():
	freq = 5

	ys_1 = ts % ts[len(ts)/freq]
	ys_2 = sin(ts*2*pi*5)

	_, plotarr = pyplot.subplots(2, 1)
	plotarr[0].plot(ts, ys_1)
	plotarr[0].set_xlabel("Zeit t in s")
	plotarr[0].set_ylabel("Amplitude")
	plotarr[1].plot(ts, ys_2)
	plotarr[1].set_xlabel("Zeit t in s")
	plotarr[1].set_ylabel("Amplitude")

def analyse(filename, resolution=100):
	print "Generating frequency-spectrogram for %s..." % filename
	low, high = 0, None
	try:
		wave = toolset.to_wave(thinkdsp.read_wave(filename))
	except:
		print "Couldn't load file %s. Returning with a silten error." % filename
		return False
	len_spetrogram = len(wave)/resolution*2
	spect = wave.make_spectrogram(len_spetrogram)
	_, plotarr = pyplot.subplots(2, 1)
	plotarr[0].plot(wave.ts, wave.ys)
	plotarr[0].set_xlabel("Zeit in s")
	plotarr[0].set_ylabel("Amplitude")

	ts = np.array(spect.times())
	if high == None:
		high = len(spect.frequencies())-1
	fs = np.array(spect.frequencies()[low:high])

	# make the array
	size = len(fs), len(ts)
	array = np.zeros(size, dtype=np.float)
	# copy amplitude from each spectrum into a column of the array
	for i, t in enumerate(ts):
		spectrum = spect.spec_map[t]
		array[:,i] = np.array(spectrum.amps[low:high])
	print("Generating graph...")
	plotarr[1].set_yscale("linear")
	plotarr[1].pcolor(ts, fs, array**0.5, cmap="nipy_spectral")
	plotarr[1].set_ylabel("Frequenz in Hz")
	plotarr[1].set_xlablel("Zeit in s")
	print("Saving image as \"res_%i_%s.png\"..." % (resolution, filename[:-4]))
	pyplot.savefig("Fourier-Results\\double\\res_%i_%s.png" % (framerate, filename.split("\\")[-1][:-4]))
	print("Done.")
	pyplot.cla()
	return True

"""files = ["noise_looped_22050.wav",
		 "vocoded_20_1024.wav",
		 "vocoded_20_2048.wav",
		 "vocoded_20_4096.wav",
		 "vocoded_20_4096_noise.wav",
		 "vocoded_20_4099_viola.wav",
		 "sounds\\buffalo_raw.wav",
		 "sounds\\buffalo_vocoder_noise_8.wav",
		 "sounds\\buffalo_synth.wav",
		 "sounds\\buffalo_viola.wav",
		 "sounds\\buffalo_vocoder_synth_20.wav",
		 "sounds\\buffalo_vocoder_synth_40.wav"
		 ]"""

files = [
	"vocoded_40_4096.wav",
	"vocoded_8_4096.wav",
	"vocoded_8_4096_noise.wav",
	"vocoded_100_4096.wav"
]

success = []
errors = []
for filename in files:
	print "\n# Processing sample %i of %i" % (files.index(filename)+1, len(files))
	if analyse(filename, 400):
		success.append(filename)
	else:
		errors.append(filename)
else:
	print "\n#################################"
	print "Following files were analyzed successfully:"
	for i in success: print("\t* "+i)
	print "Following files couldn't be loaded:"
	for i in errors: print("\t* "+i)