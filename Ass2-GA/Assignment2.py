


import random
num_courses = int(input("Enter the number of courses: "))
courses = []
for i in range(num_courses):
    course_name = input(f"Enter the name of course {i+1}: ")
    course_time =int(1)
    courses.append((course_name, course_time))

num_slots = int(input("Enter the number of exam slots: "))
Slots = []
for i in range(num_slots):
    slot = input(f"Enter time slot: ")
    slot_time =int(1)
    Slots.append((slot,slot_time))

num_halls = int(input("Enter the number of exam halls: "))
halls = []
for i in range(num_halls):
    hall_name = input(f"Enter the name of exam hall {i+1}: ")
    halls.append((hall_name))

max_time = int(input(f"Enter the maximum available time for Halls:"))
print('Courses:')
print(courses)
print("Time Slotes for each exam: ") 
print(Slots)
print("Halls: ")  
print(halls)
print("Maximum time of Hall availibilty is:")
print(max_time)

exams=[]
overlapping=[]
for i in range(len(courses)):
    for j in range(i+1, len(courses)):
        course1= courses[i][0]
        course2 = courses[j][0]
        common_students = int(input(f"Enter the number of overlapping students between {course1} and {course2}: "))
        overlapping.append((course1, course2, common_students))
print("Overlapping number of students in different pairs of courses:")
print(overlapping)

#----------GENERATING RANDOM POPULTATION----------
print("Population:")
population=[]
def generatePop():
    for course in courses:
        h=random.choice(halls)
        t=random.choice(Slots)
        population.append((course[0],t[0],h))
for i in range(5):
    generatePop()

print(population)
#-------------------------------------------------

solution=[]
for course in courses:
     h=random.choice(halls)
     t=random.choice(Slots)
     solution.append((course,h,t))

print("Solution:")
for s in solution:
    print(f"{s[0][0]}: {s[2][0]} in {s[1]}")

def calculate_fitness(solution,overlapping,max_time):
    penalty = 0
    occupied_halls = {}
    for slot in Slots:
        occupied_halls[slot[0]] = set()
    print(occupied_halls)
    for exam in solution:
        course=exam[0][0]
        hall=exam[1]
        time_slot=exam[2][0]
        if hall in occupied_halls[time_slot]:
            penalty += 10
        else:
            occupied_halls[time_slot].add(hall)

    common_students = {}
    for slot in Slots:
        common_students[slot[0]] = set()
    for overlap in overlapping:
        course1 = overlap[0]
        course2 = overlap[1]
        common = overlap[2]
        for exam1 in solution:
            if exam1[0][0] == course1:
                for exam2 in solution:
                    if exam2[0][0] == course2 and exam1[2][0] == exam2[2][0]:
                        common_students[exam1[2][0]].add((course1, course2, common))
                        break
    for exam in solution:
        hall = exam[1]
        time_slot = exam[2]
        hall_time = 0
        for exam2 in solution:
            if exam2[1] == hall and exam2[2] == time_slot:
                hall_time += exam2[0][1]
        if hall_time > max_time:
            penalty += 10 * (hall_time - max_time)
    for slot in Slots:
        students = set()
        for exam in solution:
            if exam[2][0] == slot[0]:
                course = exam[0]
                for overlap in overlapping:
                    if overlap[0] == course or overlap[1] == course:
                        students.update({overlap[0], overlap[1]})
        if len(students) > len(set(students)):
            penalty += 100
    
    return  (penalty)

fitness=calculate_fitness(population[0],overlapping,max_time)
print(fitness)