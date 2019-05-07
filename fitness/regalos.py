#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# resuelve problema de examen de enero de 2017

import sets

precios = [62,55,17,115,40,65,80,83,99,49,25,30,22,30,30,50,70,60,58,110]
estrellas = [1,4,3,2,5,1,1,2,5,4,3,4,4,3,2,3,5,4,4,5]
presupuesto = 300.0

def fitness0 (chromosome):
	coste = 0.0
	maxc = precios[chromosome[0]]
	minc = precios[chromosome[0]]
	for r in chromosome:
		coste += precios[r] # acumula el coste total
		if precios[r]<minc:
			minc = precios[r]
		if precios[r]>maxc:
			maxc = precios[r]

	diferencia = maxc - minc # calcula la diferencia entre el más caro y el más barato
	return (coste,diferencia)

def phenotype (chromosome): # describe el cromosoma de modo legible
	coste, diferencia = fitness0(chromosome)
	costes = []
	for r in chromosome:
		costes.append(precios[r])
	return '%s %s (%s, %s)' % (chromosome, costes, coste, diferencia)

def fitness (chromosome):
	coste, diferencia = fitness0(chromosome)
	if coste>presupuesto: # si se pasa del presupuesto, fitness 0
		return 0.0
	total = 10 / (1.0 + (presupuesto - coste) + diferencia) # mayor cuanto más cerca del presupuesto y menor la diferencia
	if len(sets.Set(chromosome))<len(chromosome): # para evitar dos regalos iguales
		return 0.1 * total
	return total
