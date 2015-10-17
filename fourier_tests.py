# -*- coding: latin-1 -*-
import numpy as np
import pylab
from cmath import * # complex numbers
from matplotlib import pyplot

__author__ = 'Silas Gyger'

def fourier(v):
	n = len(v)
	c = [0+1j*0 for i in xrange(n)]

	print "Starting fourier-transformation of %i samples." % n

	prec_counter = 0

	for k in xrange(n):
		for i in xrange(n-1):
			deg = (2.0*np.pi*k*i)/n
			c[k] += v[i] * ( np.cos(deg)-1j*np.cos(deg))
		c[k]*= 1.0/n

		prec_counter += 1
		# Print out percentage:
		"""if prec_counter >= n / 100:
			prec_counter = 0
			print "Process: %i%%" % (1.0*k/n*100)"""

	return c

# Open file before algorithm starts, so when it fails to open, no time is wasted:
framerate = 20
xs = np.arange(0, 1, 1.0/framerate)
ys = 0.7 * np.cos(2*pi*xs)+0.3*np.cos(9*2*pi*xs)
cs = fourier(ys)
pyplot.plot(ys)
pyplot.show()
pyplot.plot(cs)
pyplot.show()
print cs

