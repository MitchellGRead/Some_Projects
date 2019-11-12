import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from datamuse_api import Datamuse
import wikipedia
import json


def main():
    start_word = 'bananas'
    end_word = 'apples'
    url_attempts = 20

    results = begin_wiki_hunt(start_word, end_word, url_attempts)

    return


def begin_wiki_hunt(start_word, end_word, url_attempts):
    main_url = 'https://en.wikipedia.org/wiki/'
    datamuse = Datamuse()

    results = {
        'start_word': start_word,
        'end_word': end_word,
        'found_path': [],
        'successful': False,
    }

    # start_links = wikipedia.WikipediaPage(start_word).links 
    # end_links = wikipedia.WikipediaPage(end_word).links

    # start_links = set(start_links)
    # end_links = set(end_links)

    # link_intersects = start_links.intersection(end_links)

    with open('same_links.txt') as f:
        link_interects = f.read().splitlines()


    # start_similar = datamuse.get_similar_meaning(start_word)
    # end_similar = datamuse.get_similar_meaning(end_word)

    with open('start_sim.json') as f:
        start_similar = json.load(f)

    with open('end_sim.json') as f:
        end_similar = json.load(f)

    

    return results


if __name__ == "__main__":
    main()