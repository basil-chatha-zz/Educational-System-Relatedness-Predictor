#!/usr/local/anaconda/bin/python
# Basil Chatha

# I certify that the entirety of this file contains only my own
# work. I also certify that I have not shared the contents of this
# file with anyone in any form.
import csv
from math import sqrt

######################################################################
# We'll represent vectors as lists of numbers; we'll define the vector
# class as a specialization of list so that we can handle
# normalization and dotproduct.

# This class is a bit odd, because I want to show off an argument
# handling trick. We'll make the vector constructor different from the
# list constructor by grouping all the arguments given into a new
# list. This means vector(1,2,3,4) will return a 4-element vector
# <1,2,3,4>, even though list(1,2,3,4) does not (the correct form is
# list([1,2,3,4]), which returns [1,2,3,4]). This isn't necessarily a
# good idea, but grouping multiple remaining arguments with the *args
# construct is a good trick to know about.

# Also, I use zip() to "sew" to lists together, element by element, so
# zip([1,2,3],[4,5,6]) yields a zip object that looks internally like
# [(1, 4), (2, 5), (3, 6)]. To unzip: zip(*zip([1,2,3],[4,5,6])).
# Note zip() is handy for transposing matrices!
class Vector(list):
    def __init__(self, *args):
        '''Constructor invokes list constructor on the collection of args given.'''
        list.__init__(self, list(args))

        # Make Vector's printed representation look pretty.
    def __repr__(self):
        '''Replace standard list brackets with angle brackets.'''
        S = list.__repr__(self)
        return('<{0}>'.format(S[1:len(S)-1]))

    def magnitude(self):
        '''Returns scalar magnitude of self.'''
        return(sqrt(sum( [ val*val for val in self ])))

    def normalize(self):
        '''Normalize self to unit magnitude.'''
        mag = self.magnitude()
        if mag > 0:
            for i in range(len(self)):
                self[i] = self[i]/mag

    # Note use of zip() to simplify the code.
    def dproduct(self, other):
        '''Dot product of self and another vector.'''
        return(sum([ pair[0]*pair[1] for pair in zip(self,other) ]))

    def edistance(self, other):
        '''Euclidean distance of self and another vector.'''
        other.normalize()
        self.normalize()
        #normalize the other vectord including self just as a safegaurd
        return(sqrt(sum([(pair[0] - pair[1])**2 for pair in zip(self, other)])))
        #return the implementation of a euclidean distance formula

