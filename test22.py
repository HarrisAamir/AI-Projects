import random
N=0 
K=0 
T=0 
examDuration= 3  #exam time and slot time are same thus no extra time for halls
PopultaionSize=100 
cources=[]  
halls=[]
timeSlots=[]
population=[]
commonStu=[]
index_fitness=[] #list that contains indexs and fitness values of population 

#-----INPUT-------
N=int(input("Enter the number of cources (N): "))

K=int(input("Enter the number of exam halls (K): "))

T=int(input("Enter the max number of slots for all halls (each exam is 3 hours): "))
for i in range(N):
    cources.append(input("Enter name of cource #"+str((i+1))+": "))
for i in range(K):
    halls.append(str(i))
for i in range(T):
    timeSlots.append(str(i))
for i in  range(N):
    for j in range(i+1, N):
        commonStu.append((cources[i], cources[j], int(input("Enter the number of common students in "+cources[i]+" and "+cources[j]+": "))))
if K*T<N:
    print("----------------------------------------------------------") 
    print("Best solution not possible as slots are less then cources ")
    print("----------------------------------------------------------") 
#------GENERATING RANDOM POPULATION------
def genPopulation():
    for i in range(PopultaionSize):
        chromosom=[]
        courcesCopy=cources[:]
        for i in range(N):
            c = random.choice(courcesCopy)
            courcesCopy.remove(c)
            t=0
            k=0
            t= random.choice(timeSlots)
            k= random.choice(halls)
            values=(c,t,k)
            chromosom.append(values)
        population.append(chromosom)    

#-------CONSTRAINTS CHECK---------

def getFromTime(chromosom, time): # returns the list of cources on same time
    courceslist=[]
    for i in range(N):
       if chromosom[i][1]==time:
           courceslist.append(chromosom[i][0])
    return courceslist

def getStudentClashesCount(courceslist): #returns the count of students with clashes between the cources of courcelist
    for i in range(len(commonStu)):
        if commonStu[i][0]==courceslist[0] and commonStu[i][1]==courceslist[1]:
            return commonStu[i][2]
        elif commonStu[i][0]==courceslist[1] and commonStu[i][1]==courceslist[0]:
            return commonStu[i][2]
    return 0

#-----FITNESS FUNCTION-----------
def fitness(chromosom):
    slotslist=[] #contains all possible slots of halls
    courcesList=[] # saves all cources in the chromosoms
    fitnessVal=0 
   
    for i in range(N):
        courcesList.append(cources[i][0])
    # checking if all cources are not in chromosom

    for i in range(N):
        if chromosom[i][0] not in courcesList:
            return 10000

    #checking for clashes of slots (2 cources have same time and same location )
    for i in range(N):
     val=str(chromosom[i][1]) + str(chromosom[i][2])
     if val not in slotslist: 
         slotslist.append(val)
     else:
         return 1000  # checking no 2 cources have same time and same hall  
    
    #checking for hours 
    for i in range(N):
        for j in range(N):
            if i!=j and chromosom[i]==cources[j]: 
                if int(chromosom[i][1])+examDuration>T*3: # checking if the cource exceeds the max time of hall 
                    fitnessVal+=(10*((int(chromosom[i][1])+examDuration)-T*3)) # for every hour exceeding max time, 10 points are added

    #checking for clashes students 
    times=[chromosom[0][1]]
    for i in range(1,N):
        if chromosom[i][1] not in times:
            times.append(chromosom[i][1]) 
        else:
            courcesList=getFromTime(chromosom,chromosom[i][1])
            count= getStudentClashesCount(courcesList)
            fitnessVal+=count*100 # for every clashed student, 100 point are added

    return fitnessVal


#-----CROSSOVER FUNCTION------
def crossover(population):
    cutPoint=N/2
    for i in range(PopultaionSize-1):
        parent1=population[i]
        parent2=population[i+1]
        child1=[]
        child2=[]
        for j in range(N):
            if j < cutPoint: 
                child1.append(parent1[j])
            else: 
                child2.append(parent1[j])
        for j in range(N):
            if j < cutPoint:
                child2.append(parent2[j])
            else:
                child1.append(parent2[j])
        population.append(child1)
        population.append(child2)
    return population


#---MUTATION FUNCTION------
def mutation(population):
    for i in range(0,PopultaionSize-1):
        index=random.randint(0, N-1)
        chromosom1=population[i][:]
        chromosom2=population[i+1][:]
        temp=chromosom1[index]
        chromosom1[index]=chromosom2[index]
        chromosom2[index]=temp
        population.append(chromosom1)
        population.append(chromosom2)
    return population

def takeFitness(elem): #used in sorting
    return elem[1]


#----EVALUATING POPULATION-----
def evaluate(population,length): # returns the best chromosoms from population 
    indexList=[]
    for i in range(len(population)):
        indexList.append((i,fitness(population[i])))
    indexList.sort(key=takeFitness)
    pop=[]
    for i in range(length):
        pop.append(population[indexList[i][0]])
    return pop

#----CREATES A NEW POPULATION-----
def nextGen():
  #new population contains 50% old 40% crossover and 10% mutation
  crossoverPop=evaluate(crossover(population),int(PopultaionSize*0.4))
  mutationPop=evaluate(mutation(population),int(PopultaionSize*0.1))
  Pop=[]
  index_fitness.sort(key=takeFitness)
  for i in range(int(PopultaionSize*0.5)):
      Pop.insert(0,population[index_fitness[i][0]])
  for i in range(int(PopultaionSize*0.4)):
      Pop.insert(0,crossoverPop[i])
  for i in range(int(PopultaionSize*0.1)):
       Pop.insert(0,mutationPop[i])
  return Pop


def main():
    global population,index_fitness
    genPopulation()
    #----Saving indexs and their fitness values 
    for i in range(PopultaionSize):
        index_fitness.append([i,fitness(population[i])])
    #running for 100 generations
    for i in range(100): 
        nextgen=nextGen()
        index_fitness=[]
        print("---Generation---%d"%i)
        for j in range(PopultaionSize):
            index_fitness.append([j,fitness(nextgen[j])])
        print("Best Solution of this generation: \n"+str(nextgen[index_fitness[0][0]]))
        index_fitness.sort(key=takeFitness, reverse=True)
        population=nextgen
    print("\n************ FINAL ****************")
    print("------SOLUTION---------")
    print(population[index_fitness[0][0]])
    print("------FITNESS----------")
    print(index_fitness[0][1])
    print("*************************")
 
main()