#!/usr/bin/python
# -*- coding: UTF8 -*-

import sys
import codecs
import re

unambiguousConsonantMap = {
	u'\u0628': u'b' , u'\u0630': u'th', u'\u0637': u'T' , u'\u0645': u'm',
	u'\u062a': u't' , u'\u0631': u'r' , u'\u0638': u'Z' , u'\u0646': u'n',
	u'\u062b': u'^' , u'\u0632': u'z' , u'\u0639': u'E' , u'\u0647': u'h',
	u'\u062c': u'j' , u'\u0633': u's' , u'\u063a': u'g' , u'\u062d': u'H',
	u'\u0642': u'q' , u'\u0641': u'f' , u'\u062e': u'x' , u'\u0635': u'S',
	u'\u0634': u'$' , u'\u062f': u'd' , u'\u0636': u'D' , u'\u0643': u'k',
	u'\u0623': u'ah', u'\u0621': u'ah', u'\u0626': u'ah', u'\u0624': u'ah',
	u'\u0625': u'ah'
}

buckwalter = {
	u'\u0628': u'b' , u'\u0630': u'th', u'\u0637': u'T' , u'\u0645': u'm',
	u'\u062a': u't' , u'\u0631': u'r' , u'\u0638': u'Z' , u'\u0646': u'n',
	u'\u062b': u'^' , u'\u0632': u'z' , u'\u0639': u'E' , u'\u0647': u'h',
	u'\u062c': u'j' , u'\u0633': u's' , u'\u063a': u'g' , u'\u062d': u'H',
	u'\u0642': u'q' , u'\u0641': u'f' , u'\u062e': u'x' , u'\u0635': u'S',
	u'\u0634': u'$' , u'\u062f': u'd' , u'\u0636': u'D' , u'\u0643': u'k',
	u'\u0623': u'>' , u'\u0621': u'\'', u'\u0626': u'}' , u'\u0624': u'&',
	u'\u0625': u'<' , u'\u0622': u'|' , u'\u0627': u'A' , u'\u0649': u'Y',
	u'\u0629': u'p' , u'\u064a': u'y' , u'\u0644': u'l' , u'\u0648': u'w',
	u'\u064B': u'F' , u'\u064C': u'N' , u'\u064D': u'K' , u'\u064E': u'a',
	u'\u064F': u'u' , u'\u0650': u'i' , u'\u0651': u'~' , u'\u0652': u'o'
}
def arabicToBuckwalter(word):
	res = ''
	for letter in word:
		if(letter in buckwalter):
			res += buckwalter[letter]
	return res

ambiguousConsonantMap = {
	u'\u0644': [u'l', u''], u'\u0648': u'w', u'\u064a': u'y', u'\u0629': [u't', u''] #These consonants are only unambiguous in certain contexts
}

maddaMap = {
	u'\u0622': [[u'ah', u'a:'], [u'ah', u'A:']]
}

