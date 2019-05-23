
import sets

#negra, rubia, baja graduacion
malta = [2, 1, 2]
levadura = [1, 2, 2]
beneficioList = [4, 7, 3]

def fitness0(chromosome): #calculo de parametros necesarios
    
    malt = 0
    lev = 0
    beneficio = 0
    print(len(chromosome))
    for r in range(len(chromosome)):
        malt += chromosome[r]*malta[r]
        lev += chromosome[r]*levadura[r]
        beneficio += chromosome[r]*beneficioList[r]
        
    return malt, lev, beneficio

def phenotype (chromosome): # describe el cromosoma de modo legible
    m, l, b = fitness0(chromosome)

    return '%s (%s, %s, %s)' % (chromosome, m, l, b)

def fitness(chromosome): #calculo de fitness, si no sobrepasa la disponibilidad de malta y levadura se observa el beneficio
    
    m, l, b = fitness0(chromosome)
    
    if(m>30 or l>45):
        return 0
    else:
        return b
    
parameters = {'alphabet':range(50), 'chromsize':3, 'target':160}