"""
    @autor: Varillas Figueroa Edgar Josue
    @date: 04/03/22
    @description: -
"""
import random
import math
import numpy as np

#Randomly generate the population
def getPopulation():
    x=[]
    for i in range(0,5):
        x.append(random.randint(0,15))
    return x

#Clear lists
def cleanList(x):
    for j in range(0,len(x)) :   
        for j in range(0,len(x)):
            x.pop(j)
            break

#Get the genotype
def genotype(x):
    gen=[]
    for i in range(0,len(x)):
        y=bin(x[i])
        y=y[2:]
        if x[i] ==0 or x[i]==1:
            y="000"+y
        if x[i]<=3 and x[i]>=2:
            y="00"+y
        if x[i]<=7 and x[i]>=4:
            y="0"+y
        gen.append(y)
    return gen

#Get the genotype    
def Phenotype(x):
    digit=[]
    phenotype=0
    for i in x:
        digit.append(int(i))
    for i in range (0,4):
        phenotype+=digit[i]*(2**(i))
    return phenotype

#Assess individuals on fitness function
def fitnessFun(x):
    return abs((x-5)/(2+math.sin(x)))

#Calculate the probability per individual
def Probability(x):
    total=sum(x)
    probability=[]
    for i in range(0,len(x)):
            probability.append(x[i]/total)
    return probability

#Calculate the cumulative probability
def cumulativeProbability(x):
    aux=0
    probability=[]
    for i in range(0,len(x)):
        aux+=x[i]
        probability.append(aux)
    return probability

#Selects parents for breeding and evaluates if they are suitable for reproduction
def rouletteSelection(population):
    p=population.copy()
    p1=p.copy()
    probability=[]
    cumulativeprobability=[]
    iteration=0
    Pc=.85
    elected=[]
    fx=[]

    cleanList(population)
    
    for m in range(0,3):
        for f in p:
                fx.append(fitnessFun(f))
        probability=Probability(fx)
        cumulativeprobability=cumulativeProbability(probability)
        while(iteration==0):
            x=[np.random.uniform(),np.random.uniform()]
            y=np.random.uniform()
            x.sort()
            for i in range(0,len(p1)):
                if cumulativeprobability[i]>x[0]:
                    elected.append(p1[i])
                    cumulativeprobability.pop(i)
                    p1.pop(i)
                    break
            for i in range(0,len(p1)):
                if cumulativeprobability[i]>x[1]:
                    elected.append(p1[i])
                    p1.pop(i)
                    break
                if i==len(p)-1 and len(elected)==1:
                    elected.append(p1[i])
                    break
            if y<=Pc and len(elected)==2:
                recombination(elected,population,m)
                p1=p.copy()
                cleanList(elected)
                break
            else:
                p1=p.copy()
                if len(elected)!=0:
                    cleanList(elected)


#Perform the crossing of the parents in 1 point.
def recombination(elected,population,aux):
    children=[]
    gen=genotype(elected)
    y=random.randint(0,4)
    fatherString=gen[0]
    fatherString1=fatherString[:y]
    fatherString2=fatherString[y:]
    motherString=gen[1]
    motherString1=motherString[y:]
    motherString2=motherString[:y]
    children.append(fatherString1+motherString1)
    children.append(motherString2+fatherString2)
    mutation(children,elected,aux,population)


#Performs mutation of offspring
def mutation(children,elected,aux, population):
    probMut=[]
    offspring=[]
    Pm=.1
    for i in range(0, len(children[0])):
        probMut.append(np.random.uniform())
    for i in range(0,len(children)):
        for j in range(0,len(children[0])):
            if probMut[j]<=Pm:
                parent=children[i]
                if parent[j]=="0":
                    parent=parent[:j]+"1"+parent[j+1:]
                    
                else:
                    parent=parent[:j]+"0"+parent[j+1:]
                    
                children[i]=parent
            else:
                break
    offspring.append(elected[0])
    offspring.append(elected[1])
    offspring.append(Phenotype(children[0]))
    offspring.append(Phenotype(children[1]))
    replacement(offspring,aux, population)

#The population is replaced by selecting the individuals with the best fitness
def replacement(offspring,aux, population):
    parent=[]
    child=[]
    fxParent=[]
    fxChild=[]
    parent.append(offspring[0])
    parent.append(offspring[1])
    child.append(offspring[2])
    child.append(offspring[3])
    for i in parent:
        fxParent.append(fitnessFun(i))
    for i in child:
        fxChild.append(fitnessFun(i))

    if aux<2:
        for j in range(0,2):
            maxParent=max(fxParent)
            maxChild=max(fxChild)
            if maxParent<maxChild:
                population.append(child[fxChild.index(maxChild)])
                fxChild.remove(maxChild)
            if maxChild<maxParent:
                population.append(parent[fxParent.index(maxParent)])
                fxParent.remove(maxParent)
            if maxChild==maxParent:
                population.append(child[fxChild.index(maxChild)])
                fxChild.remove(maxChild)
    else:
        maxParent=max(fxParent)
        maxChild=max(fxChild)
        if maxParent<maxChild:
                population.append(child[fxChild.index(maxChild)])
        if maxChild<maxParent:
                population.append(parent[fxParent.index(maxParent)])
        if maxChild==maxParent:
                population.append(child[fxChild.index(maxChild)])

#Main function
def geneticAlgorithm(population):
    print(f"Generación 0 ->Phenotype: {population}")
    print(f"Genotype: {genotype(population)}")
    for j in range(0,10):
        rouletteSelection(population)
        print(f"Generación {j+1} ->Phenotype: {population}")
        print(f"Genotype: {genotype(population)}")
    
population=getPopulation()
geneticAlgorithm(population)