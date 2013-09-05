# %load_ext autoreload
# %autoreload 2


import pandas as pd
import re
import os
import matplotlib
import pickle
import datetime
import networkx as nx
import numpy as np
import operator

def load_records(dir):
	"""Return dataframe of all records, with new column of cited references as list"""

	# I saved all the WoS full records for 'machine learning'
	files =os.listdir(dir)
	df =pd.concat([pd.read_table(df, sep='\t',index_col = False) for df in [dir+f for f in files]])
	df = df.drop_duplicates()

	#fix index
	index = range(0, df.shape[0])
	df.index = index

	#to get all cited refs
	cited_refs = [set(re.split(pattern='; ', string=str(ref).lower().lstrip().rstrip())) for ref in df.CR]

	# add as column to dataframe
	df['cited_refs'] = cited_refs

	# normalise authors
	df.au = [str(au).lower().lstrip().rstrip() for au in df.AF]

	return df


def clean_topics(df):
	
	"""Wos.DE field has a mixture of topics and techniques.
	-------------------------------------
	Returns a cleaned-up, de-pluralised list version of all the topics and techniques
	"""

	df['topics'] = df.DE.dropna().str.lower().str.strip().str.replace('\(\\w+ \)', '').str.replace('($  )|(  )', ' ')
	# df.topics = df.topics.str.replace('s;', ';')
	# df.topics = df.topics.str.replace('s$', '')
	df.topics = df.topics.str.replace('svm', 'support vector machine')
	df.topics = df.topics.str.replace('artificial neural network', 'neural network')
	df.topics = df.topics.str.replace('neural networks', 'neural network')

	df.topics = df.topics.str.split('; ')
	return df

def keyword_counts(df):

	""" Returns a dictionary with keyword counts"""
	
	de_all = [d for de in df.topics.dropna() for d in de]
	de_set = set(de_all)
	de_counts = {de:de_all.count(de) for de in de_set}
	return de_counts


def manual_topic_classifier(df, existing_topic_classes, topic_counts_sorted, start = 0, count=100, ):
	
	"""Returns a dictionary with topics classified as techniques
	or not. Asks the user to classify them by hand, starting with the most frequent
	Parameters
	------------------
	count: how many to classify
	start: where in the list to start
	"""

	if existing_topic_classes is None:
		existing_topic_classes = dict()
	if topic_counts_sorted is None:
		de_all = [d for de in df.topics.dropna() for d in de]
		de_set = set(de_all)
		de_counts = {de:de_all.count(de) for de in de_set}
		topic_counts_sorted = sorted(de_counts.iteritems(), key = operator.itemgetter(1), reverse=True)
	topic_classes = {t:raw_input('\n' + t+ ' is technique? ') for t,v in topic_counts_sorted[start:start+count] if not existing_topic_classes.has_key(t)}
	existing_topic_classes.update(topic_classes)
	return existing_topic_classes


def coword_matrix(df, keys):

	""" Implementation of Callon style co-word analysis of  the 
	Wos DE field -- the keywords field in the database
	
	Parameters
	------------------------------------------------
	df: the WoS literature DataFrame
	keys: keywords to use
	"""

	topics = df.topics
	


	# create document term matrix of keywords
	topics = topics.dropna()
	cow = np.zeros((len(topics), len(keys)))

	# hate doing these nested for loops but I couldn't get the list comprehensions working properly
	for row in range(0,len(topics)):
		top = topics.iget(row)
		hits = list()
		for t in top:
			if keys.count(t) >0:
				hits.append(keys.index(t))
		cow[row, hits] = 1
	#to create coword matrix
	cow_m = np.dot(np.transpose(cow), cow)
	cow_df = pd.DataFrame(cow_m, columns=keys, index=keys)
	return cow_df

def inclusion_score(cow_df, key1, key2, de_counts):
	""" Calculates  the inclusion score (conditional probability?) of key1
	given the presence of key2 (or vice versa)"""

	c_ij = cow_df[key1][key2]
	I_ij = c_ij/min(de_counts[key1], de_counts[key2])
	return I_ij

def proximity_score(cow_df,key1, key2, de_counts, article_count):
	""" Calculates  the equivalence score (mutual inclusion) of key1
	given the presence of key2 (or vice versa)"""

	c_ij = cow_df[key1][key2]
	p_ij = c_ij/(de_counts[key1] * de_counts[key2]) * article_count
	return p_ij
2
def equivalence_score(cow_df, key1, key2, de_counts):
	""" Calculates  the equivalence score (mutual inclusion) of key1
	given the presence of key2 (or vice versa)"""	

	c_ij = cow_df[key1][key2]
	E_ij  = c_ij**2/(de_counts[key1] * de_counts[key2])
	return E_ij

def equivalence_matrix(cow_df, de_counts):
	""" Constructs the equivalence matrix for all combinations of key words; 
	This is following (Callon, 1991).

	Parameters
	---------------------------------------------------------------- 
	cow_df: the matrix of co-word counts
	de_counts: the list of keyword counts
	"""

	keys = cow_df.columns.tolist()
	key_combinations = [(k1,k2) for k1 in cow_df.columns for k2 in cow_df.index if k1 != k2]
	ecow = np.zeros(cow_df.shape)
	for kc in key_combinations:
		key1, key2 = kc
		i1 = keys.index(key1)
		i2 = keys.index(key2)
		sc = equivalence_score(cow_df, key1, key2, de_counts)
		ecow[i1,i2] = sc

	eqcow_df = pd.DataFrame(ecow, columns=cow_df.columns, index = cow_df.index)
	return eqcow_df

def discipline_techniques_graph(df):

	""" Constructs a bipartite graph from techniques to discipline_techniques_graph.
	It assumes that dataframe already has a cleaned up topics field.
	Preferably it has already been cut down just to techniques
	------------------------------
	Returns graph
	"""

	df['SC_l'] = df.SC.str.lower()

	tg = nx.DiGraph()
	[tg.add_edge(te, f) for t,f in zip(df.topics, df.SC_l) if t is not np.nan  for te in t]
	return tg

def trim_degrees(g, degree=1):
	g2 = g.copy()
	d = nx.degree(g2)
	[g2.remove_node(n) for n in g2.nodes() if d[n] <= degree]
	return g2

def sorted_map(map): return sorted(map.iteritems(), key=lambda (k,v): (-v,k))

def trim_edges(g, weight=1):
    g2 = nx.Graph()
    [g2.add_edge(f,to, edata) for f, to, edata in g.edges(data=True) if edata['weight']>weight]
    return g2

def island_method(g, iterations=5):
    weights = [edata['weight'] for f, to, edata in g.edges(data=True)]
    mn = int(min(weights))
    mx = int(max(weights))
    step = int((mx-mn)/iterations)
    return [[threshold, trim_edges(g, threshold)] for threshold in range(mn,mx,step)]