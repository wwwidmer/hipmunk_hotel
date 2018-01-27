import requests
from multiprocessing.dummy import Pool as ThreadPool


API_URL = 'http://localhost:9000/scrapers/{}'


class QuickSearch(object):
    '''
        For the test parsing all URLs sequentially took over ten seconds!
        So we need to grab all of the URLs in parallel
        (Otherwise we'll be "kinda" slow)
    '''
    def __init__(self, providers, max_threads=None):
        self.providers = providers
        self.max_threads = max_threads
        if max_threads is None:
            self.max_threads = len(providers)

        self.searched = {}

    def get_url(self, url):
        '''
            Get one URL and save its contents in a dictionary
            Using requests over urllib
                because its a bit simpler to read and less code
            They're both pretty much the same performance wise
        '''
        try:
            self.searched[url] = requests.get(url).json()
        except Exception as e:
            self.searched[url] = {
                'error': str(e)
            }
    def get_all(self):
        self.searched = {}
        urls = [API_URL.format(provider) for provider in self.providers]
        thread_pool = ThreadPool(self.max_threads)
        results = thread_pool.map(self.get_url, urls)
        thread_pool.close()
        thread_pool.join()

        merged = []
        for value in self.searched.values():
            if 'error' in value:
                print('Error! {}'.format(value['error']))
                continue
            results = value['results']
            merged += results

        '''
            Just using sorted is pretty fast here - since the results of each
            API call are sorted themselves.
            See "Timsort" https://en.wikipedia.org/wiki/Timsort the algorithm
            python's sorted method uses.
            "The algorithm finds subsequences of the data that are already ordered,
            and uses that knowledge to sort the remainder more efficiently."
            This runs in (n log n). (Its constant time to insert without any rules)

            If we were going to maintain order as we appended to our results list
            we would have to "sort" as we inserted.
            An efficient way to do this sounds like some kind of tree, so that our
            sorted insertion normally takes (log n) time. 

        '''

        return sorted(merged, key=lambda x: x['ecstasy'], reverse=True)
