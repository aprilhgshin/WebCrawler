#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 20:04:42 2020

@author: april
"""
from crawler import crawl, mp_scrape_url_list
from lxml import html
from lxml.html.soupparser import fromstring
from lxml.etree import tostring
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import time
import sys

def no_mp_scrape_url(page_url_list, recursion):
    '''
    no_mp_scrape_url is identical to mp_scare_url_list except without the multiprocessing
    param page_url_list: list of string urls
    param recursion: int value for maximum recursion depth
    return None

    '''
    
    if (recursion < 0): # manually 
        return

    url_list = []
    for url in page_url_list:
        try:
            page = requests.get(url)
            tree = html.fromstring(page.content)
            soup = BeautifulSoup(tostring(tree), 'html.parser')
        except requests.exceptions.SSLError as e:
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
    
def test(url_list, recursion):
    start_time = time.time()
    mp_scrape_url_list(url_list, recursion) # Manually setting maximum recursion depth
    end_time = time.time() - start_time

    # To compare the runtime of program with multiprocessing and without multiprocessing
    start_time_noMP = time.time()
    no_mp_scrape_url(url_list, 1)
    end_time_noMP = time.time() - start_time_noMP
    
    if (end_time - end_time_noMP) > 0:
        print("Multiprocessing error")
    elif (end_time - end_time_noMP) < 0:
        factor = end_time/end_time_noMP
        print("Success. Runtime is decreased by a factor of ", factor, "for ", recursion, "level of pages")
    
    
if __name__ == '__main__':
    starting_url = sys.argv[1] # one argument required: e.g. "https://www.rescale.com"
    url_list = [starting_url]
    recursion = int(sys.argv[2])
    
    test(url_list, recursion)
   