vowelMap = {
	u'\u0627': [[u'a:', u''], [u'A:', u'']], u'\u0649': [[u'a:', u''], [u'A:', u'']],
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
forwardEmphatics = [u'\u063a', u'\u062e']
consonants = [u'\u0623', u'\u0625', u'\u0626', u'\u0624', u'\u0621', u'\u0628', u'\u062a', u'\u062b', u'\u062c', u'\u062d', u'\u062e', u'\u062f', u'\u0630', u'\u0631', u'\u0632', u'\u0633', u'\u0634', u'\u0635', u'\u0636', u'\u0637', u'\u0638', u'\u0639', u'\u063a', u'\u0641', u'\u0642', u'\u0643', u'\u0644', u'\u0645', u'\u0646', u'\u0647', u'\u0622']

fixedWords = {
	u'\u0647\u0630\u0627': [u'h a: th a:', u'h a: th a',],
	u'\u0647\u0630\u0647': [u'h a: th i0 h i0', u'h a: th i1 h'],
	u'\u0647\u0630\u0627\u0646': [u'h a: th a: n i0', u'h a: th a: n'],
	u'\u0647\u0624\u0644\u0627\u0621': [u'h a: ah u0 l a: ah i0', u'h a: ah u0 l a: ah'],
	u'\u0630\u0644\u0643': [u'th a: l i0 k a', u'th a: l i0 k'],
	u'\u0643\u0630\u0644\u0643': [u'k a th a: l i0 k a', u'k a th a: l i1 k'],
	u'\u0630\u0644\u0643\u0645': u'th a: l i0 k u1 m',
	u'\u0623\u0648\u0644\u0626\u0643': [u'ah u0 l a: ah i0 k a', u'ah u0 l a: ah i1 k'],
	u'\u0637\u0647': u'T a: h a',
	u'\u0644\u0643\u0646': [u'l a: k i0 nn a', u'l a: k i1 n'],
	u'\u0644\u0643\u0646\u0647': u'l a: k i0 nn a h u0',
	u'\u0644\u0643\u0646\u0647\u0645': u'l a: k i0 nn a h u1 m',
	u'\u0644\u0643\u0646\u0643': [u'l a: k i0 nn a k a', u'l a: k i0 nn a k i0'],
	u'\u0644\u0643\u0646\u0643\u0645': u'l a: k i0 nn a k u1 m',
	u'\u0644\u0643\u0646\u0643\u0645\u0627': u'l a: k i0 nn a k u0 m a:',
	u'\u0644\u0643\u0646\u0646\u0627': u'l a: k i0 nn a n a:',
	u'\u0627\u0644\u0631\u062D\u0645\u0646': [u'rr a H m a: n i0',  u'rr a H m a: n'],
	u'\u0627\u0644\u0644\u0647': [u'll a: h i0', u'll a: h', u'll A: h u0', u'll A: h a', u'll A: h', u'll A'],
	u'\u0647\u0630\u064A\u0646': [u'h a: th a y n i0', u'h a: th a y n']
}
def isFixedWord(word, results, orthography):
	lastLetter = word[-1]
	if(lastLetter == u'\u064e'):
		lastLetter = [u'a', u'A']
	elif(lastLetter == u'\u0627'):
		lastLetter = [u'a:']
	elif(lastLetter == u'\u064f'):
		lastLetter = [u'u0']
	elif(lastLetter == u'\u0650'):
		lastLetter = [u'i0']
	elif(lastLetter in unambiguousConsonantMap):
		lastLetter = [unambiguousConsonantMap[lastLetter]]
	wordConsonants = re.sub(u'[^\u0647\u0630\u0627\u0647\u0646\u0621\u0623\u0648\u0644\u0626\u0643\u0645\u064A\u0637]', '', word)
	if(wordConsonants in fixedWords):
		if(isinstance(fixedWords[wordConsonants], list)):
			for pronunciation in fixedWords[wordConsonants]:
				if(pronunciation.split(' ')[-1] in lastLetter):
					results += orthography + ' ' + pronunciation + '\n'
		else:
			results += orthography + ' ' + fixedWords[wordConsonants] + '\n'
	return results

inputFileName = sys.argv[1]
inputFile = codecs.open(inputFileName, 'r', 'utf-8')
utterances = inputFile.read().splitlines()
inputFile.close()

result = ''

for utterance in utterances:
	utterance = utterance.replace(u'\u0627\u064b', u'\u064b')
	utterance = utterance.replace(u'\u0652', u'')
	utterance = utterance.replace(u'\u064e\u0627', u'\u0627')
	utterance = utterance.replace(u'\u064e\u0649', u'\u0649')
	utterance = utterance.replace(u' \u0627', u' ')
	utterance = utterance.replace(u'\u064b', u'\u064e\u0646')
	utterance = utterance.replace(u'\u064c', u'\u064f\u0646')
	utterance = utterance.replace(u'\u064d', u'\u0650\u0646')
	utterance = utterance.replace(u'\u0622', u'\u0623\u0627')
	utterance = utterance.split(u' ')

	for word in utterance:
		if(word != '-'):
			orthography = arabicToBuckwalter(word)
			result = isFixedWord(word, result, orthography)
		
			emphaticContext = False
			word = u'bb' + word + u'ee' #This is the end/beginning of word symbol. just for convenience
			
			phones = []
			for index in range(2, len(word) - 2):
				letter = word[index]
				letter1 = word[index + 1]
				letter2 = word[index + 2]
				letter_1 = word[index - 1]
				letter_2 = word[index - 2]
				#----------------------------------------------------------------------------------------------------------------
				if(letter in consonants and not letter in emphatics + [u'\u0631'""", u'\u0644'"""]):#non-emphatic consonants (except for Lam and Ra) change emphasis to 'no emphasis'
					emphaticContext = False
				if(letter in forwardEmphatics):
					emphaticContext = True
				if(letter1 in emphatics and not letter1 in forwardEmphatics):
					emphaticContext = True
				#----------------------------------------------------------------------------------------------------------------
				#----------------------------------------------------------------------------------------------------------------
				if(letter in unambiguousConsonantMap):#Unambiguous phones
					phones += [unambiguousConsonantMap[letter]]
				#----------------------------------------------------------------------------------------------------------------
				if(letter == u'\u0644'):
					if(not letter1 in diacritics and letter2 in [u'\u0651']):#Lam could be omitted in definite article (sun letters)
						phones += [ambiguousConsonantMap[u'\u0644'][1]]
					else:
						phones += [ambiguousConsonantMap[u'\u0644'][0]]
				#----------------------------------------------------------------------------------------------------------------
				if(letter == u'\u0651' and not letter_1 in [u'\u0648', u'\u064a']):#shadda just doubles the letter before it
					phones[len(phones) - 1] += phones[len(phones) - 1]
				#----------------------------------------------------------------------------------------------------------------
				if(letter == u'\u0622'):#Madda only changes based in emphaticness
					if(emphaticContext):
						phones += [maddaMap[u'\u0622'][1]]
					else:
						phones += [maddaMap[u'\u0622'][0]]
				#----------------------------------------------------------------------------------------------------------------
				if(letter == u'\u0629'):#Ta' marboota is determined by the following if it is a diacritic or not
					if(letter1 in diacritics):
						phones += [ambiguousConsonantMap[u'\u0629'][0]]
					else:
						phones += [ambiguousConsonantMap[u'\u0629'][1]]
				#----------------------------------------------------------------------------------------------------------------
				if(letter in vowelMap):
					if(letter in [u'\u0648', u'\u064a']): #Waw and Ya are complex they could be consonants or vowels and their gemination is complex as it could be a combination of a vowel and consonants
						if(letter1 in diacritics + [u'\u0627'] or (letter1 in [u'\u0648', u'\u064a'] and not letter2 in diacritics + [u'\u0627', u'\u0648', u'\u064a'])):
							phones += [ambiguousConsonantMap[letter]]
						elif(letter1 in [u'\u0651']):
							if(letter_1 in [u'\u064e']):
								phones += [ambiguousConsonantMap[letter], ambiguousConsonantMap[letter]]
							else:
								phones += [vowelMap[letter][0][0], ambiguousConsonantMap[letter]]
						else:
							if(emphaticContext):	
								phones += [vowelMap[letter][1][0]]
							else:
								phones += [vowelMap[letter][0][0]]
					if(letter in [u'\u064f', u'\u0650']): #Kasra and Damma could be mildened if before a final silent consonant
						if(emphaticContext):
							if((letter1 in unambiguousConsonantMap or letter1 == u'\u0644') and letter2 == u'e' and len(word) > 7):
								phones += [vowelMap[letter][1][1]]
							else:
								phones += [vowelMap[letter][1][0]]
						else:
							if((letter1 in unambiguousConsonantMap or letter1 == u'\u0644') and letter2 == u'e' and len(word) > 7):
								phones += [vowelMap[letter][0][1]]
							else:
								phones += [vowelMap[letter][0][0]]
					if(letter in [u'\u064e', u'\u0627', u'\u0649']): #Alif could be ommited in definite article and beginning of some words
						if(letter in [u'\u0627'] and letter_1 in [u'\u0648', u'\u0643'] and letter_2 == u'b'):
							phones += [[vowelMap[letter][0][0], u'a']]
						elif(letter in [u'\u0627'] and letter_1 in [u'\u064f', u'\u0650']):
							temp = True #do nothing
						elif(letter in [u'\u0627', u'\u0649'] and letter1 in [u'e']):
							if(emphaticContext):
								phones += [[vowelMap[letter][1][0], vowelMap[u'\u064e'][1]]]
							else:
								phones += [[vowelMap[letter][0][0], vowelMap[u'\u064e'][0]]]
						else:
							if(emphaticContext):
								phones += [vowelMap[letter][1][0]]
							else:
								phones += [vowelMap[letter][0][0]]
			
			possibilities = 1
			pronunciations = []
			for letter in phones:
				if(isinstance(letter, list)):
					possibilities = possibilities * len(letter)
			for i in range(0, possibilities):
				pronunciations.append([])
				iterations = 1
				for index, letter in enumerate(phones):
					if(isinstance(letter, list)):
						curIndex = (i / iterations) % len(letter)
						if(letter[curIndex] != u''):
							pronunciations[i].append(letter[curIndex])
						iterations = iterations * len(letter)
					else:
						if(letter != u''):
							pronunciations[i].append(letter)
			for pronunciation in pronunciations:
				prevLetter = ''
				toDelete = []
				for i in range(0, len(pronunciation)):
					letter = pronunciation[i]
					if(letter in ['a:', 'u0:', 'i0:', 'A:', 'U0:', 'I0:'] and prevLetter == letter[0:-1]):
						toDelete.append(i - 1)
					prevLetter = letter
				for i in toDelete:
					del(pronunciation[i])
				result += orthography + ' ' + ' '.join(pronunciation) + '\n'

outFile = codecs.open('dict', 'w', u'utf-8')
outFile.write(result)
outFile.close()