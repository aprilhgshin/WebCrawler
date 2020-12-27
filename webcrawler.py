from lxml import html
from lxml.html.soupparser import fromstring
from lxml.etree import tostring
import requests
from bs4 import BeautifulSoup
#import sys
import multiprocessing as mp
import os

# debug int value 1 for printing statements, 0 for no extra printing statements
debug = 0

def crawl(starting_url):
    '''
    The method crawl scrapes all urls from the given url.
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

    # Scrapes web page of starting_url and prints & saves all identified urls with https or http into url_list
    for tag in soup.find_all('a'):
        link = tag.get('href')
        if link is not None:
            if (link[0:8] == "https://" or link[0:7] == "http://"):
                # To make sure we don't have duplicate urls
                if link not in url_list:
                    url_list.append(link)
                    print(" ",link)
    return url_list


def mp_scrape_url_list(starter_url, nprocess, page_level):
    '''
    The method mp_scrape_url_list generates all urls scraped from a given list of urls.
    Details provided under method scrape_helper

    param starter_url: starting string url
    param nprocess: number of processes to use for parallel processing
    param page_level: number of nested page levels to recurse through (for testing purposes). This program will run until there are absolutely no urls on the webpages if this restriction is not set.
    return total number of urls from entire nested web scraping
    '''
    return scrape_helper([starter_url], 0, [], nprocess, page_level)


def scrape_helper(page_url_list, url_count, already_processed, nprocess, page_level):
    '''
    The method scrape_helper generates all urls scraped from a given list of urls.
    We call the crawl function on the given list of urls to generate a list of urls linked in each given url.
    As we ultimately begin with one starting url and branch out to many urls (depending on how many urls are linked on the starting url),
        we have a tree structure of urls. Therefore, we choose to use recursion to generate urls linked in each given url.
    We generate the list of linked urls for each url in parallel through multiprocessing.

    param page_url_list: list of string urls
    param url_count: int value for count of total urls scraped from web pages
    param already_processed: list of urls (strings) that's already been scraped
    param nprocess: number of processes
    param page_level: number of nested page levels to recurse through (for testing purposes). This program will run until there are absolutely no urls on the webpages if this restriction is not set.

    return total_count: total number of urls from entire nested web scraping
    '''
    if (len(page_url_list) == 0 or page_level == 0):
        return url_count

    url_list = []
    total_count = len(page_url_list)

    with mp.Pool(processes=nprocess) as p:

        for url in page_url_list:
            # If url was already processed (i.e. webscraped), skip and process next url
            if (url in already_processed):
                continue

            #Adding url to list of processed url's.
            already_processed.append(url)

            # Returns list of urls scraped from current url
            crawl_result = p.map(crawl, [url])
            result = crawl_result[0]

            # Keeping track of total count of url's
            total_count += (scrape_helper(result, url_count+len(result), already_processed, nprocess, page_level-1))

    return total_count


if __name__ == '__main__':

    starting_url = sys.argv[1] # one argument required: e.g. "https://www.rescale.com"
    '''
    Method mp_scrape_url_list arguments: starter_url, nprocess, page_level
    I set page_level to 3, which signifies the number of nested page levels to recurse through.
    This program will run until there are absolutely no urls on the webpages if the page_level restriction is not set.
    '''
    url_count = mp_scrape_url_list(starting_url, 4, 3)
