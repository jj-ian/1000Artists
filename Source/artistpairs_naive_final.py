#!/usr/bin/env python

import csv # For parsing .csv file

ARTIST_FILE_NAME = "ArtistList.csv"
MIN_COUNT = 50

# Open the file and turn it into a favesList, which is a list of lists where the outer list is the list of listeners, and the inner list is each listener's favorite artists
with open(ARTIST_FILE_NAME, "rb") as csvFile:
    reader = csv.reader(csvFile)
    favesList = list(reader)

# Assign each artist an ID
uniqueArtists = 0
artistMap = {}

# Iterate through input and insert each artist into artistMap, which is a map where key = artist and value = the artist's unique ID
for listenerList in favesList:
	for artist in listenerList:
		if artist not in artistMap:
			artistMap[artist] = uniqueArtists
			uniqueArtists = uniqueArtists + 1

# Map of pairs, where key = pair and value = the number of times the pair occurs together
pairMap = {}

for listenerList in favesList:
	# Enumerate each pair in each listener's list 
	for i in xrange(0, len(listenerList)):
		for j in xrange(i+1, len(listenerList)):
			artist1 = listenerList[i]
			artist2 = listenerList[j]

			# Sort the pair alphabetically so (Artist1, Artist2) is the same as (Artist2, Artist1)
			artistPairList = sorted([artist1, artist2])
			artistPair = (artistPairList[0], artistPairList[1])

			# Increment each pair's count in the pairMap
			if artistPair not in pairMap:
				pairMap[artistPair] = 1
			else:
				pairMap[artistPair] = pairMap[artistPair] + 1


results = []

# Iterate through pairmap, find all pairs that occur more than MIN_COUNT number of times, and add every such pair to the results list
for pair, count in pairMap.iteritems():
	if count >= MIN_COUNT:
		results.append((count, pair))

# Print the results in CSV format
for (count, pair) in results:
	print pair[0] + "," + pair[1]






