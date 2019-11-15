from datamuse_api import Datamuse
import wikipedia
import json
import requests
import time


def main():
    wiki_url = 'https://en.wikipedia.org/wiki/'

    start_word = 'bananas'
    end_word = 'apples' # cookie red
    url_attempts = 1 #20

    results = wiki_hunt(start_word, end_word, url_attempts)

    if results['successful']:
        for i, link in enumerate(results['current_path']):
            print(f'{i}:' + wiki_url + link)
    else:
        print(f'The poor program could not find a path between {start_word} and {end_word} with {url_attempts} tries.')

    return


def wiki_hunt(current_word, end_word, url_attempts):
    datamuse = Datamuse()

    results = {
        'start_word': current_word,
        'end_word': end_word,
        'current_path': [current_word],
        'successful': False,
    }

    end_page, end_links = get_wiki_info(end_word)
    # end_similar = datamuse.get_similar_meaning(end_word)
    with open('end_sim.json') as f:
        end_similar = json.load(f)

    for i in range(url_attempts):
        # Get the current word wiki page links
        curr_page, curr_links = get_wiki_info(current_word)

        results = check_winning_page(curr_page, curr_links, end_page, results)

        if results['successful']:
            return results

        # Look for potential intersections with the target page links
        # link_intersects = get_link_intersects(curr_links, end_links)
        with open('same_links.txt') as f:
            link_intersects = f.read().lower().splitlines()

        # We want to test the link intersections as they will be likely to mention one another
        if link_intersects != []:

            # Attempt to find a reasonable path using similar words 
            words_similar = find_matching_similar_words(current_word, end_similar, link_intersects)
            words_similar = remove_visited_pages(results['current_path'], words_similar)

            if words_similar:
                highest_ranked_similar = max(words_similar, key=words_similar.get)

            # Attempt to find a reasonable path using related words
            



                # current_word = highest_rank
                # results['current_path'].append(current_word)
                # continue



            
    return results


def check_winning_page(curr_page, curr_links, end_page, results):
    if curr_page == end_page:
        results['successful'] = True
    elif end_page.title.lower() in curr_links:
        results['current_path'].append(end_page.title.lower())
        results['successful'] = True 

    return results


def remove_visited_pages(visited_pages, word_rankings):
    for page in visited_pages:
        if page in word_rankings:
            del word_rankings[page]

    return word_rankings


def find_matching_similar_words(current_word, end_similar, link_interects=[]):
    datamuse = Datamuse()
    same_similar_words = {}

    # current_similar = datamuse.get_similar_meaning(current_word)
    with open('start_sim.json') as f:
        current_similar = json.load(f)

    current_similar_words = extract_dict_words(current_similar)
    for entry in end_similar:

        entry_word = entry['word']
        if entry_word in current_similar_words:
            # get the index of the word in current similar words to correlate that to its score in its dictionary
            same_similar_words[entry_word] = entry['score'] + current_similar[current_similar_words.index(entry_word)]['score']

            # If the word is also in the list of the pages link intersects put higher emphasis on it
            if entry_word in link_interects:
                same_similar_words[entry_word] = same_similar_words[entry_word] * 2

    return same_similar_words


def extract_dict_words(datamuse_dict):
    words = []
    for entry in datamuse_dict:
        words.append(entry['word'])

    return words


def get_link_intersects(page_one_links, page_two_links):
    page_one_links = set(page_one_links)
    page_two_links = set(page_two_links)

    intersect = list(page_one_links.intersection(page_two_links))

    return intersect


def get_wiki_info(wiki_title):
    wikipedia.set_rate_limiting(True)

    try:
        wiki_page = wikipedia.page(title=wiki_title)
    except requests.Timeout as e:
        time.sleep(1)
        wiki_page = wikipedia.page(title=wiki_title)

    links = ['dfadf']
    # links = [link.lower() for link in wiki_page.links]
    return (wiki_page, links)


if __name__ == "__main__":
    main()