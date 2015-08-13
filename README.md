# Arabic-Phonetiser
Convert Arabic diacritised text to a sequence of phonemes and create a pronunciation dictionary from them for alignment using HTK

# Usage
      phonetise-Buckwalter.py [inputfile]

[inputfile] should be a utf8 text file contianing in every line: "[sound-filename]" "[arabic-text-in-buckwalter]"
the output will be two files:
dict: contianing the sorted pronunciation dicationary with a carrage return at the end for use with tools like HTK
utterance-pronunciations.txt: A file contianing in every line: "[sound-filename]" "[phoneme-sequence]"