######################################################################
class Dataset():
    def __init__(self, codefile='./DataFiles/codes.csv', defnfile='./DataFiles/defn.csv', datafile='./DataFiles/data.csv'):
        self.readCodes(codefile)
        self.readData(datafile)
        self.readDefinitions(defnfile)
        #run readCodes, readData, and readDefinitions and make them attributes of the dataset object

    def readDefinitions(self, defnfile):
        self.D = {}
        # Open the filename for reading.
        with open(defnfile, newline='', encoding='latin-1') as file:
            # Use csv reader.
            reader = csv.reader(file)
            # Skip the header!
            next(reader)
            # Process each row.
            for row in reader:
                self.D[row[0]] = row[1:2]
                # Ugly fix for badly formatted World Bank file where
                # double quotes in string were not properly escaped.
                self.D[row[0]].append(' '.join([ x.rstrip('"') for x in row[2:-1] ]).rstrip('"'))
                self.D[row[0]].append(row[-1])

    def readCodes(self, codefile):
        self.C = {}
        #open filename for reading
        with open(codefile, newline='', encoding='latin-1') as file:
            #use csv reader
            reader = csv.reader(file)
            #skip the header
            next(reader)
            #process each row
            for row in reader:
                self.C[row[0]] = (row[1], row[2])
                #make the keys the country codes and their values tuples of country and regiions

    def readData(self, datafile):
        self.V = {}
        self.P = {}
        # Open the filename for reading.
        with open(datafile, newline='', encoding='latin-1') as file:
            # Use csv reader.
            reader = csv.reader(file)
            # Skip the header!
            next(reader)
            # Process each row.
            for row in reader:
                if len(row[1]) != 0:
                    # Skip lines with missing values.
                    if row[4] != '..' and row[1] in self.C:
                        # Add to V as appropriate.
                        if row[3] not in self.V:
                            #if the variable is not already in V make it with country codes with associated values
                            self.V[row[3]] = { row[1]:row[4] }
                        else:
                            self.V[row[3]][row[1]] = row[4]
                            #otherwise add the country code and associated value to the already-made variable in V
            for key1 in self.V.keys():
                self.P[key1] = len(self.V[key1])
                #make P a dict of each variable and its associated frequency
            for variable in self.V.keys():
                #for every variable in V
                if int(self.P[variable]) >= 1:
                    #if their is 1 or more countries in the variable
                    S = sum([float(x) for x in self.V[variable].values()])
                    Avg = S/len(self.V[variable])
                    #find the average
                    if self.P[variable] == 1:
                        variance = 0
                        #set variance to 0 if only one country is present
                    else:
                        variance = sum([(float(country)-Avg)**2 for country in self.V[variable].values()])/(len(self.V[variable].values())-1)
                        #otherwise find the variance according to the variance equation described in the project discription and on wikihow
                    ssd = sqrt(variance)
                    #find the standard deviation: the square root of variance
                for country in self.V[variable]:
                    #for every country in each variable
                    if int(self.P[variable]) <= 1 or ssd == 0.0:
                        self.V[variable][country] = 0
                        #if 0 countries have the variable or the standard deviation is 0, change the country's value to 0
                    else:
                        zScore = (float(self.V[variable][country]) - Avg)/ssd
                        self.V[variable][country] = zScore
                        #otherwise change the country's value to its zScore by turning its original value into a float,
                        #subtracting the average for the variable, and dividing by the standard deviation


######################################################################
class Analysis():
    def __init__(self, D, j=5):
        self.U = {}
        sU = {}
        #a temporary U var
        self.E = {}
        self.D = D
        sE = {}
        #a temporary E var
        maxs = []
        #list of most common variables
        mostCommonVars = sorted(D.P.values())
        mostCommonVars.reverse()
        #sorted list in descending order of variable frequency
        for i in range(j):
            #for each dimension
            for key in D.P:
                #go through each key in P
                if D.P[key] == mostCommonVars[i] and key not in maxs:
                    maxs.append(key)
                    break
                    #find the top j most common vars and put them in maxs
        for countryCode in D.C:
            #for every countryCode in C
            for variable in maxs:
                #go through every variable in maxs
                if countryCode not in sU:
                    sU[countryCode] = Vector()
                    #if the code isnt in sU, make a new vector object
                if countryCode in D.V[variable]:
                    sU[countryCode].append(D.V[variable][countryCode])
                    #if the country code is in V[variable], append its zscore
                else:
                    sU[countryCode].append(0)
                    #otherwise append 0US
            if sU[countryCode].magnitude() != 0.0:
                sU[countryCode].normalize()
                self.U[countryCode] = sU[countryCode]
                #only add the vector to U if it doesn't have a magnitude of 0
        for country in D.C:
            #for every country in C
            self.E[country] = []
            sE[country] = []
            #add a key to the E dict and sE
            for key in self.U:
                #for every key in U
                if key != country and country in self.U:
                    sE[country].append((self.U[country].edistance(self.U[key]), key))
                    #if the key isn't the country and its in U add a tuple of the country's distance
                    #from the key and the key's name
            sortsE = sorted(sE[country], key=lambda tup:tup[0])
            #sort the list of tuples by distance in ascending order
            self.E[country] += sortsE
            #add the sorted list of tuples to the country's value in E
    def KNN(self, target, k=5):
        return([(self.E[target][i])+(self.D.C[self.E[target][i][1]]) for i in range(k)])
        #return a list of tuples of the top k closest countries to the target in j dimensions
        #and each of their respective associated information


def main():
    import re
    x = Dataset()
    y = Analysis(x)
    run = 1
    while run:
        country = input('Please input country code: ').upper()
        print(y.KNN(country))
        cont = input('Continue? ').lower()
        if not re.search('tru[e]*',cont):
            run = 0

if __name__ == '__main__':
    main()
