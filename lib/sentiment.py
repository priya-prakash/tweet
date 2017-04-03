import textblob
from textblob import TextBlob
import time
import string
import json
import argparse

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

senti=""
subob=""

def sentiment_value(tweet_text):
	sent=TextBlob(tweet_text)
	(senti,subob)=sent.sentiment
	if(senti>0.1):
		return 1
	else:
		return 0