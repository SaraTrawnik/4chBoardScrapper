#! /usr/bin/python3
import os
import requests
import argparse

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
    
    # get all link of threads you want downloaded / remember about current 4chan 4channel split
    
    # get links of all pictures in the thread
    
    # get actual pictures and store in the dir named after a thread
