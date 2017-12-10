
from collections import defaultdict

import datetime, time, os, pickle, sys

import numpy as np
import matplotlib.pyplot as plt

logline = []

# converts HH:MM:SS to seconds after extracting it from a message passed in as the argument
def tosecs(x):
	hms = x.split()[3][11:-6].split(':')
	hms = [int(a0) for a0 in hms]
	return 3600*hms[0] + 60*hms[1] + hms[2]

# outputs stored value of plotted point to terminal if said point is clicked
def onpick(event):
	ind = event.ind
	print('\nonpick scatter : ', ind, np.take(logline, ind))

# run this file by typing python3 insight.py patterns logdata
# $python3 insight_v2.py /path/to/file/containing/keywords /path/to/directory/containing/logfiles
# patterns is a text file containing the list of search terms
# logdata contains rawfiles, logdata.cluster and logdata.filter
regex_list    = sys.argv[1]
log_directory = sys.argv[2]+'/'

log_subdirectory = os.listdir(log_directory)
print(log_subdirectory)
log_subdirectory = [x for x in os.listdir(log_directory) if os.path.isfile(log_directory+x)]
log_subdirectory.sort(key = lambda x: datetime.date(*(int(x[:4]), int(x[4:6]), int(x[6:]))))
print(log_subdirectory)

cluster_path = (log_directory+'//'+ log_directory[:-1] + '.cluster/')
os.makedirs(cluster_path, exist_ok = True)

# saves the search terms in 'patterns' to a list
with open(regex_list, 'r') as regexes:
	regexparams = [line.replace("\n", "") for line in regexes]
	regexparams = [line for line in regexparams if line != ""]

# searches for the terms in patterns
def keyword_search(message):
	hits = [rgxpm for rgxpm in regexparams if rgxpm in message]
	if hits == []:
		return False
	else:
		return True

for logfile in log_subdirectory:

	with open(cluster_path+logfile+'.pkl', 'rb') as cluster_dict:
		clusters = pickle.load(cluster_dict)

	timestamps = []
	relevances = []
	# array of random colours
	colorpool  = np.random.random(len(clusters.keys()))
	colors     = []
	colorpool_tracker = 0
	logline    = []

	for k, v in clusters.items():
	
		# if there are more than 100 messages
		if len(v) > 100:
			timestamp_local = []
			for i in v:
				# some messages don't confirm to the format like the last line in some file mentioning a ZAP ERROR
				# the try catch is for these lines, which barely if ever, occur
				try:
					if keyword_search(i):
						# stores x coordinates of each plotted point within a cluster
						timestamp_local.append(tosecs(i))
						# stores the message which will be displayed if a point is clicked
						logline.append(i)
				except ValueError:
					pass
			# adds y coordinates of the new cluster to a list
			relevances.extend([len(timestamp_local) for i in timestamp_local])
			# stores the colours for the new cluster in the list storing colours for all plotted points
			colors.extend([colorpool[colorpool_tracker] for i in timestamp_local])
			# adds x coordinates of the new cluster to a list
			timestamps.extend([i for i in timestamp_local])
			colorpool_tracker += 1

	# area of the circles being plotted
	areas = np.array([100 for i in timestamps])
	# timestamps in seconds - the x axis
	timestamps = np.array(timestamps)
	# relevance - the y axis
	relevances = np.array(relevances)
	
	fig, ax = plt.subplots()
	# log of occurences to the base 2
	col = ax.scatter(timestamps, np.log2(relevances), s=areas, c=colors, alpha=0.5, picker=True)
	fig.canvas.mpl_connect('pick_event', onpick)

	plt.savefig(cluster_path + logfile, dpi=300) # can be used to save the image at required dpi
	plt.show()	

	'''
	# plots a histogram of how many messages were emitted for each second of the day
	# or rather, slices the day into 'bins' number of segments and the height of each bar is the 
	# number of messages emitted in that frame of time.

	plt.hist(timestamps, bins=4000, align='mid')
	plt.savefig('logfile_hist', dpi=300)
	'''



'''

for each plotted point

the x coordinate is the time in the day when the event occured; in seconds ranging from 0 to 86400

the y coordinate indicates how many times a structurally similar sentence was found in the log file

the y axis has been scaled logarithmically with respect to base 2

'''




















