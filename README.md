# Build Your Own Web Crawler

## Project Description

This program accomplishes the following (derived from document):
 1. Fetch the HTML document at that URL
 2. Parse out URLs in that HTML document
 3. Log/print the URL visited along with all the URLs on the page
 4. Loop back to step 1 for each of these new URLs
 
 Additionally, the program fetches URLs in parallel to speed up the crawl.
 A stopping condition is placed to limit the number of levels of pages through which we will scrape URLs.
 
 These URLs will be output

## Instructions
To successfully run the Web Crawler, make sure to have the following Python modules installed:
 - lxml
 - Beautiful Soup
 - Requests
 - Multiprocessing
 
 Otherwise, please run the following command on a Linux/MacOS terminal:
 ```
 $pip install lxml
 $pip install beatifulsoup4
 $pip install requests
 $pip install multiprocessing
 ```
 Note: If you use Python3, replace pip with pip3
 
 To run the Web Crawler, download crawler.py and simply run the following command on Linux/MacOS terminal:
 ```
 $python3 ./crawler.py <insert_starting_url>
 ```
 Provide a url as the single argument, e.g. https://www.rescale.com
 
 ## Documentation
 There are two functions in crawler.py, *crawl* and *mp_scrape_url_list*, that achieve the web crawling.
 
 #### *crawl*
Argument: <br/>
   *starting_url*, string url<br/>
Return Value: <br/>
   *url_list*, a list of string urls 

 This will give the function the url to the webpage from which all linked urls will be scraped.
 We use Python's request module to retrieve the webpage, html module to parse from the url, and BeautifulSoup to pull data out of the file. 
 In the case we are unable to make a secure connection to the scraped website's server, we will handle all SSLErrors by disregarding those webpages and moving on the next url if it exists.
 The function then extracts all a href tags and only outputs urls with "https://" and "http://"
 
 #### *mp_scrape_url_list*
Arguments:<br/> 
   *page_url_list*, list of string urls<br/>
   *recursion*, int value for maximum recursion depth. This is a stopping condition to limit the number of levels of pages through which we will scrape URLs.<br/>
Return Value:<br/>
   None
  
*mp_scrape_url_list* generates all urls scraped from a given list of urls. We call the crawl function on the given list of urls to generate a list of urls linked in each given url. As we ultimately begin with one starting url and branch out to many urls (depending on how many urls are linked on the starting url), we have a tree structure of urls. Therefore, we choose to use recursion to generate urls linked in each given url through multiple levels of pages. We generate the list of linked urls for each url in parallel through multiprocessing using Python's Pool class of Multiprocessing module. The Pool class allows us to run a function across multiple input values in parallel. 
Additionally, we may choose the recursive depth of the function i.e. from how many level of pages we would like to scrape urls. 
    
### Testing
*test_crawler.py* is created for testing the implementation and effectiveness of multiprocessing.
To run test_crawler.py, download test_crawler.py and run the following command on a Linux/Unix terminal:
```
$python3 ./test_crawler.py <insert_starting_url> <int_level_of_pages>
```
<int_level_of_pages> will limit the int number of levels of pages from which URLs will be scraped. For fast testing, you may set the value to 1. With more input (values set to greater than 1), we will see a runtime decreased by a larger factor.

Functions of *test_crawler.py*:
#### *no_mp_scrape_url*
Arguments:<br/>
   *page_url_list*, list of string urls<br/>
   *recursion*, int value for maximum recursion depth<br/>
Return Value:<br/>
   None<br/>

*no_mp_scrape_url* has the equivalent functionality as *mp_scrape_url_list* except with no multiprocessing. Therefore, crawl function is used to scrape linked urls from given urls as well as taking advantage of recursion to scrape urls from multiple levels of pages. The maximum level of pages through which we will scrape is limited by the argument *recursion*.
 
#### *test*
Arguments:<br/>
   *url_list*, list of string urls<br/>
   *recursion*, int value for maximum recursion depth<br/>
Return Value:<br/>
   None<br/>
   
The *test* function will compare the runtime between two programs with the same purpose to scrape URLs, however, one with multiprocessing taking place and the other without. 
If successful, it will print the factor by which runtime decreased with multiprocessing. Otherwise, it will print an error message.
 
 
 
 
