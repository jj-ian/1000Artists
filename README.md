1000 ARTISTS CODING CHALLENGE

Julie Chien

# PROBLEM

The attached utf-8 encoded text file contains the favorite musical artists of 1000 users from LastFM. Each line is a list of artists.

Write a program that takes a file or standard input, and produces a list of pairs of artists which appear TOGETHER in at least fifty different lists. For example, in the above sample, Radiohead and Morrissey appear together twice, but every other pair appears only once. Your program should output the pair list to stdout in the same form as the input (eg Artist Name 1, Artist Name 2\n).

# SOLUTION

I implemented 3 different solutions, all in Python. 

1. **Naive solution**

Enumerate every pair per line in the input, counting the occurrences of each pair. The pairs are counted using a map where key = a pair of artists, and value = the number of times that pair occurred together in the input. 

To get the results, iterate through the result map and print all pairs that occur together at least 50 times.

2. **Dense matrix**

Build a matrix where each row represents a listener and each column represents an artist. The entry at matrix[A, B] = 1 if listener A likes artist B, 0 if not. 

Multiply this matrix’s transpose with the matrix itself. The resulting product is a matrix productMatrix where every column and row represents an artist. The entry at productMatrix[A, B] = the number of times artists A and B were listed together.

To get the results, print out all pairs A, B in productMatrix where productMatrix[A, B] >= 50. 

3. **Sparse matrix**

Since there were 11,289 unique artists and each listener liked an average of 45 artists, the data is sparsely concentrated in this dataset. 

This solution is the same as the dense matrix solution, except that I used sparse matrix representations from the SciPy library to represent my matrices. 

Additionally, I made a first pass through the input and threw out any artists that occur fewer than 50 times, because they cannot possibly belong to any pairs in the solution.

# TO COMPILE AND RUN

Note: You must have Python and the csv, numpy, and scipy.sparse libraries. You may have to change the first line of the scripts to wherever your Python is located. Mine was in #!/usr/bin/python.

> cd Source/
> chmod 755 artistpairs_naive_final.py artistpairs_sparse_matrix_final.py

To run the naive solution:

> ./artistpairs_naive_final.py

To run the sparse matrix solution:

> ./artistpairs_sparse_matrix_final.py

Note I did not include the dense matrix solution since it’s the same as the sparse matrix solution, save the libraries used.

# RESULTS

The naive solution took on average 2.959 seconds to complete.

The dense matrix solution took a very long time to complete -- 145 minutes and 44.580 seconds!

The sparse matrix solution was quite fast and completed in **0.549 seconds**. 

Without the additional optimization of throwing out artists that occur less than 50 times, the sparse matrix solution took 1.152 seconds.

# TIME COMPLEXITY

Let A = the number of unique artists and L = the number of listeners.

Let A’ = the average number of artists liked by each listener. A’ is bounded above by A.

Let A’’ = the number of artists that appear at least 50 times.

Let B = the number of pairs of artists that occur together in the dataset. B is bounded above by A2 -- the number of all possible pairs over A artists.

**The naive solution** has a runtime complexity of **O(L****B****)**. This comes from enumerating each pair of artists per listener to insert into the map of pair counts. This part of the algorithm is the bottleneck and dominates the big-O.

LB is bounded from above by LA**2****. **In this dataset, A = 11,289, A2 = 127,441,521, and B = 751,192. Then, LB is much smaller than LA**2** for this dataset.

We can get an even tighter bound: If we assume that there’s not too much variance in the length of the playlists, we can estimate the average-case running time to be O(LA’**2**). Since A’ = 45 in this dataset, this ends up being much smaller than LB and LA**2**, which makes the algorithm run quite quickly for this dataset.

**The dense matrix solution**’s bottleneck is the matrix multiplication, which is **O(LA****2****)** regardless of what the data looks like. This makes the dense matrix solution very slow.

**The sparse matrix solution**’s bottleneck is also the matrix multiplication, which is still **O(LA****2****)**. However, using the sparse matrices in the SciPy library gives us a huge performance boost, due to optimizations like parallelization, caching, and vectorization  that are built into the library’s sparse matrix operations. 

In the sparse matrix solution, I added the additional optimization of removing all artists that appear fewer than 50 times. Then, a tighter bound on the sparse matrix’s runtime is **O(LA’’****2****)**. This combined with SciPy’s optimizations make the sparse matrix solution super fast -- half a second for this dataset.

# SPACE COMPLEXITY

**The naive solution**’s space bottleneck is the map of artist pairs, which is O(B). Since the data is sparse,  O(B) is much smaller than O(A2) for this dataset.

**The dense matrix solution** has a space complexity of O(A2) regardless of the sparsity of the data. The bottleneck is the product matrix which is of size A x A.

**The sparse matrix solution** has a space complexity of O(B). The bottleneck is the product matrix which is of size A’’ x A’’; however, SciPy’s representation of it condenses it to O(B).

# NOTES

1. Bloom filters could be used to improve space complexity.

2. The runtime and space complexities I give assume that maps can be accessed in O(1) time, which would be true if the map was implemented using a hashtable. In languages like Python and C++, maps are implemented using red-black trees, which have O(log n) access time. The runtime of the naive solution, for example, would then be **O(L B log B)**. I chose to gloss over this to focus more on the algorithm instead of the language’s implementation of the data structures.

