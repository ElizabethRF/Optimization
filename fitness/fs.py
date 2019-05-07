#!/usr/bin/python
# -*- coding: iso-8859-1 -*-


# Adjust sensibility factor to insuline and ratio I/R (insuline carbohydrates)

print 'chromosome [ FS, I/R ], alphabet [0, 50], type: floating'

# Data: a set of observation values: g0, I, R, g4
# real data from patient Joan
# found: 1.33 26.07 (63.35)
samples = [
[369, 14, 6, 204],
[280, 11, 3.5, 220],
[72, 5, 3.5, 72],
[317, 9, 3.5, 124],
[161, 6, 3.5, 58],
[220, 7, 3.5, 242],
[362, 11, 3.5, 144],
[284, 8, 3.5, 281],
[232, 8, 3.5, 86],
[209, 7, 3.5, 171],
[226, 8, 4.0, 70],
[152, 6, 3.5, 72],
[202, 7, 3.5, 284],
[241, 8, 3.5, 134],
[235, 9, 3.5, 51],
[168, 6, 3.5, 174],
[155, 6, 3.5, 184],
[162, 6, 3.5, 101],
[185, 7, 3.5, 68],
[268, 8, 3.5, 231],
[197, 5, 3.5, 107],
[92, 5, 3.5, 79],
[216, 7, 3.5, 71],
[313, 9, 3.5, 230],
[257, 8, 3.5, 101],
[173, 7, 3.5, 115],
[169, 7, 3.5, 165],
[264, 8, 3.5, 201],
[196, 7, 3.5, 75],
[84, 5, 3.5, 107],
[257, 8, 3.5, 95],
[186, 7, 3.5, 239],
[198, 7, 3.5, 85],
[210, 7, 3.5, 246],
[144, 6, 3.5, 88],
[73, 5, 3.5, 72],
[107, 5, 3.5, 107],
[201, 7, 3.5, 195],
]

def g4 (g0, I, R, IR, FS): # estimated glucose in 4 hours
	#return g0 + FS * (R*IR - I)
	return g0 + (R*IR)*FS - FS*I

import math

def error (chromosome):
	res = 0.0
	for sample in samples:
		res += (sample[3]-g4(sample[0],sample[1],sample[2],chromosome[0],chromosome[1]))**2
	return (res/len(samples))**0.5

def phenotype (chromosome): # for pretty print
	res = ''
	for g in chromosome:
		res += "%4.2f " % (g)
	res += '(%4.2f)' % (error(chromosome))
	return res

# now is the fitness function

def fitness (chromosome):
	return 1.0 / (1.0 + error(chromosome))


# force parameters

parameters = { 'alphabet':[0, 50], 'type':'floating', 'elitism':True, 'norm':True, 'chromsize':2, 'pmut':0.2 }
