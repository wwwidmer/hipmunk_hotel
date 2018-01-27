import requests
from multiprocessing.dummy import Pool as ThreadPool


API_URL = 'http://localhost:9000/scrapers/{}'


class QuickSearch(object):
    '''
        For the test parsing all URLs took over ten seconds!
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
        self.searched[url] = requests.get(url).json()

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

        return sorted(merged, key=lambda x: x['ecstasy'], reverse=True)
