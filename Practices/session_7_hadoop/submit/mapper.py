# -*-coding:utf-8 -*
import sys
import string
import collections

wordCount = collections.Counter()
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # ignore case to avoid duplicates
    lower = line.lower()
    # replace punctuation with spaces, except for hyphens
    punc = string.punctuation
    punc_nohyphens = punc.replace('-', '')
    justText = lower.translate(
        str.maketrans(' ', ' ', punc_nohyphens))
    # allow hyphenated words, but watch out for
    # double-hyphens which might be a stand-in for em-dash
    emdashRemoved = justText.replace('--', ' ')
    # split the line into words
    words = emdashRemoved.split()
    # now we can remove leading and trailing curly quotes
    # and hyphens, but leave apostrophes in the middle
    # and allow hyphenated words.
    # note that we lose possessive ending in s, e.g. Angus'
    punc_curly = '”’‘“-'
    for word in words:
        word = word.strip(punc_curly)
        if len(word) > 0:
            wordCount[word] += 1
# write the results, tab delimited
# which will be the input for reducer.py
for word, count in wordCount.most_common():
    print('%s\t%s' % (word, count))
