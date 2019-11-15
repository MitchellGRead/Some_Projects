import urllib.request
import urllib.error
import json

'''
This is created using the https://www.datamuse.com/api/ which is a word finding engine with certain constraints.
'''

'''
Could rebuild using the requests library
'''
class Datamuse:
    def __init__(self):
        self.main_url = 'https://api.datamuse.com/'


    def get_related_words(self, word, code, max=100, topic=''):
        '''
        Gets related words using a specified code:
            jja = Popular nouns by given adjective
            jjb = Popular adjectives by given noun
            trg = Words statisically associated with provided word ("triggers")
        
        Args:
            word (str): Word we want other words related to
            code (str): Three digit specific code
            max (int, optional): How many words we want to grab. Must be < 1000. Defaults to 100.
            topic (str, optional): A topic regarding the word can be provided. Defaults to ''.
        
        Returns:
            list: List of dictionaries with words and their score for relativity
        '''

        word = word.replace(' ', '+')
        slug = f'words?rel_{code}={word}&max={max}'

        json_data = self.load_json(self.main_url + slug)

        if json_data is not None:
            return json_data
        else: 
            return []


    def get_similar_meaning(self, word, max=100):
        '''
        Gets words that have a similar meaning to the one provided.
        
        Args:
            word (str): Word we want other words related to
            max (int, optional): How many words we want to grab. Must be < 1000. Defaults to 100.
        
        Returns:
            list: List of dictionaries with words and their score for relativity
        '''

        word = word.replace(' ', '+')
        slug = f'words?ml={word}&max={max}'

        json_data = self.load_json(self.main_url + slug)

        if json_data is not None:
            return json_data
        else:
            return []


    def load_json(self, url):
        '''
        Loads the json data from an API call to datamuse.com
        
        Args:
            url (str): valid datamuse http url api call
        
        Returns:
            list: list of dictionaries from api call
        '''

        json_data = self.open_page(url)

        if json_data == False:
            return None

        if json_data == []:
            return None

        return json.loads(json_data)


    def open_page(self, url):
        '''
        The following function will open a URL page and read its contents to extract data.
        
        Args:
            url (str): URL to a webpage
        
        Returns:
            str: Webpage contents of provided URL
        '''

        try:
            url_site = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            print(f'{e.code} error - {e.reason} -- Skipping: {url} ')
            return False
        except urllib.request.URLError as e:
            print(f'Please confirm {url} is a proper URL.')
            return False

        return url_site.read()#.decode('utf-8')
