#UC_Tours.py
#Noah Brackenbury, Winter 2016
#adapted and reworked from Will Brackenbury
#uses gale-shapley twice, with scanning for improvement in round 2 of matching

from random import shuffle
import sys
import os

CONST_TOURS = 2

class Person(object):

	def __init__(self, name, prefs):
	
		self.name = name # str name of person
		self.prefs = prefs # list populated with preffered tour ids
		self.tours = [0 for i in range(CONST_TOURS)] # list with tour identities
		self.proposalIndex = 0 # int for use in Gale Shapley
		self.firstTourPref = -1 # int mark where on pref list their first tour was
		self.secondTourPref = -1 # int mark where on pref list their second tour was
		
	def add_tour(self, tourName, sess, prefInt):
		self.tours[sess-1] = tourName  # sess-1 because python numbering starts at 0
		self.proposalIndex = 0
		if sess == 1:
			self.firstTourPref = prefInt
		if sess == 2:
			self.secondTourPref = prefInt

	def remove_tour(self, slot):
		self.tours[slot] = 0

	def get_pref(self): # function returns current locaiton on pref list and increments
		goal = self.prefs[self.proposalIndex]
		self.proposalIndex += 1
		return goal
	
	def __str__(self): # function returns string with person and tours
		ret = self.name + ", "
		for i in range(len(self.tours)):
			if self.tours[i] == 0:
				ret += "(Unfilled), "
			else:
				ret += self.tours[i] + ", "
				if i == 0:
					ret += str(self.firstTourPref + 1) + ", "
				else:
					ret += str(self.secondTourPref + 1) + ", "
		ret = ret[:-2]
		return ret


class Tour(object):

	def __init__(self, ident, maxCapacity): 
	
		self.maxCapacity = maxCapacity # int of capacity for tour
		self.id = ident  # str name of tour
		self.currentCapacity = [[0 for i in range(self.maxCapacity)], 
														[0 for i in range(self.maxCapacity)]]
														# 0 designates open slots to be filled with names
		
	def full(self, sess):
		full = True
		sess = sess-1 # sess-1 because python numbering starts at 0
		for i in range(len(self.currentCapacity[sess])):
			if self.currentCapacity[sess][i] == 0:
				full = False
		return full
			
	def slots(self, sess):
		# note: sess here is kept the same because it has already been decremented in
		# add_person, where this function is always called from, so the correct and
		# pythonized version of the variable is passed in
		ret = self.maxCapacity
		for i in range(len(self.currentCapacity[sess])):
			if self.currentCapacity[sess][i] != 0:
				ret -= 1
		return ret		 

	def add_person(self, name, sess):
		sess = sess-1 # sess-1 because python numbering starts at 0
		slot = self.maxCapacity - self.slots(sess)
		self.currentCapacity[sess][slot] = name

	def remove_person(self, name, sess):
		successful = False
		sess = sess-1 # sess-1 because python numbering starts at 0
		for k in range(len(self.currentCapacity[sess])):
			if self.currentCapacity[sess][k] == name:
				self.currentCapacity[sess][k] = 0
				for j in range(k,len(self.currentCapacity[sess])-1):
					self.currentCapacity[sess][j] = self.currentCapacity[sess][j+1]
				self.currentCapacity[sess][self.maxCapacity-1] = 0
				successful = True

	def __str__(self, sess):
		sess = sess-1 # sess-1 because python numbering starts at 0
		ret = self.id + ", "
		for i in range(self.maxCapacity):
			ret += str(self.currentCapacity[sess][i]) + ", "
		ret = ret[:-2]
		if self.maxCapacity == 0:
			ret += ": None"
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
		initTour = linesTourFile[i].split(",") # these are strings
		initTour = Tour(initTour[0], int(initTour[1]))
		Tours.append(initTour)
		
	#Person's name, preference1, preference2, preference3...
	#Initialize the list of people
	initPeople = []
	for i in range(len(linesPplFile)):
		initPerson = linesPplFile[i].split(",") # these are strings
		initPerson = Person(initPerson[0], initPerson[1:])
		initPeople.append(initPerson)
	
	People = initPeople

	# first tour
	for i in range(len(Tours)):
		for j in range(len(People)): # the runtime on this is atrocious but it works
			if People[j].firstTourPref == -1: # move on if already been assigned a tour
				pref = People[j].get_pref()
				targetTour = None
				for k in range(len(Tours)):
					if Tours[k].id == pref:
						targetTour = Tours[k]
				if targetTour == None:
					print("Error: " + People[j].name + " requested a non-existant tour")
					quit()
				if targetTour.full(1) == False:
					People[j].add_tour(targetTour.id, 1, People[j].proposalIndex-1)
					targetTour.add_person(People[j].name, 1)
					for k in range(len(Tours)):
						if Tours[k].id == pref:
							Tours[k] = targetTour

	People.sort(key=lambda x: x.firstTourPref, reverse=True) 
	# sort list by first tour pref for fairness

	# second tour, the more complicated part
	for i in range(len(Tours)):
		for j in range(len(People)): # the runtime on this is atrocious but it works
			if People[j].secondTourPref == -1: # move on if already assigned 2 tours
				if People[j].proposalIndex >= len(Tours): 
				# this is for if the only tour left open is their first tour
					People[j].proposalIndex = 0
					if People[j].firstTourPref == 0:
						for k in range(len(Tours)):
							if Tours[k].id == People[j].prefs[1]:
								Tours[k].maxCapacity += 1
								Tours[k].currentCapacity[1].append(0)
								Tours[k].currentCapacity[0].append(0)
					else:
						for k in range(len(Tours)):
							if Tours[k].id == People[j].prefs[0]:
								if Tours[k].maxCapacity == 0:
									for k in range(len(Tours)):
										if Tours[k].id == People[j].prefs[1]:
											Tours[k].maxCapacity += 1
											Tours[k].currentCapacity[1].append(0)
											Tours[k].currentCapacity[0].append(0)
								else:
									Tours[k].maxCapacity += 1
									Tours[k].currentCapacity[1].append(0)
									Tours[k].currentCapacity[0].append(0)
				pref = People[j].get_pref()
				if pref == People[j].tours[0]:
					pref = People[j].get_pref()
				targetTour = None
				for k in range(len(Tours)):
					if Tours[k].id == pref:
						targetTour = Tours[k]
				if targetTour == None:
					print("Error: " + People[j].name + " requested a non-existant tour")
					quit()
				if targetTour.full(2) == False:
					People[j].add_tour(targetTour.id, 2, People[j].proposalIndex-1)
					targetTour.add_person(People[j].name, 2)
					for k in range(len(Tours)):
						if Tours[k].id == pref:
							Tours[k] = targetTour
				else:
					for n in range(People[j].proposalIndex-1):
						nPref = People[j].prefs[n];
						nTargetTour = None
						for k in range(len(Tours)):
							if Tours[k].id == nPref:
								nTargetTour = Tours[k]
						if nTargetTour == None:
							print("Error: nTargetTour is a non-existant tour")
							quit()
						if targetTour.full(1) == False:
							if nTargetTour.full(2) == False:
								People[j].remove_tour(0)
								nTargetTour.remove_person(People[j].name, 1)
								People[j].add_tour(targetTour.id, 1, People[j].proposalIndex-1)
								targetTour.add_person(People[j].name, 1)
								People[j].add_tour(nTargetTour.id, 2, n)
								nTargetTour.add_person(People[j].name, 2)

		#Output file
	outFile = open("output.csv", "w")
	toWrite = ""

	for i in range(len(People)): # write each person's tours and where they were on pref
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
	print("See output.csv")

main()