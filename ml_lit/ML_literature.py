# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%load_ext autoreload
%autoreload 2

import ml_lit_anal as ml
import re
import nltk
import pickle
import operator
import google_scholar_parser as gs
import pandas as pd
import networkx as nx
import itertools
import matplotlib.pyplot as plt
import numpy as np

# <markdowncell>

# ## A generative model of the machine learning literature
# 
# "Let's build a generative model of the machine learning literature" Andrew Ng, lecture on GDA and Naive Bayes
# 
# The idea of this analysis is to show how machine learning relates to various scientific and technical fields. In its treatment of the literature, it draws both on citation analysis techniques developed  in various fields, as well as text mining, social netowrk analysis and indeed machine learning itself to explore this rather large literature. 

# <markdowncell>

# ## Fields of research in the literature
# 
# I downloaded from Thomson ISI Web of Science all the references returned by the query 'machine learning.' I also downloaded the cited references. 
# 
# Other possible queries such as 'data mining' return too many references to handle -- over 2 million, so I stuck with machine learning, which return aroudn 25,000 references.

# <codecell>

df = ml.load_records('data/')
print('There are %s records in the dataset'%df.shape[0])

#actually this is more about fields than topics
df['fields'] = df.SC.dropna().str.lower().str.split('; ')

all_fields = sorted([e  for el in df.fields.dropna() for e in el])
fields_set = set(all_fields)
field_counts = {e:all_fields.count(e) for e in fields_set}

# <markdowncell>

# Many different fields of research or disciplines are included in the results, and they help make sense of the multi-disciplinary nature of machine learning techniques. 

# <codecell>

print('%s different fields appear in the machine learning literature'%len(fields_set))
field_counts_s = sorted(field_counts.iteritems(), key=lambda(k,v):(-v,k))
field_counts_s[0:30]

# <markdowncell>

# The literature does reach back into the 1950s, but the real growth is in the 1990s-2000s. From 2005 onwards, several thousand publications a year appear.
# 
# We can see also the distribution of fields. Computer science totally dominates the fields. That only goes to show perhaps that machine learning is a computer science-driven set of techniques. But other fields such as automation and control systems,  biochemistry/molecular biology, management science, robotics, telecommunications and imaging science are important components. This already shows something of the wide dissemination of machine learning techniques. 

# <codecell>

#the problem is that computer science clutters everything -- get rid of it?

figure(figsize=(10,12))
subplot(1,2,2)

hist(df.PY, bins=100, alpha=0.6, label= 'Machine Learning Publications by Year')
subplot(1,2,1)
#this doesn't work -- TBA
major_fields = {f:v for f,v in field_counts.iteritems() if v > 3 or f is not 'computer science'}
print(len(field_counts), len(major_fields))
heights = major_fields.values()
ind= np.arange(len(heights))
plt.barh(ind, heights)
width =0.2
plt.title('Machine Learning Publications by Discipline')
xticks = plt.yticks(ind+width/2., major_fields.keys() )

# <markdowncell>

# On

# <codecell>


#bar(height=field_counts.values()[0:100])
#bar(left=range(1, len(field_counts.keys())), height=field_counts.values(), label='Machine Learning Publications by Discipline')

# <codecell>

gr_f = nx.DiGraph()
gr_f.add_edges_from([i for de in df.fields.dropna() for i in itertools.combinations(de,2)])

# <codecell>

evc = nx.centrality.eigenvector_centrality(gr_f)
[ (k,v) for (k,v) in sorted(evc.iteritems(), key=lambda(k,v):(v,k), reverse=True) if v >0]

# <codecell>

gr_f.out_degree(['biochemistry & molecular biology'])

# <codecell>

gr_f.out_degree('automation & control systems')

# <codecell>

degf = [deg for deg in gr_f.degree_iter()]
degf.sort(key = lambda x: x[1], reverse=True)
degf

# <codecell>


g2f = gr_f.copy()
d = nx.degree(g2f)
remove = 14
[g2f.remove_node(n) for n in g2f.nodes() if d[n] <= remove]
g2f.remove_node('computer science')
g2f.remove_node('engineering')
g2f.size()

# <codecell>

figure(figsize=(10,10))
nx.draw_spring(g2f, dim=3, k=1, float=0.2, alpha=0.4)

# <codecell>

figure(figsize=(13,10))
nx.draw_spectral(g2f, alpha=0.5)

# <codecell>

nx.write_gexf(g2f,'fields.gexf')

# <markdowncell>

# ## Authors in ML literature
# 

# <codecell>

df.af = df.AF.dropna().str.lower().str.strip()
df.af = df.af.str.split('; ')
af_all = [d for de in df.af for d in de if d is not nan]
af_set = set(af_all)
print "There %s authors listed and unique authors number %s" % (len(af_all), len(af_set))

