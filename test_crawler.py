from webcrawler import crawl, mp_scrape_url_list
import unittest

class TestMPWebscrape(unittest.TestCase):

    def no_mp_helper(self, page_url_list, url_count, already_processed, nprocess, page_level):
        '''
        The method no_mp_helper generates all urls scraped from a given list of urls without using multiprocessing.
        We call the crawl function on the given list of urls to generate a list of urls linked in each given url.
        As we ultimately begin with one starting url and branch out to many urls (depending on how many urls are linked on the starting url),
            we have a tree structure of urls. Therefore, we choose to use recursion to generate urls linked in each given url.

        param page_url_list: list of string urls
        param url_count: int value for count of total urls scraped from web pages
        param already_processed: list of urls (strings) that's already been scraped
        param nprocess: number of processes
        param page_level: number of nested page levels to recurse through (for testing purposes). This program will run until there are absolutely no urls on the webpages if this restriction is not set.

        return total_count: total number of urls from entire nested web scraping
        '''
        if (len(page_url_list) == 0 or (page_level == 0)):
            return url_count

        url_list = []
        total_count = [len(page_url_list)]

        for url in page_url_list:
            if (url in already_processed):
                continue

            #Adding url to list of processed url's.
            already_processed.append(url)

            # Returns list of urls scraped from current url
            result = crawl(url)

            # Keeping track of total count of url's
            total_count.append(self.no_mp_helper(result, url_count+len(result), already_processed, nprocess, page_level-1))

        return sum(total_count)

    def no_mp(self, starter_url, nprocess, page_level):
        '''
        The method no_mp is identical to mp_scrape_url_list with the exception that no multiprocessing is used to generate all urls scraped from a given list of urls.
        Details provided under method no_mp_helper.

        param starter_url: starting string url
        param nprocess: number of processes to use for parallel processing
        param page_level: number of nested page levels to recurse through (for testing purposes). This program will run until there are absolutely no urls on the webpages if this restriction is not set.
        return total number of urls from entire nested web scraping
        '''
        return self.no_mp_helper([starter_url], 0, [], nprocess, page_level)


    def test_no_mp(self, starter_url, nprocess, page_level):
        '''
        Compares the total url count between web scraping urls with and without multiprocessing i.e. methods mp_scrape_url_list and no_mp
        If the test fails, an assertion error will be displayed. Otherwise, none.

        param starter_url: starting string url
        param nprocess: number of processes to use for parallel processing
        param page_level: number of nested page levels to recurse through (for testing purposes). This program will run until there are absolutely no urls on the webpages if this restriction is not set.
        '''
        no_mp_count = self.no_mp(starter_url, nprocess, page_level)
        mp_count = mp_scrape_url_list(starter_url, nprocess, page_level)

        self.assertEqual(no_mp_count, mp_count)


if __name__ == '__main__':
    testing = TestMPWebscrape()
    starting_url = "https://www.rescale.com/"#sys.argv[1] # one argument required: e.g. "https://www.rescale.com"

    '''
    Method test_no_mp arguments: starter_url, nprocess, page_level
    For testing purposes, I set page_level to 2, which signifies the number of nested page levels to recurse through.
    This program will run until there are absolutely no urls on the webpages if the page_level restriction is not set.
    '''
    url_count = testing.test_no_mp(starting_url, 4, 2)
