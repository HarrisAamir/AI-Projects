import random

N=int(input("Enter the number of cources (N): "))
K=int(input("Enter the number of exam halls (K): "))
T=int(input("Enter the max hours for all halls: "))

cources=[]
halls=[]
timeSlots=[]
chromosoms=[]
cells=[]
for i in range(N):
    cources.append((input("Enter name of cource #"+str((i+1))+": "),input("Enter the exam time for the cource (hours): ")))
    
# print(cources)

for i in range(K):
    halls.append(str(i))
# print(halls)

for i in range(T):
    timeSlots.append(str(i))
# print(timeSlots)

commonStu=[]

for i in range(N):
    for j in range(i+1, N):
        commonStu.append((cources[i][0], cources[j][0], int(input("Enter the number of common students in "+cources[i][0]+" and "+cources[j][0]+": "))))

print(commonStu)

def genPopulation():
    chromosom=[]
    courcesCopy=cources[:]
  
    for i in range(N):
        c = random.choice(courcesCopy)
        courcesCopy.remove(c)
        t=0
        k=0
        t= random.choice(timeSlots)
        k= random.choice(halls)
        values=(c[0],t,k)
        chromosom.append(values)
    chromosoms.append(chromosom)
        

for i in range(100):
    genPopulation()

print(chromosoms)

def getFromTime(chromosom, time):
    courceslist=[]
    for i in range(N):
       if chromosom[i][1]==time:
           courceslist.append(chromosom[i][0])
    return courceslist

def getStudentClashesCount(courceslist):
    for i in range(len(commonStu)):
        if commonStu[i][0]==courceslist[0] and commonStu[i][1]==courceslist[1]:
            return commonStu[i][2]
        elif commonStu[i][0]==courceslist[1] and commonStu[i][1]==courceslist[0]:
            return commonStu[i][2]
    return 0

def fitness(chromosom):
    slotslist=[]
    fitnessVal=0
    courcesList=[]

    # checking if all cources are in chromosom
    for i in range(N):
        courcesList.append(cources[i][0])
    for i in range(N):
        if chromosom[i][0] not in courcesList:
            return 10000

    for i in range(N):
     val=str(chromosom[i][1]) + str(chromosom[i][2])
     if val not in slotslist: 
         slotslist.append(val)
     else:
         return 10000  # checking no 2 cources have same time and same hall  
    
    #checking for hours 
    for i in range(N):
        for j in range(N):
            if chromosom[i][0]==cources[j][0]: 
                # print("ending hour of "+cources[j][0]+" %d "%(int(chromosom[i][1])+int(cources[j][1])))
                if int(chromosom[i][1])+int(cources[j][1])>T: # checking if the cource exceeds the max time of hall 
                    fitnessVal+=(10*((int(chromosom[i][1])+int(cources[j][1]))-T))


    #checking for clashes students 
    times=[chromosom[0][1]]
   
    for i in range(1,N):
        if chromosom[i][1] not in times:
            times.append(chromosom[i][1]) 
           
        else:
             courcesList=getFromTime(chromosom,chromosom[i][1])
            #  print(courcesList)
             count= getStudentClashesCount(courcesList)
            #  print("count: %d "%count)
             fitnessVal+=count*100

    #checking for overlaping slots
    

    return fitnessVal

fitnessVals=[]
for i in range(100):
    fitnessVals.append(fitness(chromosoms[i]))
    print("fitness %d "%i + ": %d" %fitness(chromosoms[i]))

nextPop=[]
def crossover():
    
    cutPoint=N/2
    print("Cutpoint----%d"%cutPoint)
    for i in range(99):
        if i%8!=0 :
            continue 
        parent1=chromosoms[i]
        parent2=chromosoms[i+1]
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
        nextPop.append(child1)
        nextPop.append(child2)
    print("-------NEXT POP----------")
    # print(nextPop)
 
crossover()
for i in range(len(nextPop)):
    print(nextPop[i])
    print(fitness(nextPop[i]))

