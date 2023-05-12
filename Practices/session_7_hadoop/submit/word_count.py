from mrjob.job import MRJob


class Count(MRJob):
    """ The below mapper() function defines the mapper for MapReduce and takes
    key value argument and generates the output in tuple format .
    The mapper below is splitting the line and generating a word with its own
    count i.e. 1 """

    def mapper(self, _, line):
        for word in line.split():
            yield word, 1

    """ The below reducer() is aggregating the result according to their key and
    producing the output in a key-value format with its total count"""

    def reducer(self, word, counts):
        yield word, sum(counts)


"""the below 2 lines are ensuring the execution of mrjob, the program will not
execute without them"""
if __name__ == '__main__':
    Count.run()
