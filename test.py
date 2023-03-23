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



def getcourceDuration(courceName):
    for i in range(len(cources)):
        if courceName==cources[i][0]:
            return cources[i][1]
    
    return -1
    
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



def checkOverlaps(chromosom):
    hallsList=[]
    for i in range(K):
        list=[]
        for j in range(T):
         list.append("_")
        hallsList.append(list)
    
    for i in range(N):
        val=0
        duration=int(getcourceDuration(chromosom[i][0]))
        starting= int(chromosom[i][1])
        hallNum= int(chromosom[i][2])
        time=int(starting)
        ending=starting+duration
        if ending>T:
            ending=T
        while time<ending:
            if hallsList[hallNum][time]=="_":
                hallsList[hallNum][time]=chromosom[i][0]
            else: 
                val+=50 #starting point already booked 
            time+=1

    return val



def fitness(chromosom):
    slotslist=[]
    fitnessVal=0

    courcesList=[]
   
    for i in range(N):
        courcesList.append(cources[i][0])
    # checking if all cources are not in chromosom

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
                    fitnessVal+=(10*((int(chromosom[i][1])+int(cources[j][1]))-T)) # for every hour exceeding max time, 10 points are added


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
             fitnessVal+=count*100 # for every clashed student, 100 point are added

    #checking for overlaping slots
    fitnessVal+=checkOverlaps(chromosom) # for every overlaping hour, 50 points are added 
    
    return fitnessVal

fitnessVals=[]
for i in range(100):
    # fitnessVals.append(fitness(chromosoms[i]))
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
 
# crossover()
# for i in range(len(nextPop)):
#     print(nextPop[i])
#     print(fitness(nextPop[i]))

newPop=[]
def mutation():
    for i in range(0,len(chromosoms)-1, int(0.1*len(chromosoms))):
        print("i in mutaion: %d"%i)
        index=random.randint(0, N-1)
        chromosom1=chromosoms[i][:]
        chromosom2=chromosoms[i+1][:]
        temp=chromosom1[index]
        chromosom1[index]=chromosom2[index]
        chromosom2[index]=temp
        newPop.append(chromosom1)
        newPop.append(chromosom2)

# mutation()

# for i in range(len(newPop)):
#    print(newPop[i])
#    print(fitness(newPop[i]))
#    print(i)


for i in range(100):
   print("%d"%i )
   print(chromosoms[i])
   print("fitness %d "%i + ": %d" %fitness(chromosoms[i]))
