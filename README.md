# Structural-Similarity-Clustering

Processes all logfiles in a given directory, using the hunpos tagger to cluster together structurally similar log entries for each indivdual logfile. Pickles the clustering to memory.

On average, takes 150s to cluster 90MB of data on my machine, the result of the process is about 95MB, which consists of all log entries and the defaultdict which helps group them.
