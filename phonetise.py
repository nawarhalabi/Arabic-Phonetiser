#!/usr/bin/python
# -*- coding: UTF8 -*-

import sys
import codecs

unambiguousConsonantMap = {
	u'\u0628': u'b' , u'\u0630': u'th', u'\u0637': u'T' , u'\u0645': u'm',
	u'\u062a': u't' , u'\u0631': u'r' , u'\u0638': u'Z' , u'\u0646': u'n',
	u'\u062b': u'^' , u'\u0632': u'z' , u'\u0639': u'E' , u'\u0647': u'h',
	u'\u062c': u'j' , u'\u0633': u's' , u'\u063a': u'g' , u'\u062d': u'H',
	u'\u0642': u'q' , u'\u0641': u'f' , u'\u062e': u'x' , u'\u0635': u'S',
	u'\u0642': u'q' , u'\u062f': u'd' , u'\u0636': u'D' , u'\u0643': u'k',
	u'\u0623': u'ah', u'\u0621': u'ah', u'\u0626': u'ah', u'\u0624': u'ah',
	u'\u0625': u'ah'
}

ambiguousConsonantMap = {
	u'\u0644': [u'l', u''], u'\u0648': u'w', u'\u064a': u'j', u'\u0629': [u't', u''] #These consonants are only unambiguous in certain contexts
}

maddaMap = {
	u'\u0622': [[u'ah', u'a:'], [u'ah', u'A:']]
}

vowelMap = {
	u'\u0627': [[u'a:', u''], [u'A:', u'']], u'\u0649': [u'a:', u'A:'],
	u'\u0648': [[u'u0:', u'u1:'], [u'U0:', u'U1:']],
	u'\u064a': [[u'i0:', u'i1:'], [u'I0:', u'I1:']],
	u'\u064e': [u'a', u'A'],
	u'\u064f': [[u'u0', u'u1'], [u'U0', u'U1']],
	u'\u0650': [[u'i0', u'i1'], [u'I0', u'I1']],
}

nunationMap = {
	u'\u064b': [[u'a', u'n'], [u'A', u'n']], u'\u064c':[[u'u1', u'n'], [u'U1', u'n']], u'\u064d': [[u'i1', u'n'], [u'I1', u'n']]
}

diacritics = [u'\u0652', u'\u064e', u'\u064f', u'\u0650', u'\u064b', u'\u064c', u'\u064d', u'\u0651']
emphatics = [u'\u0636', u'\u0635', u'\u0637', u'\u0638', u'\u063a', u'\u062e', u'\u0642']
consonants = [u'\u0623', u'\u0625', u'\u0626', u'\u0624', u'\u0621', u'\u0628', u'\u062a', u'\u062b', u'\u062c', u'\u062d', u'\u062e', u'\u062f', u'\u0630', u'\u0631', u'\u0632', u'\u0633', u'\u0634', u'\u0635', u'\u0636', u'\u0637', u'\u0638', u'\u0639', u'\u063a', u'\u0641', u'\u0642', u'\u0643', u'\u0644', u'\u0645', u'\u0646', u'\u0647', u'\u0622']

inputFileName = sys.argv[1]
inputFile = codecs.open(inputFileName, "r", "utf-8")
utterances = inputFile.read().splitlines()
inputFile.close()

result = ""

