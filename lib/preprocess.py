import re
import json
import codecs
import pandas
import io
import vincent
from collections import Counter
from collections import defaultdict
import operator

import math
import nltk
from nltk.corpus import stopwords

import string
import argparse
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#include :( :{ :[ :/	
emoticon_str=r"""
	(?:
		[:=;]
		[oO\-]?
		[D\)\]\(/\\OpP\[\{]
	)"""

reg_str= [
	emoticon_str,
	r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

punctuation= list(string.punctuation)
stop= stopwords.words('english')+ punctuation+['RT','rt','via','The','This']

dates_hashtag=[]
tokens_re= re.compile(r'('+'|'.join(reg_str)+')',re.VERBOSE|re.IGNORECASE)
emoticon_re=re.compile(r'^'+emoticon_str+'$',re.VERBOSE|re.IGNORECASE)

com=defaultdict(lambda:defaultdict(int))

def get_parser():
	parser=argparse.ArgumentParser(description="Dataset")
	parser.add_argument("-f",
						"--file",
						dest="filename",
						help="Filter",
						default='-')
	return parser

def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

def tokenize(s):
	return tokens_re.findall(s)
	
def preprocess(s,lowercase=False):
	tokens=tokenize(s)
	if lowercase:
		tokens= [token if emoticon_re.search(token) else token.lower() for token in tokens]
	return tokens

def is_ascii(text):
    if isinstance(text, unicode):
        try:
            text.encode('ascii')
        except UnicodeEncodeError:
            return False
    else:
        try:
            text.decode('ascii')
        except UnicodeDecodeError:
            return False
    return True
		
parser=get_parser()
args=parser.parse_args()	
name= "./data/stream__"+args.filename

with codecs.open(name,'r') as f:
	count_all=Counter()
	#n_docs=0
	for line in f:
		tweet=json.loads(line)
		if 'text' not in tweet:
			continue
		#n_docs=n_docs+1
		terms_all=[term.encode('ascii') for term in preprocess(tweet['text']) if term not in stop and is_ascii(term) and not term.startswith(('#','@'))]
		count_all.update(terms_all)
		dates_hashtag.append(tweet['created_at'])
		for i in range(len(terms_all)-1):
			for j in range(i+1, len(terms_all)):
				w1,w2=sorted([terms_all[i], terms_all[j]])
				if w1!=w2:
					com[w1][w2]+=1
		
	print(count_all.most_common(10))

	#most co-occurent terms
	com_max=[]
	for t1 in com:
		t1_max_terms=sorted(com[t1].items(),key=operator.itemgetter(1),reverse=True)[:5]
		for t2, t2_count in t1_max_terms:
			com_max.append(((t1, t2), t2_count))
	terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
	print(terms_max[:5])
	
"""	p_t= {}
	p_t_com=defaultdict(lambda:defaultdict(int))
	#print com
	for term,n in count_all.items():
		p_t[term]=math.log(n,2)-math.log(n_docs,2)
		for t2 in com[term]:
			#print com[term][t2]
			p_t_com[term][t2]=math.log(com[term][t2],2)-math.log(n_docs,2)
	#print p_t_com
	pmi=defaultdict(lambda:defaultdict(int))
	for t1 in p_t:
		for t2 in com[t1]:
			denom=p_t[t1]+p_t[t2]
			if denom!=0:
				pmi[t1][t2] = p_t_com[t1][t2]-denom
				#print p_t_com[t1][t2]
				#print denom
	
	semantic_orientation={}
	for term, n in p_t.items():
		pos_assoc=sum(pmi[term][tx] for tx in positive_vocab)
		neg_assoc = sum(pmi[term][tx] for tx in negative_vocab)
		semantic_orientation[term] = pos_assoc - neg_assoc
	
	semantic_sorted = sorted(semantic_orientation.items(), 
                         key=operator.itemgetter(1), 
                         reverse=True)
	top_pos = semantic_sorted[:10]
	top_neg = semantic_sorted[-10:]
	print("positive")
	print(top_pos)
	print("negative")
	print(top_neg)
	"""