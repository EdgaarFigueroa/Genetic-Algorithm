import random
import math

def getPopulation():
    x=[]
    for i in range(0,10):
        x.append(random.randint(0,1557))
    return x

def cleanList(x):
    for j in range(0,len(x)) :   
        for j in range(0,len(x)):
            x.pop(j)
            break

def genotype(x):
    genotipo=[]
    for i in range(0,len(x)):
        y=bin(x[i])
        y=y[2:]
        if x[i] ==0 or x[i]==1:
            y="0000000000"+y
        elif x[i]<=3 and x[i]>=2:
            y="000000000"+y
        elif x[i]<=7 and x[i]>=4:
            y="00000000"+y
        elif x[i]<=15 and x[i]>=8:
            y="0000000"+y
        elif x[i]<=31 and x[i]>=16:
            y="000000"+y
        elif x[i]<=63 and x[i]>=32:
            y="00000"+y
        elif x[i]<=127 and x[i]>=64:
            y="0000"+y
        elif x[i]<=255 and x[i]>=128:
            y="000"+y
        elif x[i]<=511 and x[i]>=256:
            y="00"+y
        elif x[i]<=1023 and x[i]>=512:
            y="0"+y
        genotipo.append(y)
    return genotipo
    
def fenotype(x):
    digito=[]
    numero=0
    for i in x:
        digito.append(int(i))
    for i in range (0,4):
        numero+=digito[i]*(2**(i))
    return numero

def degToRad(x):
    return x*math.pi/180

def fitnessFun(x,data):
    #AQUI SE CAMBIA
    while True:
        for row in range(len(x)):
            for col in range(len(x[0])):
                if col>len(x[0])-1:
                    continue
                if x[row][col]==0:
                    data[row].pop(col)
                    x[row].pop(col)

    return abs((x-5)/(2+math.sin(x)))

def prob(x):
    total=0
    prob=[]
    while(total==0):
        for i in range(0,len(x)):
            total+=x[i]
        for i in range(0,len(x)):
            prob.append(x[i]/total)
    return prob

def probAcumu(x):
    aux=0
    probAcum=[]
    for i in range(0,len(x)):
        aux+=x[i]
        probAcum.append(aux)
    return probAcum

def rouletteSelection(population):
    ##MODIFICAR AQUÍ
    p=population.copy()
    p1=p.copy()
    proba=[]
    probAcum=[]
    proba2=[]
    probAcum2=[]
    proba3=[]
    probAcum3=[]
    aux=0
    Pc=.85
    elected=[]
    elected2=[]
    elected3=[]

    while(aux==0):
        proba=prob(population)
        probAcum=probAcumu(proba)
        x=[random.random(),random.random()]
        y=random.random()
        x.sort()
        for i in range(0,len(p1)):
            if probAcum[i]>x[0]:
                elected.append(p1[i])
                probAcum.pop(i)
                p1.pop(i)
                break
        for i in range(0,len(p1)):
            if probAcum[i]>x[1]:
                elected.append(p1[i])
                p1.pop(i)
                break
            if i==len(p)-1 and len(elected)==1:
                elected.append(p1[i])
                break
        if y<Pc and len(elected)==2:
            aux=1
        else:
            p1=p.copy()
            if len(elected)!=0:
                cleanList(elected)
    aux=0
    while(aux==0):
        proba2=prob(p1)
        probAcum2=probAcumu(proba2)
        x=[random.random(),random.random()]
        y=random.random()
        x.sort()
        for i in range(0,len(p1)):
            if probAcum2[i]>x[0]:
                elected2.append(p1[i])
                p1.pop(i)
                probAcum2.pop(i)
                break
        for i in range(0,len(p1)):
            if probAcum2[i]>x[1]:
                elected2.append(p1[i])
                p1.pop(i)
                break
            if i==len(p1)-1 and len(elected2)==1:
                elected2.append(p1[i])
                break
        if y<Pc and len(elected2)==2:
            aux=1
        else:
            p1=p.copy()
            if len(elected2)!=0:
                cleanList(elected2)
    aux=0
    while(aux==0):
        elected3.append(p1[0])
        z=random.random()
        y=random.random()
        p.remove(p1[0])
        proba3=prob(p)
        probAcum3=probAcumu(proba3)
        for i in range(0,len(p)):
            if probAcum3[i]>z:
                elected3.append(p[i])
                break
        if y<Pc and len(elected3)==2:
            aux=1
        else:
            p=population.copy()
            if len(elected3)!=0:
                cleanList(elected3)
    cleanList(population)
    recombination(elected,population,0)
    recombination(elected2,population,1)
    recombination(elected3,population,2)

