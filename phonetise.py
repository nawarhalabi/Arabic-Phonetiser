#!/usr/bin/python
# -*- coding: UTF8 -*-

import sys
import codecs
import re

unambiguousConsonantMap = {
	u'\u0628': u'b' , u'\u0630': u'*' , u'\u0637': u'T' , u'\u0645': u'm' ,
	u'\u062a': u't' , u'\u0631': u'r' , u'\u0638': u'Z' , u'\u0646': u'n' ,
	u'\u062b': u'^' , u'\u0632': u'z' , u'\u0639': u'E' , u'\u0647': u'h' ,
	u'\u062c': u'j' , u'\u0633': u's' , u'\u063a': u'g' , u'\u062d': u'H' ,
	u'\u0642': u'q' , u'\u0641': u'f' , u'\u062e': u'x' , u'\u0635': u'S' ,
	u'\u0634': u'$' , u'\u062f': u'd' , u'\u0636': u'D' , u'\u0643': u'k' ,
	u'\u0623': u'<' , u'\u0621': u'<' , u'\u0626': u'<' , u'\u0624': u'<' ,
	u'\u0625': u'<'
}

buckwalter = {
	u'\u0628': u'b' , u'\u0630': u'*' , u'\u0637': u'T' , u'\u0645': u'm',
	u'\u062a': u't' , u'\u0631': u'r' , u'\u0638': u'Z' , u'\u0646': u'n',
	u'\u062b': u'^' , u'\u0632': u'z' , u'\u0639': u'E' , u'\u0647': u'h',
	u'\u062c': u'j' , u'\u0633': u's' , u'\u063a': u'g' , u'\u062d': u'H',
	u'\u0642': u'q' , u'\u0641': u'f' , u'\u062e': u'x' , u'\u0635': u'S',
	u'\u0634': u'$' , u'\u062f': u'd' , u'\u0636': u'D' , u'\u0643': u'k',
	u'\u0623': u'>' , u'\u0621': u'\'', u'\u0626': u'}' , u'\u0624': u'&',
	u'\u0625': u'<' , u'\u0622': u'|' , u'\u0627': u'A' , u'\u0649': u'Y',
	u'\u0629': u'p' , u'\u064a': u'y' , u'\u0644': u'l' , u'\u0648': u'w',
	u'\u064b': u'F' , u'\u064c': u'N' , u'\u064d': u'K' , u'\u064e': u'a',
	u'\u064f': u'u' , u'\u0650': u'i' , u'\u0651': u'~' , u'\u0652': u'o'
}

def arabicToBuckwalter(word):
	res = ''
	for letter in word:
		if(letter in buckwalter):
			res += buckwalter[letter]
		else:
			res += letter
	return res

ambiguousConsonantMap = {
	u'\u0644': [u'l', u''], u'\u0648': u'w', u'\u064a': u'y', u'\u0629': [u't', u''] #These consonants are only unambiguous in certain contexts
}

maddaMap = {
	u'\u0622': [[u'<', u'aa'], [u'<', u'AA']]
}

vowelMap = {
	u'\u0627': [[u'aa', u''], [u'AA', u'']], u'\u0649': [[u'aa', u''], [u'AA', u'']],
	u'\u0648': [[u'uu0', u'uu1'], [u'UU0', u'UU1']],
	u'\u064a': [[u'ii0', u'ii1'], [u'II0', u'II1']],
	u'\u064e': [u'a', u'A'],
	u'\u064f': [[u'u0', u'u1'], [u'U0', u'U1']],
	u'\u0650': [[u'i0', u'i1'], [u'I0', u'I1']],
}

nunationMap = {
	u'\u064b': [[u'a', u'n'], [u'A', u'n']], u'\u064c':[[u'u1', u'n'], [u'U1', u'n']], u'\u064d': [[u'i1', u'n'], [u'I1', u'n']]
}

diacritics = [u'\u0652', u'\u064e', u'\u064f', u'\u0650', u'\u064b', u'\u064c', u'\u064d', u'\u0651']
diacriticsWithoutShadda = [u'\u0652', u'\u064e', u'\u064f', u'\u0650', u'\u064b', u'\u064c', u'\u064d']
emphatics = [u'\u0636', u'\u0635', u'\u0637', u'\u0638', u'\u063a', u'\u062e', u'\u0642']
forwardEmphatics = [u'\u063a', u'\u062e']
consonants = [u'\u0623', u'\u0625', u'\u0626', u'\u0624', u'\u0621', u'\u0628', u'\u062a', u'\u062b', u'\u062c', u'\u062d', u'\u062e', u'\u062f', u'\u0630', u'\u0631', u'\u0632', u'\u0633', u'\u0634', u'\u0635', u'\u0636', u'\u0637', u'\u0638', u'\u0639', u'\u063a', u'\u0641', u'\u0642', u'\u0643', u'\u0644', u'\u0645', u'\u0646', u'\u0647', u'\u0622']

