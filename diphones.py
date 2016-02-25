import sys
import re

phones = ["<","b","t","^","j","H","x","d","*","r","z","s","$","S","D","T","Z","E","g","f","q","k","l","m","n","h","w","y","aa","uu0","ii0","a","u0","i0","AA","A","u1","i1","<<","bb","tt","^^","jj","HH","xx","dd","**","rr","zz","ss","$$","SS","DD","TT","ZZ","EE","gg","ff","qq","kk","ll","mm","nn","hh","ww","yy","sil"]

consonants = [
"r", "g", "y",
"b", "z", "f",
"t", "s", "q",
"$", "k", "<",
"j", "S", "l",
"H", "D", "m",
"x", "T", "n",
"d", "Z", "h",
"*", "E", "w", "^",
"<<", "rr", "gg",
"bb", "zz", "ff",
"tt", "ss", "qq",
"$$", "kk", "yy",
"jj", "SS", "ll",
"HH", "DD", "mm",
"xx", "TT", "nn",
"dd", "ZZ", "hh", 
"**", "EE", "ww", "^^"
]

emphaticConsonants = ["q", "qq", "x", "xx", "T", "TT", "D", "DD", "S", "SS", "Z", "ZZ", "g", "gg"
]
nonemphaticVowels = ["aa", "a"
]
backEmphaticConsonants = ["q", "qq", "T", "TT", "D", "DD", "S", "SS", "Z", "ZZ"
]

vowels = ["aa", "A",
"uu0",
"ii0",
"a", "u1", "AA",
"i0", "u0", "i1"
]
pause = ["sil", "sp"
]
phones = consonants + vowels#+ ["", "-", "DIST", "Dist", "dist"]
allSymbols = phones + pause
stopsVoiced = ["b", "d", "D", "G", "J",
"bb", "dd", "DD", "GG", "JJ"
]
stopsVoiceless = ["p", "t", "T", "<", "k", "q", "<",
"pp", "tt", "TT", "<<", "kk", "qq", "<<"
]
stops = stopsVoiced + stopsVoiceless
fricVoiced = ["v", "*", "z", "Z", "j", "g", "E",
"vv", "**", "zz", "ZZ", "jj", "gg", "EE"
]
fricVoiceless = ["f", "S", "s", "^", "$", "x", "H", "h",
"ff", "SS", "ss", "^^", "$$", "xx", "HH", "hh"
]
fric = fricVoiced + fricVoiceless
nasals = ["m", "n",
"mm", "nn"
]
trill = ["r",
"rr"
]
approx = ["w", "y", "l",
"ww", "yy", "ll"
]

types = {"phones": phones, "consonants" : consonants, "vowels": vowels, "stops": stops, "stopsVoiced": stopsVoiced, "stopsVoiceless": stopsVoiceless, "fric": fric, "fricVoiced": fricVoiced, "fricVoiceless": fricVoiceless, "nasals": nasals, "trill": trill, "approx": approx, "pause": pause}

target = sys.argv[1] #Directory of the phonetised transcript

lines = []
diphoneResults = {}
diphoneTypeResults = {}

for con in consonants:
	for vow in vowels:
		vow = re.sub("U", "u", vow)
		vow = re.sub("I", "i", vow)
		if(not (con in emphaticConsonants and vow in nonemphaticVowels)):
			diphoneResults[con + '-' + vow] = 0
			
for con in consonants:
	diphoneResults[con + '-sil'] = 0

for vow in vowels:
	for con in consonants:
		if(len(vow) > 1 and vow[1:] in vowels):
			vow = vow[1:]
		vow = re.sub("U", "u", vow)
		vow = re.sub("I", "i", vow)
		if(not (con in backEmphaticConsonants and vow in nonemphaticVowels) and not (len(con) > 1)):
			diphoneResults[vow + '-' + con] = 0

with open(target, 'r') as file:
	lines = file.readlines()

for line in lines:
	line = line.rstrip()
	line = line.split(' ')
	
	if(len(line) > 1):
		for i in range(1, len(line)):
			next = 'e'
			if(i < len(line) - 1):
				next = line[i+1].rstrip()
			cur = line[i].rstrip()
			prev = line[i -1].rstrip()
			
			prev = re.sub("U", "u", prev)
			prev = re.sub("I", "i", prev)
			cur = re.sub("U", "u", cur)
			cur = re.sub("I", "i", cur)
			next = re.sub("U", "u", next)
			next = re.sub("I", "i", next)
			if(len(prev) > 1 and prev[1:] in vowels):
				prev = prev[1:]

			if(prev + '-' + cur in diphoneResults and not(prev in vowels and cur in consonants and next in vowels)):
				diphoneResults[prev + '-' + cur] += 1

			for type1 in types: #For all boundary types, add the delta to the statistics
				for type2 in types:
					if(prev in types[type1] and cur in types[type2]):
						if(type1 + '-' + type2 in diphoneTypeResults):
							diphoneTypeResults[type1 + "-" + type2] += 1
						else:
							diphoneTypeResults[type1 + "-" + type2] = 1

res = ''
for key in diphoneResults:
	res += key + ', ' + str(diphoneResults[key]) + '\n'

with open("diphone-results.csv", "w") as file:
	file.write(res)
	
res = ''
for key in diphoneTypeResults:
	res += key + ', ' + str(diphoneTypeResults[key]) + '\n'

with open("diphone-types-results.csv", "w") as file:
	file.write(res)