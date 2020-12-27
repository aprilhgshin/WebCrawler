# Build Your Own Web Crawler

## Project Description

This program accomplishes the following:
 1. Fetch the HTML document at that URL
 2. Parse out URLs in that HTML document
 3. Log/print the URL visited along with all the URLs on the page
 4. Loop back to step 1 for each of these new URLs
 
 Additionally, the program fetches URLs in parallel to speed up the crawl using Python's multiprocessing module.
 A stopping condition is placed to limit the number of levels of pages through which we will scrape URLs for testing purposes.

## Instructions
To successfully run the Web Crawler, make sure to have the following Python modules installed:
 - lxml
 - Beautiful Soup
 - Requests
 - Multiprocessing
 
 Otherwise, please run the following command on a Linux/MacOS terminal:
 ```
 $pip3 install lxml
 $pip3 install beatifulsoup4
 $pip3 install requests
 $pip3 install multiprocessing
 ```
 Note: pip3 is for those with Python of version 3 and up.
 
 To use the web crawler, first, clone the WebCrawler repository with the the following command on Linux/MacOS terminal:
 ```
 $ git clone https://github.com/aprilhgshin/WebCrawler.git
 ```
 
 To run the webcrawler, use the following commands on terminal:
 ```
 $python3 webcrawler.py <insert_starting_url>
 ```
 Provide a url as the single argument, e.g. https://www.rescale.com
 
 ### Troubleshooting 
 If you receive an error regarding threads/forks, please enter the following commands in your terminal: 
 ```
 $nano .bash_profile
 ```
 
 Write the following statement in the open file:
 ```
 $export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
 ```
 Save and exit the file. Run webcrawler.py.
 
 If the same error persists, when compiling and running webcrawler.py, also use the command: 
 ```
 $OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES python3 webcrawler.py
 ```
 ## webcrawler.py
 There are two functions in webcrawler.py, *crawl* and *mp_scrape_url_list*, that achieve the web crawling.
  #### *crawl*

 This will give the method the url to the webpage from which all linked urls will be scraped.
 We use Python's request module to retrieve the webpage, html module to parse from the url, and BeautifulSoup to pull data out of the file. 
 In the case we are unable to make a secure connection to the scraped website's server, we will handle all SSLErrors by disregarding those webpages and moving on the next url if it exists.
 The function then extracts all a href tags and only outputs urls with "https://" and "http://"
 
 #### *mp_scrape_url_list*
  
Using the helper method *scrape helper*, *mp_scrape_url_list* generates all urls scraped from a given list of urls. We call the crawl function on the given list of urls to generate a list of urls linked in each given url. As we ultimately begin with one starting url and branch out to many urls (depending on how many urls are linked on the starting url), we have a tree structure of urls. Therefore, we choose to use recursion to generate urls linked in each given url through multiple levels of pages. We generate the list of linked urls for each url in parallel through multiprocessing using Python's Pool class of Multiprocessing module. The Pool class allows us to run a function across multiple input values in parallel. 
Additionally, we may choose the number of nested page levels to recurse through (for testing purposes). This program will run until there are absolutely no urls on the webpages if this restriction is not set.

    
 ## test_crawler.py
 *test_crawler.py* is created for testing the web scraping with and without multiprocessing.
 It contains the method *no_mp*, which implements the same functionality as *mp_scrape_url_list* except without multiprocessing.
 It also contains a test to compare the total number of urls scraped yielded from the methods *mp_scrape_url_list* and *no_mp*.
 To run *test_crawler.py*, run the following command on a Linux/Unix terminal:
 ```
 $python3 test_crawler.py
 ```
 The test compares the total url count between web scraping urls with and without multiprocessing.
 If the test fails i.e. the counts are not identical, then an assertion error will be displayed. Otherwise, nothing will happen.



 
 
