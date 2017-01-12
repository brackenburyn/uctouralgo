#UC_Tour_Algorithm.py

from random import shuffle
import sys
import os

CONST_TOURS = 2

class Person(object):

	def __init__(self, name, prefs):
	
		self._name = name
		self._prefs = prefs # Populated with tour identities
		self._curr_pref = 0
		self.sat = 0 #short for satisfaction
		self.tours = [None for i in range(CONST_TOURS)] # Populated with tour identities
		#for i in range(len(self._prefs)):
			#self._prefs[i] = int(self._prefs[i])
		
	def add_tour(self, tourName, slot):
		self.tours[slot] = tourName
	
	def inc_pref(self):
		self._curr_pref += 1
	
	def inc_sat(self):
		self.sat += (1 + CONST_TOURS - (self._curr_pref)) ** 1.5 
		self.inc_pref()
	
	def avail(self):
		avail = []
		for i in range(len(self.tours)):
			if self.tours[i] == None:
				avail.append(i)
		return avail
	
	def __str__(self):
		ret = self._name + ", "
		for i in range(len(self.tours)):
			if self.tours[i] == None:
				ret += "(Unfilled), "
			else:
				ret += self.tours[i] + ", "
		ret = ret[:-2]
		return ret


class Tour(object):

	def __init__(self, ident, maxCapacity): #MaxCapacity should be a list of the capacity for each tour, for cancelled sessions 0 = full
	
		self._maxCapacity = maxCapacity #List of capacities for each tour, of len(CONST_TOURS)
		self._id = ident
		self.currentCapacity = [0 for i in range(len(self._maxCapacity))]
		for i in range(len(self._maxCapacity)):
			self._maxCapacity[i] = int(self._maxCapacity[i])
		for i in range(len(self.currentCapacity)):
			self.currentCapacity[i] = self._maxCapacity[i]
		
	def full(self):
		full = True
		for i in range(len(self.currentCapacity)):
			if self.currentCapacity[i] != 0:
				full = False
		return full
			
	def slots(self):
		ret = []
		for i in range(len(self.currentCapacity)):
			if self.currentCapacity[i] != 0:
				ret.append(i)
		return ret		 

	def __str__(self):
		ret = self._id + ": "
		for i in range(CONST_TOURS):
			ret += str(self.currentCapacity[i]) + ", "
		ret = ret[:-2]
		return ret 

def multLSort(twoList):
	for i in range(len(twoList)):
		twoList[i] = sorted(twoList[i], key = lambda People : People.sat) 


def findTour(theMatrix, tour_id, slot):
	passed = slot
	for i in range(len(theMatrix)):
		if theMatrix[i][0] == tour_id:
			if passed == 0:
				return i
			else:
				passed -= 1
	return -1

def share(l1, l2):
	ret = []
	for i in range(len(l1)):
		for j in range(len(l2)):
			if l1[i] == l2[j]:
				ret.append(l1[i])
	return ret


def main():

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
		initTour = linesTourFile[i].split(",")      #Impt to note that the lines that are being split are still in text format
		initTour = Tour(initTour[0], initTour[1:])
		Tours.append(initTour)
		
	#Person's name, preference1, preference2, preference3...
	
	#Initialize the list of people
	initPeople = []
	for i in range(len(linesPplFile)):
		initPerson = linesPplFile[i].split(",")      #Impt to note that the lines that are being split are still in text format
		initPerson = Person(initPerson[0], initPerson[1:])
		initPeople.append(initPerson)
	
	shuffle(initPeople)
	People = initPeople
	
	roundList = [People] + [[] for i in range(CONST_TOURS)]
	finalPeople = []
	
	
	#satfisfied = True
	#for i in range(len(roundList)):
	#for j in range(CONST_TOURS):
	#if (roundList[i]._prefs[j] == None):

	satisfied = False
				
	currRound = 0

	while not satisfied:
	
		#If the current round is empty, select the next round
		if len(roundList[currRound]) == 0:
			currRound += 1
		
		if (currRound == CONST_TOURS):
			#Randomly place them into groups
			for i in range(len(Tours)): #This can either end with the tours 
			#running out of slots, the people are full up on tours, or the availability 
			#of tours and the people don't match up
				seen = 0  #this is designed to protect against the edge case in which a 
				#tour isn't full, but because of strange scheduling, no one has 
				#availability for it. Hopefully a swap chain would fix this up, but 
				#for the moment, this is sufficient
				while not (Tours[i].full()): 
					if len(roundList[currRound]) == 0:
						break
					currPerson = roundList[currRound].pop(0)
					
					possibleSlots = share(Tours[i].slots(), currPerson.avail())
					if len(possibleSlots) > 0:
						currPerson.add_tour(Tours[i]._id, possibleSlots[0])
						currPerson.inc_sat()
						Tours[i].currentCapacity[possibleSlots[0]] -= 1					
						roundList[currRound].append(currPerson)
					else:
						if (currPerson.avail() == []):	
							finalPeople.append(currPerson)
						else:
							seen += 1
							if seen == len(roundList[currRound]): 
								break
							else:
								roundList[currRound].append(currPerson)
				
						
			for i in range(len(roundList[currRound])):
				finalPeople.append(roundList[currRound][i])
						
			satisfied = True
			continue	
			
		#Given that we're in a main round, pop the person out of the list
		
		currPerson = roundList[currRound].pop(0)
		
		#Find the target tour of that person's preference
		targetTour = None
		for i in range(len(Tours)):
			if Tours[i]._id == currPerson._prefs[currPerson._curr_pref]:
				targetTour = Tours[i]
		
		possibleSlots = share(targetTour.slots(), currPerson.avail())
		if len(possibleSlots) > 0:
			currPerson.add_tour(targetTour._id, possibleSlots[0])
			currPerson.inc_sat()
			targetTour.currentCapacity[possibleSlots[0]] -= 1
			roundList[currRound + 1].append(currPerson)
			multLSort(roundList)
		else:
			#if targetTour.full():
			currPerson.inc_pref()
			roundList[currRound + 1].append(currPerson)
			multLSort(roundList)
	
	#Output file
	outFile = open("output.csv", "w")
	
	matrix = []
	for i in range(len(Tours)):
		for j in range(len(Tours[i]._maxCapacity)):
			matrix.append([Tours[i]._id])
				
	for i in range(len(finalPeople)):
		for j in range(CONST_TOURS):
			index = findTour(matrix, finalPeople[i].tours[j], j)
			if index == -1:
				continue
			matrix[index].append(finalPeople[i]._name)
	
	#this will break if len(matrix) < 1
	
	
	maxLength = len(matrix[0])
	for i in range(len(matrix)):
		if len(matrix[i]) > maxLength:
			maxLength = len(matrix[i])
	
	toWrite = ""
	for i in range(maxLength):
		for j in range(len(matrix)):
			try:
				toWrite += matrix[j][i] + ", "
			except IndexError:
				toWrite += " , "
				
		toWrite += "\n"
	
	
	outFile.write(toWrite)
	outFile.close()

	
	
main()