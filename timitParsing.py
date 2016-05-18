import re
import os
SAM = 16000

stress={}

with open("/Users/elias/Desktop/IPhODv2/IPhOD2_Words.txt") as f2:
	lines = f2.readlines()
for l in lines:
	pattern = ""
	line= re.split("\\s", l)
	
		#found the right word
	stressString = line[3]
	regex = re.compile("[0-9]")
	for char in stressString:
		m = re.match(regex, char)
		if m is not None:
			pattern += char
	stress[line[1]]=pattern



def getStress(word):
	
	
	try:	
		if stress[word][0] == "1":
		#correct stress pattern
			return True
		else:
			return False
	except:
		return False

def getSPS(lines):
	maxIndex = 0
	line = ""
	count = 0
	
	#get syllables/second
	for i in range(len(lines)):		
		
		lArr = re.split("\\s", lines[i])
		if lArr[2] == "h#":				
			#this is the first -1, ignore it
			continue
		else:
			
			c = lArr[2].strip()	
			#check if it's a vowel				
			regex = re.compile("iy|ih|eh|ey|ae|aa|aw|ay|ah|ao|oy|ow|uh|uw|er|ax|ix|axr|ax-h", re.I) 
			m = re.match(regex, c)
			if m is not None:
				count +=1				
		line = lines[i]
	lArr = re.split("\\s", line)
	finalDur = int(lArr[1])
	finalDurSec = finalDur/SAM		
	SPS = count/finalDurSec
	return (SPS, count)

def getSylNum(lines, start, end):

	regex = re.compile("iy|ih|eh|ey|ae|aa|aw|ay|ah|ao|oy|ow|uh|uw|er|ax|ix|axr|ax-h", re.I) 
	count=0
	
	for line in lines:
		lArr = re.split("\\s", line)
	
		if int(lArr[0])>=int(start) and int(lArr[1])<= int(end):
		
			m = re.match(regex, lArr[2])
			if m is not None:

				count+=1
			else:
				continue
		else:
			continue
	return count

def getLastPhoneme(phnlines, wordEnd):
	last = ""
	for l in phnlines:
		line = re.split("\\s", l)

		if str(line[1])== str(wordEnd):
		
			last = line[2]
	return last

def getAge(SID):
	age = 0
	with open("/Users/elias/Desktop/timit/doc/spkrinfo.txt") as f4:
		lines = f4.readlines()
	for l in lines:
		line = re.split("\\s", l)
		if line[0].upper() == SID.upper():
			recdate = line[8].split("/")
			recyear = recdate[len(recdate)-1]
			birthdate = line[10].split("/")
			birthyear = birthdate[len(birthdate)-1]
		#	print(line[8])
			try:
				age = int(recyear)-int(birthyear)
			except Exception:
				age = 0
	return age

