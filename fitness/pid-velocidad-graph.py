#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# This file defines PID control for car velocity
# and defina fitness for adjust parameters Kp, Ti and Td of PID

import math
import matplotlib.pyplot as plt

p = 0.1
def velocity (ut, ut10, v1):
	acelmax = 12.8
	if v1==0: resistencia=0
	else: resistencia = 0.116*math.log(v1)+0.2255
	inercia = ut10*acelmax*p
	return ut*acelmax*p - resistencia + inercia + v1

N = 8

def PID (signal, v1, v2, Kp, Ti, Td):
	# implementa un controlador PID de parámetros Kp, Ti, Td para ajustar velocidades
	global P, I, D
	error = signal-v1
	P = Kp*error
	aux = Td+N*p
	D = Td/aux*D - Kp*Td*N/aux*(v1-v2)
	res = P+I+D
	if Ti==0: I=0
	else: I = I + Kp*p/Ti*error
	if res>1: res=1
	elif res<0: res=0
	return res

def control (Kp, Ti, Td, signal1, signal):
	# calcula los parámetros ts, d, overshoot, ess que miden la bondad de una regulación
	global P, I, D
	P = I = D = 0
	v1 = v2 = signal1
	over = v1
	vut = [0]*10
	tsok = False
	ts = 1.0
	N = 250 # número de iteraciones para estabilización
	sign = math.copysign(1,signal-signal1)
	cambiosign = 0
	for ite in range(N):
		ut = PID(signal,v1,v2,Kp,Ti,Td)
		v2 = v1
		v1 = velocity(ut,vut[ite],v1)
		if signal>=signal1 and v1>over: over=v1
		if signal<signal1 and v1<over: over=v1
		if (v1-v2)*sign<0:
			cambiosign += 1
		sign = math.copysign(1,v1-v2)
		if not tsok and abs(v1-signal)<signal*0.01:
			tsok = True
			ts = float(ite)/N
		vut.append(ut)
		evolucion.append(v1) # almacena para pintar en phenotype
		#errors.append((v1-signal)**2) # prueba
	ess = abs(v1-signal)/10.0
	overshoot = abs(over-signal)/10.0
	d = cambiosign/50.0
	#print [ts, d, overshoot, ess]
	return [ts, d, overshoot, ess]
	#return errors # prueba

# how to use SALGA

# first, define a fenotype function (optional): given a chromosome returns an individual
# If defined, it's used only to print the best generation individual

def errors (chromosome): # calcula el error en tres situaciones: paso de 0 a 50, paso de 50 a 30 y paso de 30 a 100. Mide la bondad de la salida de velocidad conseguida
	global evolucion
	evolucion = [] # para pintar graficamente la evolucion
	return control(chromosome[0],chromosome[1],chromosome[2],0,50)+control(chromosome[0],chromosome[1],chromosome[2],50,30)+control(chromosome[0],chromosome[1],chromosome[2],30,100)

def globalerror (l): # calcula el error global de una lista de errores
	return sum(l) # sumatorio de errores
	#return sum(l)+10.0*max(l) # sumatorio de errores penalizando el peor error

def pinta ():
	plt.cla()
	plt.axhline(y=50, color='r', linestyle='-')
	plt.axhline(y=30, color='r', linestyle='-')
	plt.axhline(y=100, color='r', linestyle='-')
	#axes.set_ylim(ylim)
	plt.plot(evolucion,'b')

def phenotype (chromosome):
	print chromosome
	c = errors(chromosome)
	e = globalerror(c)
	print 'Errors: ', c, e
	#pinta()
	l1.set_ydata(evolucion)
	plt.title('Genetic. Error=%4.2f' % e)

	return "Kp: %4.2f; Ti: %4.2f; Td: %4.2f (%4.2f)" % (chromosome[0],chromosome[1],chromosome[2],e)


# inicializa gráfico
plt.ion()

print 'Datos de partida encontrados por el diseñador'
e = globalerror(errors([0.11,80,0.6]))
print e
pinta()
plt.title('Human design. Error=%4.2f' % e)

print 'Datos encontrados por el genético'
print globalerror(errors([0.099128576669451, 56.62227472405584, 0.2971897528352121]))
print 'Datos encontrados por el memético'
print globalerror(errors([0.10257676913415392, 57.364802707683154, 0.31625609413267364]))

fig = plt.figure()
axes = fig.add_subplot(111)
ylim = axes.set_ylim(0.0,110)
l1, = axes.plot(evolucion, 'b')
plt.axhline(y=50, color='r', linestyle='-')
plt.axhline(y=30, color='r', linestyle='-')
plt.axhline(y=100, color='r', linestyle='-')

# second, define a fitness function (mandatory): given an chromosome, returns a number indicating the goodness of that chromosome

def fitness (chromosome):
	#errors = control(chromosome[0],chromosome[1],chromosome[2],0,50)#+control(chromosome[0],chromosome[1],chromosome[2],50,30)+control(chromosome[0],chromosome[1],chromosome[2],30,100)
	e = errors(chromosome)
	error = globalerror(e)
	return 1.0 / (1.0 + error)


# third: force parameters

parameters = { 'alphabet':[0, 100], 'type':'floating', 'elitism':True, 'norm':True, 'chromsize':3, 'pmut':0.2, 'popsize':100 }

# Explicar Goodhart Law
