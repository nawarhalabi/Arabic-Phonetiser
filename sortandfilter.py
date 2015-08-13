#!/usr/bin/python
# -*- coding: UTF8 -*-

import sys
import codecs
import re

def distinct(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

inputFileName = sys.argv[1]
inputFile = codecs.open(inputFileName, 'r', 'utf-8')
utterances = inputFile.read().splitlines()
inputFile.close()

utterances = sorted(distinct(utterances))

inputFile = codecs.open(inputFileName, 'w', 'utf-8')
inputFile.write("\n".join(utterances) + '\r\n')
inputFile.close()