for utterance in utterances:
	print len(utterance)
	utterance = utterance.replace(u'\u0627\u064b', u'\u064b')
	utterance = utterance.replace(u'\u0652', u'')
	utterance = utterance.replace(u'\u064e\u0627', u'\u0627')
	utterance = utterance.replace(u' \u0627', u' ')
	utterance = utterance.split(u' ')

	for word in utterance:
		result += word
		if(word != "-"):
			emphaticContext = False
			word = u'bb' + word + u'ee' #This is the end/beginning of word symbol. just for convenience
			
			phones = []
			for index in range(2, len(word) - 2):
				letter = word[index]
				
				#----------------------------------------------------------------------------------------------------------------
				if(word[index] in consonants and not word[index] in emphatics + [u'\u0631', u'\u0644']):
					emphaticContext = False
				if(word[index + 1] in emphatics):
					emphaticContext = True
				#----------------------------------------------------------------------------------------------------------------
				#----------------------------------------------------------------------------------------------------------------
				if(letter in unambiguousConsonantMap):#Unambiguous phones
					phones += [unambiguousConsonantMap[letter]]
				#----------------------------------------------------------------------------------------------------------------
				if(letter == u'\u0644'):
					if(not word[index + 1] in diacritics):#Lam could be omitted in definite article (sun letters)
						print "test"
						phones += [ambiguousConsonantMap[u'\u0644']]
					else:
						phones += [ambiguousConsonantMap[u'\u0644'][0]]
				#----------------------------------------------------------------------------------------------------------------
				if(letter == u'\u0651' and not word[index - 1] in [u'\u0648', u'\u064a']):#shadda just doubles the letter before it
					phones[len(phones) - 1] += phones[len(phones) - 1]
				#----------------------------------------------------------------------------------------------------------------
				if(letter == u'\u0622'):#Madda only changes based in emphaticness
					if(emphaticContext):
						phones += [maddaMap[u'\u0622'][1]]
					else:
						phones += [maddaMap[u'\u0622'][0]]
				#----------------------------------------------------------------------------------------------------------------
				if(letter == u'\u0629'):#Ta' matboota is determined by the following if it is a diacritic or not
					if(word[index + 1] in diacritics):
						phones += [ambiguousConsonantMap[u'\u0629'][0]]
					else:
						phones += [ambiguousConsonantMap[u'\u0629'][1]]
				#----------------------------------------------------------------------------------------------------------------
				if(letter in vowelMap):
					if(letter in [u'\u0648', u'\u064a']): #Waw and Ya are complex they could be consonants or vowels and their gemination is complex as it could be a combination of a vowel and consonants
						if(word[index + 1] in diacritics + [u'\u0627'] or (word[index + 1] in [u'\u0648', u'\u064a'] and not word[index + 2] in diacritics + [u'\u0627', u'\u0648', u'\u064a'])):
							phones += [ambiguousConsonantMap[letter]]
						elif(word[index + 1] in [u'\u0651']):
							if(word[index - 1] in [u'\u064e']):
								phones += [ambiguousConsonantMap[letter] + ambiguousConsonantMap[letter]]
							else:
								phones += [vowelMap[letter][0][0] + ambiguousConsonantMap[letter]]
						else:
							if(emphaticContext):	
								phones += [vowelMap[letter][1][0]]
							else:
								phones += [vowelMap[letter][0][0]]
					if(letter in [u'\u064f', u'\u0650']): #Kasra and Damma could be mildened if before a final silent consonant
						if(emphaticContext):
							if((word[index + 1] in unambiguousConsonantMap or word[index + 1] == u'\u0644') and word[index + 2] == u'e'):
								phones += [vowelMap[letter][1][1]]
							else:
								phones += [vowelMap[letter][1][0]]
						else:
							if((word[index + 1] in unambiguousConsonantMap or word[index + 1] == u'\u0644') and word[index + 2] == u'e'):
								phones += vowelMap[letter][0][1]
							else:
								phones += [vowelMap[letter][0][0]]
					if(letter in [u'\u064e', u'\u0627', u'\u0649']): #Alif could be ommited in definite article and beginning of some words
						if(letter in [u'\u0627'] and word[index - 1] in [u'\u0648', u'\u0643'] and word[index - 2] == u'b'):
							phones += [vowelMap[letter][0] + [u'a']]
						else:
							if(emphaticContext):	
								phones += [vowelMap[letter][1]]
							else:
								phones += [vowelMap[letter][0]]
			print phones
			#result += "".join(phones) + " " + " ".join(phones) + '\n'

outFile = codecs.open("dict", "w", u'utf-8')
outFile.write(result)
outFile.close()