fixedWords = {
	u'\u0647\u0630\u0627': [u'h aa * aa', u'h aa * a',],
	u'\u0647\u0630\u0647': [u'h aa * i0 h i0', u'h aa * i1 h'],
	u'\u0647\u0630\u0627\u0646': [u'h aa * aa n i0', u'h aa * aa n'],
	u'\u0647\u0624\u0644\u0627\u0621': [u'h aa < u0 l aa < i0', u'h aa < u0 l aa <'],
	u'\u0630\u0644\u0643': [u'* aa l i0 k a', u'* aa l i0 k'],
	u'\u0643\u0630\u0644\u0643': [u'k a * aa l i0 k a', u'k a * aa l i1 k'],
	u'\u0630\u0644\u0643\u0645': u'* aa l i0 k u1 m',
	u'\u0623\u0648\u0644\u0626\u0643': [u'< u0 l aa < i0 k a', u'< u0 l aa < i1 k'],
	u'\u0637\u0647': u'T aa h a',
	u'\u0644\u0643\u0646': [u'l aa k i0 nn a', u'l aa k i1 n'],
	u'\u0644\u0643\u0646\u0647': u'l aa k i0 nn a h u0',
	u'\u0644\u0643\u0646\u0647\u0645': u'l aa k i0 nn a h u1 m',
	u'\u0644\u0643\u0646\u0643': [u'l aa k i0 nn a k a', u'l aa k i0 nn a k i0'],
	u'\u0644\u0643\u0646\u0643\u0645': u'l aa k i0 nn a k u1 m',
	u'\u0644\u0643\u0646\u0643\u0645\u0627': u'l aa k i0 nn a k u0 m aa',
	u'\u0644\u0643\u0646\u0646\u0627': u'l aa k i0 nn a n aa',
	u'\u0627\u0644\u0631\u062D\u0645\u0646': [u'rr a H m aa n i0',  u'rr a H m aa n'],
	u'\u0627\u0644\u0644\u0647': [u'll aa h i0', u'll aa h', u'll AA h u0', u'll AA h a', u'll AA h', u'll A'],
	u'\u0647\u0630\u064a\u0646': [u'h aa * a y n i0', u'h aa * a y n'],
	
	u'\u0646\u062a': u'n i1 t',
	u'\u0641\u064a\u062F\u064a\u0648': u'v i0 d y uu1',
	u'\u0644\u0646\u062F\u0646': u'l A n d u1 n'
}

def isFixedWord(word, results, orthography):
	lastLetter = word[-1]
	if(lastLetter == u'\u064e'):
		lastLetter = [u'a', u'A']
	elif(lastLetter == u'\u0627'):
		lastLetter = [u'aa']
	elif(lastLetter == u'\u064f'):
		lastLetter = [u'u0']
	elif(lastLetter == u'\u0650'):
		lastLetter = [u'i0']
	elif(lastLetter in unambiguousConsonantMap):
		lastLetter = [unambiguousConsonantMap[lastLetter]]
	wordConsonants = re.sub(u'[^\u0647\u0630\u0627\u0647\u0646\u0621\u0623\u0648\u0644\u0626\u0643\u0645\u064A\u0637\u062a\u0641\u062F]', '', word)#Remove all dacritics from word
	if(wordConsonants in fixedWords):#check if word is in the fixed word lookup table
		if(isinstance(fixedWords[wordConsonants], list)):
			for pronunciation in fixedWords[wordConsonants]:
				if(pronunciation.split(' ')[-1] in lastLetter):
					results += orthography + ' ' + pronunciation + '\n'#add each pronunciation to the pronunciation dictionary
		else:
			results += orthography + ' ' + fixedWords[wordConsonants] + '\n'#add pronunciation to the pronunciation dictionary
	return results

inputFileName = sys.argv[1]
inputFile = codecs.open(inputFileName, 'r', 'utf-8')
utterances = inputFile.read().splitlines()
inputFile.close()

result = ''

