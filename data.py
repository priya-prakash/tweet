import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

import sys
import argparse
import string 
import json

sys.path.append('./lib')
import config

#Command line argument accepting. format becomes python data.py -q query -d data
# output stored in data/stream_query.json
def get_parser():
	parser=argparse.ArgumentParser(description="Dataset")
	parser.add_argument("-q",
						"--query",
						dest="query",
						help="Filter",
						default='-')
	parser.add_argument("-d",
						"--data-dir",
						dest="data_dir",
						help="Data Directory")
	return parser
	
class MyListener(StreamListener):

	def __init__(self, data_dir,query):
		query_fname=format_filename(query)
		self.outfile="%s/stream_%s.json" % (data_dir,query_fname)
	
	def on_data(self,data):
		try:
			with open(self.outfile,'a') as f:
				f.write(data)
				print(data,"\n")
				return True
		except BaseException as e:
			print("Error on data:%s" %str(e))
			time.sleep(5)
		return True
		
		"""try:
			with open(self.outfile,'a') as f:
				f.write(data)
				print(data)
                return True
		except BaseException as e:
			print("Error on_data: %s" % str(e))
			time.sleep(5)
		return True"""
	
	def on_error(self,status):
		print(status)
		return True
		
def format_filename(fname):
	return ''.join(convert_valid(one_char) for one_char in fname)
	
def convert_valid(one_char):
	valid_chars="-_.%s%s" % (string.ascii_letters, string.digits)
	if one_char in  valid_chars:
		return one_char
	else:
		return '_'

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status
		
if __name__ == '__main__':
	parser=get_parser()
	args=parser.parse_args()
	auth=OAuthHandler(config.consumer_key,config.consumer_secret)
	auth.set_access_token(config.access_token,config.access_secret)
	#print config.access_token
	#entry point of data
	api=tweepy.API(auth)  
	print("Entered API")
	twitter_stream=Stream(auth,MyListener(args.data_dir,args.query))
	twitter_stream.filter(track=[args.query])