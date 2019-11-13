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

    results = wiki_hunt(start_word, end_word, url_attempts)

    print(results)

    return


def wiki_hunt(current_word, end_word, url_attempts):
    main_url = 'https://en.wikipedia.org/wiki/'
    datamuse = Datamuse()

    results = {
        'start_word': current_word,
        'end_word': end_word,
        'current_path': [current_word],
        'successful': False,
    }

    end_page, end_links = get_wiki_info(end_word)
    end_similar = datamuse.get_similar_meaning(end_word)
    # with open('end_sim.json') as f:
    #     end_similar = json.load(f)

    for i in range(url_attempts):
        # Get the current word wiki page links
        curr_page, curr_links = get_wiki_info(current_word)

        results = check_winning_page(curr_page, end_page, results)

        if results['successful']:
            return results

        # Look for potential intersections with the target page links
        link_intersects = get_link_intersects(curr_links, end_links)
        # with open('same_links.txt') as f:
        #     link_intersects = f.read().lower().splitlines()

        if link_intersects != []:
            words_similar = find_similar_words(current_word, end_similar, link_intersects)
            words_similar = remove_visited_pages(results['current_path'], words_similar)

            if words_similar:
                highest_rank = max(words_similar, key=words_similar.get)

                current_word = highest_rank
                results['current_path'].append(current_word)
                continue
            
    return results


def check_winning_page(curr_page, end_page, results):
    if curr_page == end_page:
        results['successful'] = True
    elif end_page.title.lower() in [link.lower() for link in curr_page.links]:
        results['current_path'].append(end_page.title.lower())
        results['successful'] = True 

    return results

def remove_visited_pages(visited_pages, word_rankings):
    for page in visited_pages:
        if page in word_rankings:
            del word_rankings[page]

    return word_rankings


def find_similar_words(current_word, end_similar, link_intersects):
    datamuse = Datamuse()

    # Get words similar to the start and end
    start_similar = datamuse.get_similar_meaning(current_word)

    # with open('start_sim.json') as f:
    #     start_similar = json.load(f)

    # Find all the similar words that match with the intersection totalling duplicates scores
    summed_relations = intersect_similar_words(start_similar, end_similar, link_intersects)
    
    return summed_relations


def intersect_similar_words(current_similar, end_similar, link_interects):
    summed_relations = {}

    # Find the similar words for our target page matching with our common links
    for word in end_similar:
        if word['word'] in link_interects:
            common_word = word['word']

            if not common_word in summed_relations:
                summed_relations[common_word] = word['score']
            else:
                summed_relations[common_word] += word['score']

    # Sum/add the similar words.
    for word in current_similar:
        if word['word'] in link_interects:
            valid = word['word']

            if not valid in summed_relations:
                summed_relations[valid] = word['score']
            else:
                summed_relations[valid] += word['score']

    return summed_relations


def get_link_intersects(page_one_links, page_two_links):
    page_one_links = set(page_one_links)
    page_two_links = set(page_two_links)

    intersect = list(page_one_links.intersection(page_two_links))

    return intersect


def get_wiki_info(wiki_title):
    wiki_page = wikipedia.page(title=wiki_title)
    # links = ['dfadf']
    links = [link.lower() for link in wiki_page.links]
    return (wiki_page, links)


if __name__ == "__main__":
    main()