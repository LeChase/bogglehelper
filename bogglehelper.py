"""
module to solve boggle boards

@gpschnaars
"""

import random

# dict for letter points (taken from scrabble)
letter_points = {'': 0,
'A': 1, 
'B': 4, 
'C': 4, 
'D': 2, 
'E': 1, 
'F': 4, 
'G': 3, 
'H': 3, 
'I': 1, 
'J': 10, 
'K': 5, 
'L': 2, 
'M': 4, 
'N': 2, 
'O': 1, 
'P': 4, 
'QU': 10, 
'R': 1, 
'S': 1, 
'T': 1, 
'U': 1,
'V': 5, 
'W': 4, 
'X': 8, 
'Y': 3, 
'Z': 10}

# read in english dictionary from file
# file must be words in single column
# strip each word, convert to uppercase, create set for faster lookup
dictionary_words = set(line.strip().upper() for line in open('words.txt'))

class Element(object):
    # simple class to store matrix elements with attributes
    def __init__(self, letter = '', position = None, 
                        letter_multiplier = 1, word_multiplier = 1):
        # super is probably unnecessary since inheriting from object base class
        super().__init__()
        # uppercase the letter
        self.letter = letter.upper()
        # set position (is tuple)
        self.position = position
        # obtain letter score from letter_scores dictionary
        self.points = letter_points[self.letter]
        # default letter/word multipliers are 1 (no effect on score)
        self.letter_multiplier = letter_multiplier
        self.word_multiplier = word_multiplier

    def find_neighbors(self, parent):
        # identify neighbors (diagonal, horizontal, vertical) of an item in a matrix
        # ignores positions with indices out of range (< 0 and >= parent length)
        # returns list containing neighboring Elements

        # unpack tuple into coordinates
        i, j = self.position
        # length of parent matrix will be upper bound
        maxlength = len(parent)
        # all potential neighbors
        self.neighbors = [(i - 1, j - 1),
                (i - 1, j),
                (i - 1, j + 1),
                (i, j + 1),
                (i + 1, j + 1),
                (i + 1, j),
                (i + 1, j - 1),
                (i, j - 1)]
        # removes all those coordinate tuples out of range of the matrix
        self.neighbors[:] = [tup for tup in self.neighbors if 
                                all(item >= 0 for item in tup) and
                                all(item < maxlength for item in tup)]
        # convert tuples in the list into the Element objects occupying the spaces
        self.neighbors[:] = [parent.from_tuple(item) for item in self.neighbors]

    def update_neighbors(self, trailing):
        # remove items that are present in the trailing/previous list
        # this is permanent ... not useful in recursion
        self.neighbors[:] = [item for item in self.neighbors if item not in trailing]

    # hidden functions
    def __str__(self):
        # for printing
        return self.letter + ' at ' + str(self.position)

    def __repr__(self):
        # only return letter when called without attribute
        return self.letter


class Matrix(list):
    # subclass list for 2d matrix
    def __init__(self, *args):
        # *args passed as usual arbitrary arguments for list
        super().__init__(*args)
        # initialize empty dict to hold all possible word + score combinations in the matrix
        self.all_tries = {}

        # # reset inputs as attributes of Element class
        # # not needed if *args passed to Matrix are already in Element form
        # self._convert_elements()

        # compute neighbors for each Element in the matrix
        self._determine_neighbors()

    def from_tuple(self, tup):
        # return item at coordinates given by <tup> (tuple)
        return self[tup[0]][tup[1]]

    def find_paths(self):
        # identify all paths through the Matrix
        for lst in self:
            for item in lst:
                # initialize root Trie with first character
                root = Trie([item])
                # see helper function
                self._recurse(item, root)

        # remove letter combinations that are not words (not present in english dictionary)
        self.all_tries = {k: v for k, v in self.all_tries.items() if k in dictionary_words}
        # convert to list of tuples sorted by decreasing score
        self.all_tries = sorted(self.all_tries.items(), key = lambda x: x[1], reverse = 1)
        return self.all_tries

    # helper functions
    def _recurse(self, item, prev):
        # for the current Element, create list of neighbors excluding previous Elements
        updated_neighbors = [neighbor for neighbor in item.neighbors if neighbor not in prev]
        # iterate through available neighbors
        for element in updated_neighbors:
            # create new Trie as to not interfere with past Tries
            new = Trie(prev[:])
            # append current element
            new.append(element)
            # only add word if it is at least 3 characters
            if len(new) >= 3:
                # create new word/score key in dictionary
                self.all_tries[new.word] = new.score
            # check how many neighbors the current element has
            new_neighbors = [neighbor for neighbor in element.neighbors if neighbor not in new]
            # if there is at least 1 neighbor left, perform the recursion
            if len(new_neighbors) > 0:
                self._recurse(element, new)

    def _determine_neighbors(self):
        # given all items in Matrix are Elements, determine neighbors for each Element
        for lst in self:
            for item in lst:
                item.find_neighbors(parent = self)

    def _convert_elements(self):
        # given a pre-made Matrix containining characters,
        # convert all to Element objects and assign tuple coordinates
        self[:] = [[Element(item, (i, j), self) for j, item in enumerate(lst)] 
                                                for i, lst in enumerate(self)]

    @staticmethod
    def random_matrix(size):
        # returns square matrix of side length <size> containing random characters 
        return [[random.choice(letter_points.keys()) for j in range(size)] for i in range(size)]

    @staticmethod
    def pad_list(inputlist, char):
        # add padding charcter to beginning and end of list
        inputlist.insert(0, char)
        inputlist.append(char)
        return inputlist

    @staticmethod
    def pad_matrix(inputmatrix, char):
        # pad a matrix with characters all around
        inputmatrix[:] = [inputmatrix.pad_list(item, char) for item in inputmatrix]
        l = len(inputmatrix) + 2
        pad = [char for i in range(l)]
        inputmatrix.insert(0, pad)
        inputmatrix.append(pad)
        return inputmatrix

    # hidden functions
    def __str__(self):
        # for print function
        # format matrix into proper-shape string
        return '\n'.join([' '.join([x.letter for x in item]) for item in self])


class Trie(list):
    # subclass list
    # Trie will be list of Element objects
    def __init__(self, *args):
        # *args passed as usual arbitrary arguments for list
        super().__init__(*args)

    @property
    def word(self):
        # return word built from concatenated letters of Elements
        return ''.join([item.letter for item in self])

    @property
    def score(self):
        # return score of constructed word
        # function of individual element scores and any multipliers present
        total_score = sum([item.points*item.letter_multiplier for item in self])
        multiplier = self.product([item.word_multiplier for item in self])
        return total_score*multiplier
    
    @staticmethod
    def product(inputlist):
        # returns product of all numbers in list/Trie
        product = 1
        for item in inputlist:
            product *= item
        return product

    # hidden functions
    def __str__(self):
        return ''.join([item.letter for item in self])

    def __repr__(self):
        return self


if __name__ == "__main__":

    pass