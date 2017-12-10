
#imports dependencies for the hunpos tagger
import nltk
from nltk.tag.hunpos import HunposTagger
from nltk.tokenize import word_tokenize

#datastructure used to cluster sentences together
from collections import defaultdict

#for filepaths, runtime of the code, saving the clustering to file using pickle
import datetime, time, os, pickle, sys
import os.path

start_time = time.clock()

# the first commandline argument is the directory containing the log files
log_directory = sys.argv[2]+'/'
regex_list = sys.argv[1]

# this list comprehensions removes the names of any directories contained within log_directory
log_subdirectory = [x for x in os.listdir(log_directory) if os.path.isfile(log_directory+x)]
# log_subdirectory is the list of logfiles that we will iterate over 

# sorting logfiles as per dates of creation
# expects the format for filename to be YYYYMMDD
log_subdirectory.sort(key = lambda x: datetime.date(*(int(x[:4]), int(x[4:6]), int(x[6:]))))
print(log_subdirectory)

#creates logdata.cluster if it doesn't exist, also saves the path to logdata.cluster
cluster_path = (log_directory+'//'+ log_directory[:-1] + '.cluster/')
os.makedirs(cluster_path, exist_ok = True)

# saves the search terms to the list : regexparams
with open(regex_list, 'r') as regexes:
	regexparams = [line.replace("\n", "") for line in regexes]
	regexparams = [line for line in regexparams if line != ""]

# checks if the string passed as argument contains any search terms
# returns either False, or the list of terms which matched
def keyword_search(message):

	hits = [rgxpm for rgxpm in regexparams if rgxpm in message]
	
	if hits == []:
		return False
	else:
		return hits

# initialises the hunpos tagger which requires the binary which will tag sentences and the model it was trained on
# it was pre trained on the en_wsj.model
hunpos_tagger = HunposTagger(path_to_bin='hunpos-1.0-linux/hunpos-tag', path_to_model='hunpos-1.0-linux/en_wsj.model')

for logfile in log_subdirectory:
	
	#if the file has been processed, proceed to the next one 
	if os.path.isfile(cluster_path+logfile+'.pkl'):
		pass

	else:
		with open(log_directory+logfile, 'r') as rsyslog:
			#prints name of current file
			print(logfile)
			#creates datastructure which will store the clusters
			clusters = defaultdict(list)
			#lops of the newline character at the end of every line
			sentences = [line[:-1] for line in rsyslog]
			#loglen stores number of messages/sentences in the logfile
			loglen = len(sentences)
			for sentence, counter in zip(sentences, range(loglen)):
				# decomposing the sentence to a binary string of pos_tags which will serve as the key for the dictionary
				pos_tags  = b''.join([i[1] for i in hunpos_tagger.tag(word_tokenize(sentence))])
				# adding the sentence to the list which is the value that the pos_tag key is mapping to
				clusters[pos_tags].append(sentence)
				# percentage completion of current logfile
				print("Completion : %4.2f%%"%(counter*100/loglen), end="\r")
			print("Completion : 100.00%")
			print()

		# saves the clustering to a pickle file for later processing and visualisation
		with open(cluster_path+logfile+'.pkl', 'wb') as cluster_dict:
			pickle.dump(clusters, cluster_dict)		

end_time = time.clock()
print("Time Elapsed : ", str(end_time-start_time))