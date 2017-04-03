import re
import json

import argparse
import codecs
import pandas
import io
import vincent
from collections import Counter

import nltk
from nltk.corpus import stopwords

import string
import sys
reload(sys)
sys.setdefaultencoding('utf8')

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
	
parser=get_parser()
args=parser.parse_args()	
name= "data/stream__"+args.filename

with open(name, 'r') as f:
	geo_data = {
		"type": "FeatureCollection",
		"features": []
	}
	for line in f:
		tweet = json.loads(line)
		if 'coordinates' not in tweet:
			continue
		geo_json_feature = {
			"type": "Feature",
			"geometry": tweet['coordinates'],
			"properties": {
				"text": tweet['text'],
				"created_at": tweet['created_at']
			}
		}
		geo_data['features'].append(geo_json_feature)
 
# Save geo data
with open('./json/geo_data.json', 'w') as fout:
	fout.write(json.dumps(geo_data, indent=4))