# -*- coding: latin-1 -*-

import thinkdsp
import math
import numpy as np
import copy
import toolset
from matplotlib import pyplot

class Vocoder(object):
	def __init__(self, framerate, window = np.hamming, num_filterbands = 20, chunk_size=1024):
		self.framerate = framerate
		self.num_filterbands = num_filterbands
		self.window = window(chunk_size)  # Signal-Fenster, f�r experimente
		# Speicherung der obligatorischen Chunk-Gr�sse
		self.chunk_size = chunk_size
		# Erstellung des Arrays, in dem sp�ter die hintere h�lfte des letzten Chunks gespeichert wird
		self.last_half_1 = np.array([np.zeros(chunk_size) for i in xrange(num_filterbands)])
		self.last_half_2 = np.array([np.zeros(chunk_size) for i in xrange(num_filterbands)])
		# Erstellen des Arrays, der die Frequenzen enth�lt: (framerate/2 = Nyquist-Freq)
		self.filter_frequencies = np.array([pow(framerate/2, 1.0/num_filterbands)**i for i in xrange(num_filterbands)])

	def vocode(self, wave_1, wave_2):
		# �berpr�fen, ob Wellen entweder wave oder numpy.array-Instanzen sind:
		assert isinstance(wave_1, (toolset.Wave, np.ndarray)), "Wave_1 must be %s" % repr(toolset.Wave)
		assert isinstance(wave_2, (toolset.Wave, np.ndarray)), "Wave_2 must be %s" % repr(toolset.Wave)

		# Falls die Wellen numpy-Arrays sind, auf Wellen konvertieren:
		if isinstance(wave_1, np.ndarray):
			wave_1 = toolset.Wave(wave_1, self.framerate)
		if isinstance(wave_2, np.ndarray):
			wave_2 = toolset.Wave(wave_2, self.framerate)

		# Die beiden Wellen auf dei korrekte Gr�sse Inspizieren:
		assert wave_1.length == self.chunk_size, "Length of wave_1 must be %i" % self.chunk_size
		assert wave_2.length == self.chunk_size, "Length of wave_2 must be %i" % self.chunk_size

		# Kreierung des arrays, der das Resultat des Algorithmus repr�sentieren wird:
		final_signal = np.zeros(self.chunk_size)

		# Kreieren der beiden Spektren:
		wave_1_spectrum = wave_1.make_spectrum()
		wave_2_spectrum = wave_2.make_spectrum()

		# �ber die einzelnen Frequenb�nder iterieren:
		for i, freq in enumerate(self.filter_frequencies):
			# Kopieren der Spektren:
			new_wave_1_spectrum = copy.deepcopy(wave_1_spectrum)
			new_wave_2_spectrum = copy.deepcopy(wave_2_spectrum)
			# Anwenden der Band-pass-filter: (Herausgefilterte signale sind immer von freq bis 2*freq)
			new_wave_1_spectrum.band_pass(freq+freq/2.0, freq/2.0)
			new_wave_2_spectrum.band_pass(freq+freq/2.0, freq/2.0)
			# Zur�ckverwandeln zu Wave:
			new_wave_1 = new_wave_1_spectrum.make_wave()
			new_wave_2 = new_wave_2_spectrum.make_wave()
			# Multiplizieren der zweiten welle mit der Amplitude der ersten:
			new_wave_1_amp_curve = new_wave_1.make_average_amp_curve()
			new_wave_2.multiply_with(new_wave_1_amp_curve)
			# F�ge das Resultat dem finalen Signal hinzu:
			final_signal += new_wave_2.ys

		return final_signal





