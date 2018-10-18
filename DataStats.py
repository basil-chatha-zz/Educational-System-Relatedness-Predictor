# Basil Chatha
# I certify that this is all my work
import csv
import numpy as np
import matplotlib.pyplot as plt

def readDefinitions(filename='./DataFiles/data.csv'):
    with open(filename) as csvfile: #open file
        reader = csv.DictReader(csvfile, fieldnames = ('Code', 'Indicator Name', 'Long definition', 'Source'))
        #tell the reader what the header columns are
        D = {row['Code']:[row['Indicator Name'],row['Long definition'], row['Source']] for row in reader if row['Code'] != 'Code' and row['Code'] != '\ufeffCode'}
    return(D)
    #return a dictionary of the code as the key, and a list of the indicator name,
    #long definition, and source making sure to skip the first line
def readData(filename='./DataFiles/data.csv'):
	C, V = {}, {}
	reader = csv.DictReader(open(filename), fieldnames = ('Country', 'Country Code', 'Series', 'Series Code', '2015 [YR2015]'))
	#open file with correct column headers
	for row in reader:
		if row['Country Code'] == 'Country Code' or row['Country Code'] == '':
			continue
            #if the first or last five lines, skip to the next iteration
		if row['Country Code'] not in C: #if the country code isn't in C, add it to it
			C.update({row['Country Code']: row['Country']})
            #update c to match country codes with their respective countries
		if row['Series Code'] not in V and row['2015 [YR2015]'] != '..':
            #if the series code of the row isn't already in v and the last column of the data file isn't empty
			V[row['Series Code']] = {row['Country Code'] : row['2015 [YR2015]']}
            #add the country code with its 2015 [YR2015] value to its matching series code
		elif row['Series Code'] in V and row['2015 [YR2015]'] != '..':
            #otherwise if the series code is in v and the last column of the data file isn't empty
			V[row['Series Code']].update({row['Country Code']: row['2015 [YR2015]']})
            #update the value of the series code to include the new country code and its 2015 [YR2015] value
	return(C, V)
def makeProfiles(C, V):
    P = {}
    for code in V:
        for country in V[code]:
            #for every series code in v, go through its keys which should be countries
            if country not in P:
                P.update({country:1})
                #if the country isn't in P, make a new key value pair for it, initilizing it as 1
            else:
                P[country]+=1
                #if the country is already in P, add one to its value in P
    ctoremove = set(C.keys()) - set(P.keys())
    # do a set difference to get the keys with 0 as values in a variable and remove them from P
    for eachcountry in ctoremove:
        del(C[eachcountry])
        #for each 0 value in C, remove it
    return(P)
def plotProfile(P):
    yvalues = [P[x] for x in sorted(P.keys())]
    #make a list of the y values for the bar graph making sure to sort the countries alphabetically
    plt.title("Country Profiles")
    plt.xlabel("Country Code")
    plt.ylabel("Data Available")
    #create the title, x and y labels for the bar graph
    plt.bar(np.arange(len(yvalues)), yvalues)
    #make the bar graph with the correct range of yvalues to make a well-scaled graph, and the actual y values
    plt.xticks(np.arange(len(yvalues)), sorted(P.keys()), rotation = 90, fontsize = 5)
    #rotate the xlabels 90 degrees and make their font size 5
    plt.show()
    #show the graph

def main():
    dataReader = readData()
    profileMaker = makeProfiles(dataReader[0], dataReader[1])
    plotProfile(profileMaker)

if __name__ == '__main__':
    main()