for utterance in utterances:
	number = utterance.split(',')[0].strip()
	utterance = utterance.split(',')[1].strip()

	utteranceText = arabicToBuckwalter(utterance)

	zeros = "" + "0" * (4 - len(number))
	utteranceLabelFile = codecs.open("labels/ARA NORM  " + zeros + number + ".lab", "w", "utf-8")

	utteranceLabelFile.write(utteranceText.replace(' - ', ' sil '))
	utteranceLabelFile.close()

	utteranceText = utteranceText.split(' ')

	utterance = utterance.replace(u'\u0627\u064b', u'\u064b')
	utterance = utterance.replace(u'\u0640', u'')
	utterance = utterance.replace(u'\u0652', u'')
	utterance = utterance.replace(u'\u064e\u0627', u'\u0627')
	utterance = utterance.replace(u'\u064e\u0649', u'\u0649')
	utterance = utterance.replace(u' \u0627', u' ')
	utterance = utterance.replace(u'\u064b', u'\u064e\u0646')
	utterance = utterance.replace(u'\u064c', u'\u064f\u0646')
	utterance = utterance.replace(u'\u064d', u'\u0650\u0646')
	utterance = utterance.replace(u'\u0622', u'\u0623\u0627')
	
	#Deal with Hamza types that when not followed by a short vowel letter, this short vowel is added automatically
	utterance = re.sub(u'\u0627\u0650', u'\u0625\u0650', utterance)
	utterance = re.sub(u'\u0627\u064e', u'\u0623\u064e', utterance)
	utterance = re.sub(u'\u0627\u064f', u'\u0623\u064f', utterance)
	utterance = re.sub(u'^\u0623([^\u064e\u064f\u0627\u0648])', u'\u0623\u064e\\1', utterance)
	utterance = re.sub(u' \u0623([^\u064e\u064f\u0627\u0648 ])', u' \u0623\u064e\\1', utterance)
	utterance = re.sub(u'\u0625([^\u0650])', u'\u0625\u0650\\1', utterance)
	if(utteranceNumber < 3):
		print utterance
	
	utterance = utterance.split(u' ')

	wordIndex = -1
	for word in utterance:
		wordIndex += 1
		if(word != '-'):
			orthography = utteranceText[wordIndex]

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
				if(letter in consonants + [u'\u0648', u'\u064a'] and not letter in emphatics + [u'\u0631'""", u'\u0644'"""]):#non-emphatic consonants (except for Lam and Ra) change emphasis to 'no emphasis'
					emphaticContext = False
				if(letter in emphatics):
					emphaticContext = True
				if(letter1 in emphatics and not letter1 in forwardEmphatics):
					emphaticContext = True
				#----------------------------------------------------------------------------------------------------------------
				#----------------------------------------------------------------------------------------------------------------
				if(letter in unambiguousConsonantMap):#Unambiguous phones
					phones += [unambiguousConsonantMap[letter]]
				#----------------------------------------------------------------------------------------------------------------
				if(letter == u'\u0644'):
					if((not letter1 in diacritics and not letter1 in vowelMap) and letter2 in [u'\u0651']):#Lam could be omitted in definite article (sun letters)
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
						if(letter1 in diacriticsWithoutShadda + [u'\u0627', u'\u0649'] or (letter1 in [u'\u0648', u'\u064a'] and not letter2 in diacritics + [u'\u0627', u'\u0648', u'\u064a']) or (letter_1 in diacriticsWithoutShadda and letter1 in consonants + [u'e'])):
							if((letter in [u'\u0648'] and letter_1 in [u'\u064f'] and not letter1 in [u'\u064e', u'\u0650', u'\u0627', u'\u0649']) or (letter in [u'\u064a'] and letter_1 in [u'\u0650'] and not letter1 in [u'\u064e', u'\u064f', u'\u0627', u'\u0649'])):
								if(emphaticContext):
									phones += [vowelMap[letter][1][0]]
								else:
									phones += [vowelMap[letter][0][0]]
							else:
								if(letter1 in [u'\u0627'] and letter in [u'\u0648'] and letter2 in [u'e']):
									phones += [[ambiguousConsonantMap[letter], vowelMap[letter][0][0]]]
								else:
									phones += [ambiguousConsonantMap[letter]]
						elif(letter1 in [u'\u0651']):
							if(letter_1 in [u'\u064e'] or (letter in [u'\u0648'] and letter_1 in [u'\u0650', u'\u064a']) or (letter in [u'\u064a'] and letter_1 in [u'\u0648', u'\u064f'])):
								phones += [ambiguousConsonantMap[letter], ambiguousConsonantMap[letter]]
							else:
								phones += [vowelMap[letter][0][0], ambiguousConsonantMap[letter]]
						else:#Waws and Ya's at the end of the word could be shortened
							if(emphaticContext):
								if(letter_1 in consonants + [u'\u064f', u'\u0650'] and letter1 in [u'e']):
									phones += [[vowelMap[letter][1][0], vowelMap[letter][1][0][1:]]]
								else:
									phones += [vowelMap[letter][1][0]]
							else:
								if(letter_1 in consonants + [u'\u064f', u'\u0650'] and letter1 in [u'e']):
									phones += [[vowelMap[letter][0][0], vowelMap[letter][0][0][1:]]]
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
						elif(letter in [u'\u0627'] and letter_1 in [u'\u0648'] and letter1 in [u'e']): #Waw al jama3a: The Alif after is optional
							phones += [[vowelMap[letter][0][0], vowelMap[letter][0][1]]]
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
					if(letter in ['aa', 'uu0', 'ii0', 'AA', 'UU0', 'II0'] and prevLetter.lower() == letter[1:].lower()):
						toDelete.append(i - 1)
						pronunciation[i] = pronunciation[i - 1][0] + pronunciation[i - 1]
					if(letter in ['u0', 'i0'] and prevLetter.lower() == letter.lower()):
						toDelete.append(i - 1)
						pronunciation[i] = pronunciation[i - 1]
					if(letter in ['y', 'w'] and prevLetter == letter):
						pronunciation[i - 1] += pronunciation[i - 1]
						toDelete.append(i);
					
					prevLetter = letter
				for i in reversed(range(0, len(toDelete))):
					del(pronunciation[toDelete[i]])
				result += orthography + ' ' + ' '.join(pronunciation) + '\n'
			
outFile = codecs.open('dict', 'w', u'utf-8')
outFile.write(result.strip())
outFile.close()