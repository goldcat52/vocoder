# -*- coding: latin-1 -*-
"""
This module was created by Silas Gyger, silasgyger@gmail.com.
It stands under CC BY 4.0 License.
http://creativecommons.org/licenses/by/4.0/
"""

import thinkdsp
import numpy as np
from matplotlib import pyplot


class Wave(thinkdsp.Wave):
	def __getitem__(self, key):
		return self.ys[key]

	def __setitem__(self, key, value):
		self.ys[key] = value
		return self

	@property
	def length(self):
		return len(self.ys)

	def multiply_with(self, obj):
		"""
		Multipliziert alle y-Werte mit den y-Werte einer anderen Welle oder einem Array.
		:param obj: toolset.Wave, thinkdsp.Wave or np.array
		:return: self
		"""
		assert isinstance(obj, (Wave, thinkdsp.Wave, np.ndarray)), "The object this Wave should be multiplied with must" \
			" either be a %s, %s or a %s instance." % (Wave, thinkdsp.Wave, np.ndarray)

		if isinstance(obj, (Wave, thinkdsp.Wave)):
			self.ys *= obj.ys
		else:
			self.ys *= obj

		return self

	def make_average_amp_curve(self, buffer_size=800):
		"""
		Creates an amp-curve using the "average" algorithm.
		:return: array containing amps
		"""
		positive = lambda x: 0 if x < 0 else x

		amps = np.zeros(self.length)
		for i, y in enumerate(self.ys):
			buffer_ys = self.ys[positive(i-buffer_size/2):i+buffer_size/2]
			amps[i] = abs(np.sum(np.abs(buffer_ys))/buffer_size)

		return amps

	def make_spectrum(self):
		"""Computes the spectrum using FFT.

		returns: Spectrum
		"""
		hs = np.fft.rfft(self.ys)
		return Spectrum(hs, self.framerate)


class Spectrum(thinkdsp.Spectrum):
	def band_pass(self, position, range, factor=0):
		"""
		Attenuate all frequencies except the ones inside the cutoffs.
		low_cutoff: frequency in Hz
		high_cutoff: frequency in Hz
		factor: what to multiply the magnitude by
		"""
		low_cutoff, high_cutoff = position-range, position+range

		self.high_pass(low_cutoff, factor)
		self.low_pass(high_cutoff, factor)

	def make_wave(self):
		"""Transforms to the time domain.

		returns: Wave
		"""
		ys = np.fft.irfft(self.hs)
		return Wave(ys, self.framerate)


def to_wave(obj, framerate=None):
	"""
	Converts a thinkdsp-Wave or a numpy-Array to a toolset.Wave.

	:param obj: The wave/array
	:param framerate: Framerate of wanted wave if obj is a numpy array
	"""
	if isinstance(obj, thinkdsp.Wave):
		return Wave(obj.ys, obj.framerate)
	if isinstance(obj, np.ndarray):
		if framerate is None:
			raise ValueError, "Missing framerate to covert numpy-Array to wave."
		else:
			return Wave(obj, framerate)
