import json
import codecs
import io
from collections import defaultdict
import operator

import time
import string
import json
import math

import string
import argparse

import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('./lib')

import preprocess
import sentiment

"""positive_vocab = [
    'good', 'nice', 'great', 'awesome', 'outstanding',
    'fantastic', 'terrific', ':)', ':-)', 'like', 'love',
    # shall we also include game-specific terms?
    # 'triumph', 'triumphal', 'triumphant', 'victory', etc.
]
negative_vocab = [
    'bad', 'terrible', 'crap', 'useless', 'hate', ':(', ':-(',
    # 'defeat', etc.
]"""

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

match = lambda a, b: [ 1 if x in b else 0 for x in a ]

parser=get_parser()
args=parser.parse_args()	
name= "data/stream__"+args.filename

text_file1=open("./vocab/positive_words.txt","r")
pos_words=text_file1.readlines()
text_file2=open("./vocab/negative_words.txt","r")
neg_words=text_file2.readlines()
positive_words=[p.rstrip() for p in pos_words]
negative_words=[n.rstrip() for n in neg_words] 
text_file1.close()
text_file2.close()

mat=mis=pos=neg=neu=0
with codecs.open(name,'r') as f:
	for line in f:
		tweet=json.loads(line)
		if 'text' not in tweet:
			continue
		terms_all=[term.encode('ascii') for term in preprocess.preprocess(tweet['text']) if term not in preprocess.stop and preprocess.is_ascii(term) and not term.startswith(('#','@'))]
		
		pos_matches=match(terms_all,positive_words)
		neg_matches=match(terms_all,negative_words)

		pos_sum=neg_sum=0
		one=two=-1
		#print pos_matches
		for i in range(len(pos_matches)-1):
			if (pos_matches[i]==1):
				pos_sum=pos_sum+1
		
		for i in range(len(neg_matches)-1):
			if (neg_matches[i]==1):
				neg_sum=neg_sum+1
				
		score_fin= pos_sum-neg_sum
		if score_fin>0:
			pos+=1
			one=1
		elif score_fin<0:
			neg+=1
			one=0
		else:
			neu+=1
			one=0
			
		two=sentiment.sentiment_value(tweet['text'])
		if(one==two):
			mat+=1
		else:
			mis+=1
	"""
	p_t= {}
	p_t_com=defaultdict(lambda:defaultdict(int))
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
	print(top_neg)"""
	
	print "match"
	print mat
	print "miss"
	print mis