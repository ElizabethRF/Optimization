#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# This file defines fitness to find the coeficients of a fourier series giving a set of values x, p(x)

# how to use SALGA

# first, define a fenotype function (optional): given a chromosome returns an individual
# If defined, it's used only to print the best generation individual

import matplotlib.pyplot as plt

def phenotype (chromosome):
	res = ''
	for g in chromosome:
		res += "%4.2f " % (g)
	res += '(MAE: %4.2f)' % MAE(chromosome)

	y2 = []
	for v in x:
		y2.append(fourier(chromosome,v))
	l1.set_ydata(y1)
	l2.set_ydata(y2)

	return res


# second, define a fitness function (mandatory): given an chromosome, returns a number indicating the goodness of that chromosome

import math

N = 100
x = [p * 0.1 for p in range(-N, N)]
T = N*2.0*0.1

def fourier (chromosome, x): # evaluates a fourier series with coeficientes in chromosome for x
	res = chromosome[0]/2.0 # a0 term
	l = len(chromosome)
	for i in range(1,l,2):
		n = (i+1)/2 # n-th term
		res += chromosome[i]*math.cos(2.0*math.pi*n*x/T) + chromosome[i+1]*math.sin(2.0*math.pi*n*x/T)
	return res

# target coeficients to search
import random
size = 21 # must be odd because a0
target = []
for i in range(size):
	target.append(random.random())


# calculates set of points to evaluate error
print fourier(target,0.0)
y = []
for v in x:
	y.append(fourier(target,v))

# https://stackoverflow.com/questions/4098131/how-to-update-a-plot-in-matplotlib
plt.ion()
fig = plt.figure()
axes = fig.add_subplot(111)
y1 = y[:]
l1, = axes.plot(x,y1,'r')
l2, = axes.plot(x,y1,'b')


# here is the fitness function

def MAE (chromosome):
	error = 0.0
	for i in range(len(x)):
		error += math.fabs(y[i]-fourier(chromosome,x[i]))
	return error / len(x)

def fitness (chromosome):
	error = MAE(chromosome)
	return 1.0 / (1.0 + error)


# third: force parameters

parameters = { 'alphabet':[-15, 15], 'type':'floating', 'elitism':False, 'norm':True, 'chromsize':size, 'pmut':0.1, 'pcross':0.5, 'target':0.999 }