def getInfo(wordStuff, startLine, nextLine, vowelLine, phnlines, line, rootname, index, didSkip, prevWord, last, closure):
	
	prevWordType = "Content"
	if wordStuff[4] and index == 1:
		prevWordType = "Function"


	fileArr = rootname.split("/")
	filename = fileArr[len(fileArr)-1]
	dialectNum = fileArr[len(fileArr)-3][2]
	dialectRegion = ""

	if int(dialectNum) == 1:
		dialectRegion = "New England"
	elif int(dialectNum) == 2:
		dialectRegion = "Northern"
	elif int(dialectNum) == 3:
		dialectRegion = "Northern Midland"
	elif int(dialectNum) == 4:
		dialectRegion = "South Midland"
	elif int(dialectNum) == 5:
		dialectRegion = "Southern"
	elif int(dialectNum) == 6:
		dialectRegion = "New York City"
	elif int(dialectNum) == 7:
		dialectRegion = "Western"
	elif int(dialectNum) == 8:
		dialectRegion = "Army Brat"
	speakInfo = fileArr[len(fileArr)-2]
	sex = speakInfo[0].upper()
	SID = speakInfo[1:len(speakInfo)]

	age = getAge(SID)
	recordingSite = "TexasInstruments"
	position = "Second"
	if index == 0:
		position = "Initial"

	word = wordStuff[0]
	wordStart = wordStuff[1]
	wordEnd = wordStuff[2]
	wrdlines = wordStuff[3]
	#we have word start and stop times
	#check if next letter is vowel
	"""
	regex = re.compile("iy|ih|eh|ey|ae|aa|aw|ay|ah|ao|oy|ow|uh|uw|er|ax|ix|axr|ax-h", re.I) 
	m = re.match(regex, vowelLine[2])
	if m is not None:
		print("in if")
	"""
	CClosure = ""
	CstartClosure = 0
	CendClosure = 0
	#found a stop plus a vowel
	if closure:
		CClosure = startLine[2]
		CstartClosure = int(startLine[0])/SAM
		CendClosure = int(startLine[1])/SAM

		C = nextLine[2]
	
		Cstart = int(nextLine[0])/SAM
		Cend = int(nextLine[1])/SAM
	else:
		C = startLine[2]
		Cstart = int(startLine[0])/SAM
		Cend = int(startLine[1])/SAM
	V = vowelLine[2]
	
	Vstart = int(vowelLine[0])/SAM
	Vend = int(vowelLine[1])/SAM
	syllables = getSPS(phnlines)
	sylCount = getSylNum(phnlines, line[0], line[1])
	toPrintAge = str(age)
	toPrintCStart = CstartClosure
	toPrintCEnd = CendClosure



	if age == 0:
		toPrintAge = ""


	if CClosure == "":
		toPrintCStart = ""
		toPrintCEnd = ""


			#C, Cstart, Cend, V, Vstart, Vend, word, wordStart, wordEnd, sylCount, syllables[0], len(wrdlines), filename, SID, recordingSite, position,prevWordType, prevWord, last, sex, int(age)

	return("%s,%s,%s,%s,%f,%f,%s,%f,%f,%s,%f,%f,%d,%f,%d,%s,%s,%s,%s,%s,%s,%s,%s,%s"%(CClosure, toPrintCStart, toPrintCEnd, C, Cstart, Cend, V, Vstart, Vend, word, wordStart, wordEnd, sylCount, syllables[0], len(wrdlines), filename, SID, position,prevWordType, prevWord, last, sex, toPrintAge,dialectRegion )) #include speaker info and previous word info

with open("/Users/elias/Desktop/CelexParsing/englishWords.txt") as f3:
		excludelines = f3.readlines()


def parseTimit(rootname):
	with open(rootname+".wrd") as f1:
		wrdlines= f1.readlines()
#	print("read word lines")
	with open(rootname+".phn") as f2:
		phnlines = f2.readlines()
