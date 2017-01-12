#cleanse_tours.py

def main():
	
	file = open("input_Tours_Final.txt", "r")
	beenRead = file.read()
	file.close()
	lines = beenRead.split("\n")
	
	tourVec = lines[0].split("\t")
	toRead = ""
	for i in range(1, len(lines)):
		splitUp = lines[i].split("\t")
		cleansed = []
		for j in range(len(splitUp)):
			cleansed.append(splitUp[j])
		for j in range(1, len(splitUp)):
			if splitUp[j] == "":
				continue
			cleansed[int(splitUp[j])] = tourVec[j]
		
		for j in range(len(cleansed)):
			if cleansed[j] == "":
				continue
			toRead += cleansed[j] + ","
		toRead = toRead[:-2] + "\n"
	
	endFile = open("Tours_cleansed_output.csv", "w")
	endFile.write(toRead)
	endFile.close()
	
	
main()