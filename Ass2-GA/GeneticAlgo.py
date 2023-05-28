# HARRIS AAMIR 
# 20i0943 SE-S 
import random
import time
start_time = time.time()
N=0                     #number of courses
K=0                     #number of exam halls
T=0                     #number of slots
totalHallTime= 0        #total time for hall
PopultaionSize=100      #size of population
courses=[]              #list of all courses with respect to index
courses_duration=[]     #list of all courses time with respect to index
halls=[]                #list of all halls (1,2,3..)
timeSlots=[]            #list of all timeSlots (1,2,3...)
population=[]           #list of all possible solutions
commonStu=[]            #list tuples containing (course, course, studentNum)
index_fitness=[]        #list that contains indexs and fitness values of population 

#-----INPUT-------
print("\n=========ASSIGNMENT 2==========")
N=int(input("\n>Enter the number of course (N): "))

for i in range(N):
    courses.append(input(">>Enter name of course #"+str((i+1))+": "))
    courses_duration.append(int(input(">>>Enter duration for this course exam (hours): ")))

K=int(input("\n>Enter the number of exam halls (K): "))
totalHallTime= int(input(">>Enter the total time avalible for halls (hours): "))

T=int(input("\n>Enter the number of slots avaliable in each hall: "))

print("\n")
for i in range(K):
    halls.append(str(i))
for i in range(T):
    timeSlots.append(str(i))
for i in  range(N):
    for j in range(i+1, N):
        commonStu.append((courses[i], courses[j], int(input(">Enter the number of common students in "+courses[i]+" and "+courses[j]+": "))))
if K*T<N: #number of courses are less then the avaliable slots
    print("----------------------------------------------------------") 
    print("|  Solution not possible as slots are less then courses  |")
    print("----------------------------------------------------------") 
    exit()
#------GENERATING RANDOM POPULATION------
def genPopulation():
    for i in range(PopultaionSize):
        chromosom=[]
        coursesCopy=courses[:]
        for i in range(N):
            c = random.choice(coursesCopy)
            coursesCopy.remove(c)
            t=0
            k=0
            t= random.choice(timeSlots)
            k= random.choice(halls)
            values=(c,t,k)
            chromosom.append(values)
        population.append(chromosom)    

#-------CONSTRAINTS CHECK---------

def getFromTime(chromosom, time): # returns the list of courses on same time
    courseslist=[]
    for i in range(N):
       if chromosom[i][1]==time:
           courseslist.append(chromosom[i][0])
    return courseslist

def getStudentClashesCount(courseslist): #returns the count of students with clashes between the courses of courselist
    for i in range(len(commonStu)):
        if commonStu[i][0]==courseslist[0] and commonStu[i][1]==courseslist[1]:
            return commonStu[i][2]
        elif commonStu[i][0]==courseslist[1] and commonStu[i][1]==courseslist[0]:
            return commonStu[i][2]
    return 0
def getcourseTime(course):
    for i in range(len(courses)):
        if courses[i]==course:
            return courses_duration[i]
    return -1

#-----FITNESS FUNCTION-----------
def fitness(chromosom):
    slotslist=[] #contains all possible slots of halls
    coursesList=[] # saves all courses in the chromosoms
    fitnessVal=0 
    for i in range(N):
        coursesList.append(chromosom[i][0])
    
    for i in range(N):
        if courses[i] not in coursesList:
            return 4000 #chromosom have reperting course

    if len(chromosom)!=N:
        return 4000 # shows that chromosome is missing a course 
    
    #checking for clashes of slots (2 courses have same time and same location )
    for i in range(N):
     val=str(chromosom[i][1]) + str(chromosom[i][2])
     if val not in slotslist: 
         slotslist.append(val)
     else:
         return 1000  # checking no 2 courses have same time and same hall  
    
    for hall in halls:
        halltime=0
        for sol in chromosom:
            if sol[2] == hall:
                halltime+=int(getcourseTime(sol[0]))
        if halltime>totalHallTime:
            fitnessVal+=10*(halltime-totalHallTime)

    #checking for clashes students 
    times=[chromosom[0][1]]
    for i in range(1,N):
        if chromosom[i][1] not in times:
            times.append(chromosom[i][1]) 
        else:
            coursesList=getFromTime(chromosom,chromosom[i][1])
            count= getStudentClashesCount(coursesList)
            fitnessVal+=count*100 # for every clashed student, 100 point are added

    return fitnessVal


#-----CROSSOVER FUNCTION------
def crossover(population):
    cutPoint=N/2
    for i in range(0,len(population)-1,8):
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
    for i in range(0,len(population)-1,10):
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

#----CREATES A NEW GENERATION -----
def nextGen():
  #new population contains 10% old 80% crossover and 10% mutation
  crossoverPop=evaluate(crossover(population),int(PopultaionSize*0.8))
  mutationPop=evaluate(mutation(population),int(PopultaionSize*0.1))
  Pop=[]
  index_fitness.sort(key=takeFitness)
  for i in range(int(PopultaionSize*0.1)):
      Pop.insert(0,population[index_fitness[i][0]])
  for i in range(int(PopultaionSize*0.8)):
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
        for j in range(PopultaionSize):
            index_fitness.append([j,fitness(nextgen[j])])
        index_fitness.sort(key=takeFitness)
        population=nextgen
    print("Total Generations: 100")
    print("\n************ FINAL ****************")
    print("------SOLUTION---------")
    for i in population[index_fitness[0][0]]:   
        print(f"-> Place Course: {(i[0])} in Hall#{1+int(i[2])} at timeslot {1+int(i[1])}")

    print("--------FITNESS----------")
    print("\t"+str(index_fitness[0][1]))
    print("************************************")
    
main()

print("---Running Time: %s seconds-----" % (time.time() - start_time))