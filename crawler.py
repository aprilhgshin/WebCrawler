#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 20:28:11 2020

@author: april
"""

from lxml import html
from lxml.html.soupparser import fromstring
from lxml.etree import tostring
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import time
import sys

# debug int value 1 for printing statements, 0 for no extra printing statements
debug = 0
test = 1

def crawl(starting_url):
    '''
    crawl scrapes all urls from the given url. 
    param starting_url: string url
    return url_list: list of string urls scraped from starting_url
    '''
    try:
        page = requests.get(starting_url) # Retrieving webpage through Python's request
        tree = html.fromstring(page.content) # Parse from url
        soup = BeautifulSoup(tostring(tree), 'lxml') # Pulling data out of file
    except requests.exceptions.SSLError as e:
            if debug:
                print("error\n")
            return []
    print(starting_url)
    url_list = []
    for tag in soup.find_all('a'):
        link = tag.get('href')
        if link is not None:
            if (link[0:8] == "https://" or link[0:7] == "http://"):
                if link not in url_list:
                    url_list.append(link)
                    print(" ",link)
    return url_list


def mp_scrape_url_list(page_url_list, recursion):
    '''
    mp_scrape_url_list generates all urls scraped from a given list of urls. 
    We call the crawl function on the given list of urls to generate a list of urls linked in each given url. 
    As we ultimately begin with one starting url and branch out to many urls (depending on how many urls are linked on the starting url), 
        we have a tree structure of urls. Therefore, we choose to use recursion to generate urls linked in each given url.
    We generate the list of linked urls for each url in parallel through multiprocessing.
    param page_url_list: list of string urls
    param recursion: int value for maximum recursion depth
    return None
    '''
    if (recursion < 0):  
        return
    url_list = []
    p = Pool()
    result = p.map(crawl, page_url_list)
    for i in range(len(result)):
        url_list.extend(result[i])
    p.close()
    p.join()
    
    mp_scrape_url_list(url_list, recursion-1)
    
def no_mp_scrape_url(page_url_list, recursion):
    '''
    no_mp_scrape_url is identical to mp_scare_url_list except without the multiprocessing
    param page_url_list: list of string urls
    param recursion: int value for maximum recursion depth
    return None

    '''
    
    if (recursion < 0): # manually 
        return
    
    if debug:
        print("recursion ", recursion)
    url_list = []
    for url in page_url_list:
        try:
            page = requests.get(url)
            tree = html.fromstring(page.content)
            soup = BeautifulSoup(tostring(tree), 'html.parser')
        except requests.exceptions.SSLError as e:
            if debug:
                print("error\n")
            continue
        print(url)
        for tag in soup.find_all('a'):
            link = tag.get('href')
            if link is not None:
                if (link[0:8] == "https://" or link[0:7] == "http://"):
                    if link not in url_list:
                        url_list.append(link)
                        print(" ",link)


    no_mp_scrape_url(url_list, recursion-1)

    

                
if __name__ == '__main__':
    
    starting_url = sys.argv[1] # one argument required: e.g. "https://www.rescale.com"
    url_list = [starting_url]
    
    start_time = time.time()
    mp_scrape_url_list(url_list, 1) # Manually setting maximum recursion depth
    end_time = time.time() - start_time
    


    #if debug:
    #    no_mp_scrape_url_list(starting_url)