# <codecell>

af_counts = {de:af_all.count(de) for de in af_set}

# <codecell>

af_counts_sorted = sorted(af_counts.iteritems(), key = operator.itemgetter(1), reverse=True)
af_counts_sorted[0:50]

# these still need cleaning -- can see some duplicates

# <codecell>

#To check out some of these

sq =gs.ScholarQuerier(author = 'Ross D King', count=50)
sq.query('')
print({a['title']:a['num_citations'] for a in sq.articles})
{a['title']:a['url'] for a in sq.articles}

# <markdowncell>

# There are some interesting differences here:
# 
#    -  Klaus Mueller works on medical decisions
#    -  dzeroski works on induction
#    -  zhou, zhi-hua at nanjing works on facial recognition
#    - Ross King works on synthetic biology and proteins

# <markdowncell>

# ## The techniques and topics in the literature
# 
# This relies on the 'DE' in the Web of Science records

# <codecell>

# topics seem to be in the DE field
df['topics'] = df.DE.dropna().str.lower().str.strip()
df.topics = df.topics.str.replace('s;', ';')
df.topics = df.topics.str.replace('s$', '')
df.topics = df.topics.str.replace('svm', 'support vector machine')
df.topics = df.topics.str.split('; ')

de_all = [d for de in df.topics.dropna() for d in de]
# need to clean out plurals
de_set = set(de_all)
print "All topics has %s and unique topics number %s" % (len(de_all), len(de_set))

# <codecell>

de_counts = {de:de_all.count(de) for de in de_set}

# <codecell>

# to see how topics are distributed

de_counts_sorted = sorted(de_counts.iteritems(), key = operator.itemgetter(1), reverse=True)
de_counts_sorted[0:50]

# <markdowncell>

# # Linking fields and topics
# 
# Can we link topics to fields?
# 
# ## Idea A: use networks
# 
# 1. clean up fields so each publication has the most distinctive fields - remove 'computer science'
# 2. clean up topics so that each publication has the most distinctive topics -- remove 'machine learning'
# 3. create bimodal network of fields & topics?
# 
# ## Idea B: use association/correlations

# <codecell>

# to create distinctive topics, drop machine learning
ftdf = df[['fields', 'topics']]
print(ftdf.shape)
ftdf.head()

# <codecell>

gr = nx.Graph()
gr.add_nodes_from(de_set)
gr.number_of_nodes()
#[i for i in itertools.combinations(de, 2) for de in df.topics[:100]]
gr.add_edges_from([i for de in df.topics.dropna()[0:200] for i in itertools.combinations(de,2)])

# <codecell>

gr2 = nx.Graph()
[gr2.add_edge(f[0],t[0]) for f,t in zip(ftdf.fields, ftdf.topics)]

# <codecell>

gr.number_of_edges()
nx.average_degree_connectivity(gr)
#nx.draw_networkx(gr)

# <codecell>

gr.remove_node('machine learning')

# <codecell>

deg=nx.degree(gr)

# <codecell>

deg['support vector machine']
deg_sorted = sorted(deg.iteritems(), key=lambda(k,v):(-v,k))
deg.values()[:50]

# <codecell>

deg_sorted[0:10]

# <codecell>

h=hist(deg.values(), 100)
loglog(h[1][1:], h[0])

# <codecell>

#remove 1-degree nodes

g2 = gr.copy()
d = nx.degree(g2)
remove = 10
[g2.remove_node(n) for n in g2.nodes() if d[n] <= remove]
g2.size()

# <codecell>

figure(figsize=(10,10))

nx.draw_networkx(g2, alpha=0.8)
nx.

# <markdowncell>

# # 2 mode networks: disciplines and techniques

# <codecell>

from networkx.algorithms import bipartite as bi

# <codecell>

tx = ml.discipline_techniques_graph(df)

# <codecell>

tx.size()
disciplines = df.SC_l.unique()
techniques = {det  for de in df.DE_l if de is not nan for det in de}
print ('

# <codecell>

df.SC_l

# <codecell>

disc = bi.projected_graph(tx, disciplines)

# <markdowncell>

# ## Retrieving further literature if needed from WoS

# <codecell>


# <codecell>


# <codecell>


# <codecell>


# <codecell>

## generate searches that can be run back against WoS

'"'+'" or "'.join([de for de,val in de_counts_sorted if val > 90 and val < 200]) + '"'

# <markdowncell>

# ## Building a topic model

# <codecell>

# <markdowncell>

# # The corpus of ML

# <codecell>

ti_ab = df.TI + df.AB
mlt = nltk.TextCollection([nltk.tokenize.word_tokenize(t) for t in ti_ab.dropna()])

# <markdowncell>
mlt.tokens[0:20]

# <markdowncell>

# ## The cited references

# <codecell>

df.NR.value_counts()