def recombination(elected,population,aux):
    hijos=[]
    gen=genotype(elected)
    y=random.randint(0,4)
    cadenaPadre=gen[0]
    cadenaPadre1=cadenaPadre[:y]
    cadenaPadre2=cadenaPadre[y:]
    cadenaMadre=gen[1]
    cadenaMadre1=cadenaMadre[y:]
    cadenaMadre2=cadenaMadre[:y]
    hijos.append(cadenaPadre1+cadenaMadre1)
    hijos.append(cadenaMadre2+cadenaPadre2)
    mutation(hijos,elected,aux,population)



def mutation(hijos,elected,aux, population):
    probMut=[]
    offspring=[]
    Pm=.1
    for i in range(0, len(hijos[0])):
        probMut.append(random.random())
    for i in range(0,len(hijos)):
        for j in range(0,len(hijos[0])):
            if probMut[j]<Pm:
                padre=hijos[i]
                if padre[j]=="0":
                    padre=padre[:j]+"1"+padre[j+1:]
                    
                else:
                    padre=padre[:j]+"0"+padre[j+1:]
                    
                hijos[i]=padre
            else:
                break
    offspring.append(elected[0])
    offspring.append(elected[1])
    offspring.append(fenotype(hijos[0]))
    offspring.append(fenotype(hijos[1]))
    replacement(offspring,aux, population)

def replacement(offspring,aux, population):
    ##MODIFICAR AQUÍ
    padre=[]
    hijo=[]
    fxPadre=[]
    fxHijo=[]
    padre.append(offspring[0])
    padre.append(offspring[1])
    hijo.append(offspring[2])
    hijo.append(offspring[3])
    for i in padre:
        fxPadre.append(fitnessFun(i))
    for i in hijo:
        fxHijo.append(fitnessFun(i))

    if aux<2:
        for j in range(0,2):
            maxPadre=max(fxPadre)
            maxHijo=max(fxHijo)
            if maxPadre<maxHijo:
                population.append(hijo[fxHijo.index(maxHijo)])
                fxHijo.remove(maxHijo)
            if maxHijo<maxPadre:
                population.append(padre[fxPadre.index(maxPadre)])
                fxPadre.remove(maxPadre)
            if maxHijo==maxPadre:
                population.append(hijo[fxHijo.index(maxHijo)])
                fxHijo.remove(maxHijo)
    else:
        maxPadre=max(fxPadre)
        maxHijo=max(fxHijo)
        if maxPadre<maxHijo:
                population.append(hijo[fxHijo.index(maxHijo)])
        if maxHijo<maxPadre:
                population.append(padre[fxPadre.index(maxPadre)])
        if maxHijo==maxPadre:
                population.append(hijo[fxHijo.index(maxHijo)])

def geneticAlgorithm(population):
    print("Generación 0 ->Fenotype: ", population)
    print("Genotype: ", genotype(population))
    for j in range(0,1000):
        rouletteSelection(population)
        print("Generación ",j+1," ->Fenotype: ",population )
        print("Genotype: ", genotype(population))
    


population=getPopulation()
geneticAlgorithm(population)