#UCtours18.py
#Noah Brackenbury, Winter 2018
#adapted and reworked from last year's UC_Tours.py
#sorts grad students into tours by desirability of tours and sortability of students

from random import shuffle
import sys
import os

CONST_TOURS = 2

class Person(object):

    def __init__(self, name, prefs):
    
        self.name = name # str name of person
        self.prefs = prefs # list populated with preffered tour ids
        self.tours = [0 for i in range(CONST_TOURS)] # list with tour names
        self.unsortability = 0 # metric for how easy it is to sort this person into their preffered tours
        self.full = 0
        
    def add_tour(self, tourName, sess):
        self.tours[sess-1] = tourName  # sess-1 because python numbering starts at 0
        if self.tours[0] != 0 and self.tours[1] != 0:
            self.full = 1

    def remove_tour(self, slot):
        self.tours[slot] = 0
        
    def get_pref(self):
        if self.prefs != []:
            return self.prefs.pop(0)
        else:
            return False
    
    def __str__(self): # function returns string with person and tours
        ret = self.name + ", "
        for i in range(len(self.tours)):
            if self.tours[i] == 0:
                ret += "(Unfilled), "
            else:
                ret += self.tours[i] + ", "
        ret = ret[:-2]
        return ret


class Tour(object):

    def __init__(self, ident, desirability, capacity1, capacity2): 
    
        self.capacity = [int(capacity1), int(capacity2)] # int of capacity for tour
        self.name = ident  # str name of tour
        self.desirability = desirability # interest in tour / capacity
        self.currentCapacity = [[0 for i in range(self.capacity[0])], 
                                [0 for i in range(self.capacity[1])]]
        # 0 designates open slots to be filled with names
        # self.imcompatible = incompatible
        
    def full(self, sess):
        full = True
        sess = sess-1 # sess-1 because python numbering starts at 0
        for i in range(len(self.currentCapacity[sess])):
            if self.currentCapacity[sess]:
                if self.currentCapacity[sess][i] == 0:
                    full = False
        return full
            
    def slots(self, sess):
        # note: sess here is kept the same because it has already been decremented in
        # add_person, where this function is always called from, so the correct and
        # pythonized version of the variable is passed in
        ret = self.capacity[sess]
        for i in range(len(self.currentCapacity[sess])):
            if self.currentCapacity[sess]:
                if self.currentCapacity[sess][i] != 0:
                    ret -= 1
        return ret         

    def add_person(self, name, sess):
        sess = sess-1 # sess-1 because python numbering starts at 0
        slot = self.capacity[sess] - self.slots(sess)
        self.currentCapacity[sess][slot] = name

    def __str__(self, sess):
        sess = sess-1 # sess-1 because python numbering starts at 0
        ret = self.name + ", "
        for i in range(self.capacity[sess]):
            ret += str(self.currentCapacity[sess][i]) + ", "
        ret = ret[:-2]
        if self.capacity[sess] == 0:
            ret += ": None"
        return ret 


def main():

    maxPrefs = 0

    #Open the file of people, read it into several lines
    pplFile = open("People.csv", "r")
    pplOrigFile = pplFile.read()
    linesPplFile = pplOrigFile.splitlines()
    pplFile.close()
    
    #Open the file of tours, read it into several lines
    tourFile = open("Tours.csv", "r")
    tourOrigFile = tourFile.read()
    linesTourFile = tourOrigFile.splitlines()
    tourFile.close()

    #Tourname, capacity1, capacity2, capacity3...
    #Initialize the list of tours
    Tours = []
    for i in range(len(linesTourFile)):
        initTour = linesTourFile[i].split(",") # these are strings
        initTour = Tour(initTour[0], float(initTour[1]), initTour[2], initTour[3])
        Tours.append(initTour)
        
    #Person's name, preference1, preference2, preference3...
    #Initialize the list of people
    People = []
    for i in range(len(linesPplFile)):
        initPerson = linesPplFile[i].split(",") # these are strings
        if len(initPerson[1:]) > maxPrefs:
            maxPrefs = len(initPerson[1:]) # update the maximum number of prefs ingested
        initPerson = Person(initPerson[0], initPerson[1:])
        People.append(initPerson)
    
    #Initialize unsortability
    for persons in People:
        unsortability = 0
        for index, tour in enumerate(Tours):
            if tour.name in persons.prefs:
                unsortability += Tours[index].desirability / len(persons.prefs)
        persons.unsortability = unsortability
    People.sort(key=lambda x: x.unsortability, reverse=True)
        
    
    # add people to tours
    for x in range(maxPrefs+2):
        for persons in People:
            if persons.full == 0:
                pref = persons.get_pref()
                if pref == False:
                    for k in range(len(Tours)):
                        if Tours[k].full(1) == False and persons.tours[0] == 0:
                            persons.add_tour(Tours[k].name, 1)
                            Tours[k].add_person(persons.name, 1)
                        elif Tours[k].full(2) == False and persons.tours[1] == 0:
                            persons.add_tour(Tours[k].name, 2)
                            Tours[k].add_person(persons.name, 2)
                    # here you could add some spillover feature
                else:
                    targetTour = None
                    for k in range(len(Tours)):
                        if Tours[k].name == pref:
                            targetTour = Tours[k]
                    if targetTour == None:
                        print("Error: " + persons.name + " requested a non-existant tour, " + pref)
                        quit()
                    if targetTour.full(1) == False and persons.tours[0] == 0:
                        persons.add_tour(targetTour.name, 1)
                        targetTour.add_person(persons.name, 1)
                    elif targetTour.full(2) == False and persons.tours[1] == 0:
                        persons.add_tour(targetTour.name, 2)
                        targetTour.add_person(persons.name, 2)

    #Output file
    outFile = open("2018output.csv", "w")
    toWrite = ""

    for i in range(len(People)): # write each person's tours
        toWrite += People[i].__str__()
        toWrite += "\n"
        
    toWrite += "\nSession 1:\n"
    for i in range(len(Tours)): # write people in session 1 of tours
        toWrite += Tours[i].__str__(1)
        toWrite += "\n"
        
    toWrite += "\nSession 2:\n"
    for i in range(len(Tours)): # write people in session 2 of tours
        toWrite += Tours[i].__str__(2)
        toWrite += "\n"
    
    outFile.write(toWrite)
    outFile.close()
    print("See 2018output.csv")
    
main()
