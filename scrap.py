#! /usr/bin/python3
import os
import requests
import argparse

def hand_shake(board): #gets the list of all threads
  r = requests.get(url="http://a.4cdn.org/"+board+"/catalog.json")
  return [str(z['no']) for x in r.json() for z in x['threads']]

def get_files_in_thread(r, board, files):
  for x in [str(z['tim'])+str(z['ext']) for z in r if 'tim' in z]:
    if not(x in files):
      resp = requests.get("http://i.4cdn.org/"+board+"/"+x, stream=True) # problematic line
        with open(x, 'wb') as saveFile:
          for chunk in resp.iter_content(1024):
            saveFile.write(chunk)
                    
def check_for_preferences(subcom, preference, ignore):
  if any(x in subcom for x in preference['blacklist']):
    return False
  if any(x in subcom for x in preference['whitelist']):
    return True
  if not(ignore):
    print(subcom)
      if input('>') == 'y':
        return True
      
def get_description(thread):
  return '\n'.join([ thread['posts'][0][x] if x in thread['posts'][0] else "" for x in ['sub','com'] ]).lower()
  
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
  queue_to_download = {}
  for x in all_links: # should be like: get info from thread, download thread
    print(x)
    r = requests.get(url=x).json()
    if args.all or check_for_preferences( get_description(r), pref, args.ignore ) is True:
      queue_to_download[r['posts'][0]['no']] = r['posts']
      
  # get actual pictures and store in the dir named after a thread
  for key, item in queue_to_download.items():
    directory = "./"+args.board+str(key) #make a directory after first post
    if not(os.path.isdir(directory)):
      os.mkdir(directory)
    os.chdir(directory)
    get_files_in_thread( item, args.board, os.listdir("../"+directory) )
    os.chdir('..')
