import thinkdsp
import toolset
import numpy as np
import vocoder as vc
from matplotlib import pyplot
import time
import sys

def vocode_audiofiles(filepath_1, filepath_2, num_filters=20, chunk_size=1024):
	"""
	"Fuses" two audiofiles using the Vocoder-algorithm.
	Note: If the length of the audiofiles differ, the longer file gets cut to the length of the shorter one.
	If the framerate differs, the file with the lower framerate is converted to the higher one, using the average-algorithm.
	# TODO: Implement what is described up there /\

	:param filepath_1 (str): Path to a .wav file
	:param filepath_2 (str): Path to a .wav file
	:param num_filters (int: Amount of filters the vocoder uses
	:param chunk_size (int): Size each chunk should have (debug)
	:return: toolset.Wave
	"""
	assert isinstance(filepath_1, str) and isinstance(filepath_1, str), "Filepaths must be of type %s" % type(" ")
	wave1 = toolset.to_wave(thinkdsp.read_wave(filepath_1))
	wave2 = toolset.to_wave(thinkdsp.read_wave(filepath_2))

	smaller_signal_length = min(wave1.length, wave2.length)

	result = np.zeros(smaller_signal_length-(smaller_signal_length % chunk_size))

	print "Starting to vocode two signals with length %i..." % smaller_signal_length

	vocoder = vc.Vocoder(wave1.framerate, np.hamming, num_filters, chunk_size)

	debug_num_chunks = (len(result)/chunk_size -1)
	debug_factor = 100.0 / debug_num_chunks
	for i in range(len(result)/chunk_size -1):
		# Status update:
		print "%g%% done, processing chunk no. %i out of %i " % (round(i * debug_factor, 2), i, debug_num_chunks)
		# Start - und ende des momentanen Chunks berechnen:
		start, end = i*chunk_size, (i+1)*chunk_size
		# Modulator- und Carrier-Chunk "herausschneiden":
		modulator = toolset.Wave(wave1.ys[start:end], wave1.framerate)
		carrier = toolset.Wave(wave2.ys[start:end], wave2.framerate)
		# Vocoder-Effekt auf die beiden Signale Anwenden:
		result[start:end] = vocoder.vocode(modulator, carrier)

	print "~job's done~"
	return toolset.Wave(result, wave1.framerate)
nf, cs = 100, 4096

result_wave = vocode_audiofiles("Sounds\\buffalo_raw.wav", "Sounds\\buffalo_synth.wav", num_filters=nf, chunk_size=cs)
result_wave.normalize()
result_wave.write("vocoded_%i_%i.wav" % (nf, cs))
