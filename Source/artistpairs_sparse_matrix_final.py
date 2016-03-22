#!/usr/bin/python

import csv # For parsing .csv file
import numpy as np # For matrices
import scipy.sparse as spa # For sparse matrices

ARTIST_FILE_NAME = "ArtistList.csv"
MIN_COUNT = 50

# Open the file and turn it into a favesList, which is a list of lists where the outer list is the list of listeners, and the inner list is each listener's favorite artists
with open(ARTIST_FILE_NAME, "rb") as csvFile:
    reader = csv.reader(csvFile)
    favesList = list(reader)

# assign each artist an ID

# Make a first pass to count up each artist's number of occurrences. We can throw out any artists that occur less than MIN_COUNT times, because they cannot possibly be part of a pair that occurs at least MIN_COUNT times.
artistCountMap = {}

for listenerList in favesList:
	for artist in listenerList:
		if artist not in artistCountMap:
			artistCountMap[artist] = 1
		else:
			artistCountMap[artist] = artistCountMap[artist] + 1

# Now we can work in a reduced space of artists who occur at least MIN_COUNT times. Assign each of these artists a unique ID.
reducedArtistID = 0
artistMap = {}

# Iterate through the input again, inserting each artist who occurs at least MIN_COUNT times into artistMap, which is a map where key = artist and value = the artist's unique ID.
for listenerList in favesList:
	for artist in listenerList:
		if artistCountMap[artist] >= MIN_COUNT:
			if artist not in artistMap:
				artistMap[artist] = reducedArtistID
				reducedArtistID = reducedArtistID + 1

# Now create an array where each each index is an artist's ID and the entry at that index is the artist with that ID. 
artistIDs = [0] * reducedArtistID
for artist, aID in artistMap.iteritems():
	artistIDs[aID] = artist

# Now we have a mapping from reduced artists -> IDs (artistMap), and from IDs -> reduced artists (artistIDs)

numListeners = len(favesList)

# Build a matrix where each row represents a listener and each column represents an artist. The entry at artistMatrix[A,B] = 1 if listener A likes artist B, and 0 if not. 
artistMatrix = spa.dok_matrix((numListeners, reducedArtistID), dtype=np.int32)

for i, listenerList in enumerate(favesList):
	for artist in listenerList:
		if artistCountMap[artist] >= MIN_COUNT:
			artistMatrix[i, artistMap[artist]] = 1

# Compress the matrix into a suitable sparse matrix representation, which in this case is the COOordinate format.
artistMatrix = artistMatrix.tocoo()

# Now we multiply the transpose of the artistMatrix with itself. The result will be a matrix of size reducedArtistCount x reducedArtistCount. 

# In this product matrix, each row represents an artist and each column represents an artist. The entry at matrixProduct[A,B] = the number of times artists A and B were listed together by the same listener.
matrixProduct = (artistMatrix.T).dot(artistMatrix)

# The entries in the diagonal of the matrixProduct represents the total number of times the corresponding artist was listed; e.g. matrixProduct[A,A] = total number of times artist A was listed. 

# We don't need this information, nor do we need the information in the bottom half of the triangle since the matrixProduct is symmetrical across the diagonal.

# Let's use the triu() function to take just the upper triangle of the matrixProduct, excluding the diagonal.
upperTriangle = spa.triu(matrixProduct, 1)

# In the upper triangle of the matrixProduct, find all the entries that have a count of at least MIN_COUNT.
indicesOfHighFreqPairs = spa.find(upperTriangle >= MIN_COUNT)

# Iterate through the results and print them out.
rows = indicesOfHighFreqPairs[0]
columns = indicesOfHighFreqPairs[1]

for i in xrange(0, len(rows)):
	if artistIDs[rows[i]] > artistIDs[columns[i]]:
		print artistIDs[columns[i]] + "," + artistIDs[rows[i]]
	else:
		print artistIDs[rows[i]] + "," + artistIDs[columns[i]]