#	print("read phone lines")
	
	x = 0 
	didSkip = False
	isStopVowel = False
	isStopVowel2 = False
	for i in range(len(wrdlines)):
		found = False
		isContentSecond = True
		line = re.split("\\s", wrdlines[i])
		wordLine1 = line
		word = line[2]
		word2 = ""
		try:
			line2 = re.split("\\s", wrdlines[i+1])
			wordLine2 = line2
			word2 = line2[2]
			wordStart2 = int(line2[0])/SAM
			wordEnd2 = int(line2[1])/SAM
		except:
		#	print("only one word")
			word2 = None

		wordStart = int(line[0])/SAM
		wordEnd = int(line[1])/SAM

	#	print("got both words")

		for line in excludelines:
				
			if word.strip() == line.strip(): #if it's one of the lines you don't want
				found = True #look at the next word
				break

		for line in excludelines:
				
			if word2.strip() == line.strip(): #if it's one of the lines you don't want
				isContentSecond = False #look at the next word
				break
		if found:
			didSkip = True
		break	
	#print("out of the for")

	
	
	line1 = re.split("\\s", wrdlines[i])
	startTime1 = line1[0]	
	endTime1 = line1[1]
	line2 = re.split("\\s", wrdlines[i+1])
	startTime2 = line2[0]
	endTime2 = line2[0]

	startLine = ""
	startLine2 = ""
	nextLine = ""
	nextLine2 = ""
	endLine = ""
	endLine2 = ""
	for i in range(len(phnlines)):
		phnline = re.split("\\s", phnlines[i])
		if int(phnline[0]) == int(startTime1):
			#first line of phon segments
			startLine = phnline
			nextLine = re.split("\\s", phnlines[i+1])
			thirdLine = re.split("\\s", phnlines[i+2])
		if int(phnline[1])<=int(endTime1):
			#last line of phon segments
			endLine=phnline
			continue
	

	for i in range(len(phnlines)):
		phnline = re.split("\\s", phnlines[i])

		if int(phnline[0]) == int(startTime2):
		
			#first line of phon segments
			startLine2 = phnline
			nextLine2 = re.split("\\s", phnlines[i+1])
			thirdLine2 = re.split("\\s", phnlines[i+2])
		if int(phnline[1])<=int(endTime2):
			#last line of phon segments
			endLine2=phnline
			continue

	stopRegex1 = re.compile("bcl|dcl|gcl|pcl|tcl|kcl|[ptkbdg]|dh", re.I)
	stopRegex2 = re.compile("[ptkbdg]|dh")
	vowelRegex = re.compile("iy|ih|eh|ey|ae|aa|aw|ay|ah|ao|oy|ow|uh|uw|er|ax|ix|axr|ax-h", re.I) 
	m = re.match(stopRegex1, startLine[2])
	m2 = re.match(stopRegex2, nextLine[2])
	closure = False
	closure2 = False
	if m is not None and m2 is None:
		m3 = re.match(vowelRegex, nextLine[2]) #check to see if it's a stop w no closure
		if m3 is not None:
	
			
			isStopVowel = True
			thirdLine= nextLine
	if m is not None and m2 is not None:
		m3 = re.match(vowelRegex, thirdLine[2])
		if m3 is not None:
		
			isStopVowel = True
			closure = True

	m = re.match(stopRegex1, startLine2[2])
	m2 = re.match(stopRegex2, nextLine2[2])

	if m is not None and m2 is None:
		m3 = re.match(vowelRegex, nextLine2[2]) #check to see if it's a stop w no closure
		if m3 is not None:
		
			
			isStopVowel2 = True
			thirdLine2= nextLine2 #make this the vowel line
	if m is not None and m2 is not None:
		m3 = re.match(vowelRegex, thirdLine2[2])
		if m3 is not None:
			
			isStopVowel2 = True
			closure2 = True


	
	#print("got first, last lines of phon segments")
	firstLine = None
	secondLine = None
	

	stress1=getStress(word)
	stress2=getStress(word2)
	
	
	if isStopVowel and not didSkip and stress1:

		wordStuff = (word, wordStart, wordEnd, wrdlines, didSkip)
		last = ""
							#wordStuff, startLine, nextLine, phnlines, line, rootname, index, didSkip, prevWord, last
		firstLine = getInfo(wordStuff, startLine, nextLine, thirdLine, phnlines, wordLine1, rootname, 0, False, last, last, closure)
		#print(firstLine)
	if isStopVowel2 and stress2 and isContentSecond:
		
		
		last = getLastPhoneme(phnlines, wordLine1[1])
		#print("last phoneme: " + last)
		wordStuff = (word2, wordStart2, wordEnd2, wrdlines, didSkip)

		
							#wordStuff, startLine, nextLine, phnlines, line, rootname, index, didSkip, prevWord, last phoneme, closure
	
		secondLine = getInfo(wordStuff, startLine2, nextLine2, thirdLine2, phnlines, wordLine2, rootname, 1, didSkip, word, last, closure2)
		#print(secondLine)
		
#parseTimit("/Users/elias/Desktop/timit/test/dr1/faks0/sx223")
	#print("done parsing")
	
	return(firstLine, secondLine)


with open("/Users/elias/Desktop/timitOutput.txt" , "w") as f3:
	#all the files in the directory
	fileRegex = ".*\.wrd"
	for directory in os.walk("/Users/elias/Desktop/timit", topdown=True):
		
		for filename in directory[2]:
			
			#make sure it ends in .wrd, .phn
			m = re.match(fileRegex, filename)
			if m is not None:
				filename = filename[0:len(filename)-4]
				toWrite = (None,None)
				#run the parseFile method
				#try:
				toWrite = parseTimit(directory[0]+"/" +filename)
				#except Exception:
					#print("no such file")
					
		
				if toWrite[0] is not None:
					#write to file
					f3.write(toWrite[0] + "\n")
				
				if toWrite[1] is not None:

					f3.write(toWrite[1] + "\n")
					


