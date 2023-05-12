# -*-coding:utf-8 -*
import sys
import collections
import statistics

wordCount = collections.Counter()
wordLengthCount = collections.Counter()
wordLengthList = []
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from mapper.py
    word, count = line.split('\t', 1)
    # ensure that it's a string followed by an int
    try:
        word = str(word)
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue
    length: int = len(word)
    wordCount[word] += count
    wordLengthCount[str(length)] += count
    # expand the counted words to a full list
    # to enable median to be calculated later
    lengthRepeated = [length] * count
    wordLengthList.extend(lengthRepeated)

for commonWord, commonWordCount in wordCount.most_common(100):
    print("{}\t{}".format(commonWord, commonWordCount))

print("\n")
for commonLength, lengthCount in wordLengthCount.most_common():
    print("{}\t{}".format(commonLength, lengthCount))

print("\n")
print("Number of words: {}".format(len(wordLengthList)))
print("Median word length: {:.0f}".format(statistics.median(wordLengthList)))
