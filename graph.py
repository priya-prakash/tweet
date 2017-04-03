import re
import json
import codecs
import pandas
import io
import vincent
from collections import Counter
from collections import defaultdict
import operator

import string
import argparse
import sys
reload(sys)
sys.setdefaultencoding('utf8')

sys.path.append('./lib')
import preprocess

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
	
def freq_bar(count,fname):
	# plotting the bar graph for most frequent terms
	freq_term=count.most_common(10)
	print("Generating bar graphs for 10 most frequent terms")
	labels,freq=zip(*freq_term)
	data={'data':freq,'x':labels}
	bar=vincent.Bar(data,iter_idx='x')
	bar.to_json(fname)
	
def time_series(dates_hashtag):
	print("Generating time series for all tweets collected")
	#processing data for time-series 
	ones = [1]*len(dates_hashtag)
	# the index of the series
	idx = pandas.DatetimeIndex(dates_hashtag)
	# the actual series (at series of 1s for the moment)
	hashtag= pandas.Series(ones, index=idx)
	# Resampling / bucketing
	per_minute = hashtag.resample('3T').sum().fillna(0)
	
	#plotting a time series visualisation
	time_chart = vincent.Line(hashtag.resample('1min').sum().fillna(0))
	time_chart.axis_titles(x='Time', y='Freq')
	time_chart.to_json('./json/time_chart.json')

#def comp_series()

parser=get_parser()
args=parser.parse_args()	
name= "data/stream__"+args.filename

with codecs.open(name,'r') as f:	
	
	#to generate bar graphs for single frequent terms
	freq_bar(preprocess.count_all,'./json/term_freq.json')
	
	#to generate a time series of all collected tweets
	time_series(preprocess.dates_hashtag)
	
	#to generate comparison chart for two competing events
	#comp_series()