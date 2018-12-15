#! /usr/bin/python3
import os
import requests
import argparse

def hand_shake(board): #gets the list of all threads
  r = requests.get(url="http://a.4cdn.org/"+board+"/catalog.json")
  return [str(z['no']) for x in r.json() for z in x['threads']]

def open_preferences(keywords):
  try:
    with open(keywords, 'r') as flow: # this is bit ugly
      return {'whitelist': flow.readline().lower().replace('\n','').split(' '), 'blacklist': flow.readline().lower().replace('\n','').split(' ')}
  except (IOError, TypeError): # assume there is no white/black-list keywords
      return {'whitelist':[],'blacklist':[]}
    
#you first iterate by all threads in the catalog
#then you choose which you want to get
#and get all the threads
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("board", help="which board you want to scrap", type=str)
  parser.add_argument("-k", "--keywords", help="file with keywords", type=str)
  parser.add_argument("-i", "--ignore", help="ignore everything that isn't in keywords", action="store_true")
  parser.add_argument("-a", "--all", help="get absolutely everything", action="store_true")
  args = parser.parse_args()
    
  # get all of the preferences from `keywords`
  pref = open_preferences(args.keywords)
  # get all link of threads you want downloaded / remember about current 4chan 4channel split
  all_links = ["http://a.4cdn.org/"+args.board+"/thread/"+x+".json" for x in hand_shake(args.board)]
  # get links of all pictures in the thread
    
  # get actual pictures and store in the dir named after a thread
