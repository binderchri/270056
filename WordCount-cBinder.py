#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #####
# python-version muss python 3 sein
# AUFRUF: > python WordCount-cBinder.py -f input.txt -ger
# entweder -ger oder -eng
# #####

import argparse
import os.path
from itertools import *


def handleArgs():
    """
    Argument handling, returning the input file and the language (either "ger" or "eng")
    :return: Tuple of input file and language string
    """
    parser = argparse.ArgumentParser(description='Counting words in an English or German text')
    parser.add_argument("-f", required=True, dest="filename", help="The filename of the input file")

    parser.add_argument("-ger", dest="language", action="store_const", const="ger",
                        help="The language of the input file is German")
    parser.add_argument("-eng", dest="language", action="store_const", const="eng",
                        help="The language of the input file is English")

    args = parser.parse_args()

    if not args.language:
        parser.error("No language defined, must be either -ger or -eng")

    if not os.path.isfile(args.filename):
        parser.error("Given file doesn't exist")

    return args.filename, args.language


def normalizeChar(character):
    character = character.lower()

    if character == "'":
        return ''

    if not character.isalnum():
        return ' '

    return character


def normalize(line, language):
    # http://stackoverflow.com/questions/12985456/replace-all-non-alphanumeric-characters-in-a-string
    line = ''.join([normalizeChar(s) for s in line]).strip()

    if language is "eng":
        return line

    line = line.replace('ö', 'oe').replace('ä', 'ae').replace('ü', 'ue').replace('ß', 'ss')
    return line


def main():
    fn, language = handleArgs()

    dictionary = dict()
    with open(fn, encoding='utf8') as fp:
        words = list(chain.from_iterable(normalize(line, language).split() for line in fp))
        for word in words:
            dictionary[word] = dictionary.get(word, 0) + 1

    # http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
    sortedByFrequency = sorted(dictionary, key=dictionary.get, reverse=True)
    print(', '.join(sortedByFrequency))


if __name__ == '__main__':
    main()
