from datamuse_api import Datamuse
import wikipedia
import json
import requests
import time
import random


def main():
    wiki_url = 'https://en.wikipedia.org/wiki/'

    start_word = 'bananas'
    end_word = 'red' # cookie red
    url_attempts = 20

    results = wiki_hunt(start_word, end_word, url_attempts)

    if results['successful']:
        for i, link in enumerate(results['current_path']):
            print(f'{i}: ' + wiki_url + link)
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

    # Pull the end page information since it remains constant
    end_page, end_links = get_wiki_info(end_word)
    end_page_similar = datamuse.get_similar_meaning(end_word)
    end_page_related = datamuse.get_related_words(end_word, code='trg')

    for i in range(url_attempts):
        print(f'Attempt {i}, searching the wiki page {current_word}.')
        
        # Get the current word wiki page links
        curr_page, curr_links = get_wiki_info(current_word)

        results = check_winning_page(curr_page, curr_links, end_page, results)

        if results['successful']:
            return results

        # Look for potential intersections with the target page links
        link_intersects = get_link_intersects(curr_links, end_links)

        if end_word in link_intersects:
            next_word = end_word
            current_word = next_word
            results['current_path'].append(current_word)
            continue

        # We want to test the link intersections as they will be likely to mention one another
        if link_intersects != []:
            words_similar = find_matching_words(current_word, end_page_similar, 'similar', results['current_path'], link_intersects)
            words_related = find_matching_words(current_word, end_page_related, 'related', results['current_path'], link_intersects)

        elif link_intersects == []:
            words_similar = find_matching_words(current_word, end_page_similar, 'similar', results['current_path'])
            words_related = find_matching_words(current_word, end_page_related, 'related', results['current_path'])

        next_word = find_next_word(words_related, words_similar)

        # if we failed to find the next optimal word then we are going to hope and select a random link
        if next_word == '':
            next_word = random.choice(curr_links)

        current_word = next_word
        results['current_path'].append(current_word)

    return results


def find_next_word(words_related, words_similar):
    if words_related and words_similar:
        highest_ranked_similar = max(words_similar, key=words_similar.get)
        highest_ranked_related = max(words_related, key=words_related.get)

        if words_related[highest_ranked_related] >= words_related[highest_ranked_similar]:
            next_word = highest_ranked_related
        else:
            next_word = highest_ranked_similar
    elif words_related:
        next_word = max(words_related, key=words_related.get)
    elif words_similar:
        next_word = max(words_similar, key=words_similar.get)
    else:
        next_word = ''

    return next_word


def find_matching_words(current_word, end_api_words, word_type, visited_pages, link_interects=[]):
    datamuse = Datamuse()
    matching_words = {}

    # Get the current words respective information
    if word_type == 'similar':
        current_api_words = datamuse.get_similar_meaning(current_word)
    elif word_type == 'related':
        current_api_words = datamuse.get_related_words(current_word, code='trg')

    # Find matching words and add their scores
    current_words = extract_dict_words(current_api_words)
    for entry in end_api_words:
        entry_word = entry['word']

        if entry_word in current_words:
            # get the index of the word in current similar words to correlate that to its score in its dictionary
            matching_words[entry_word] = entry['score'] + current_api_words[current_words.index(entry_word)]['score']

            # If the word is also in the list of the pages link intersects put higher emphasis on it
            if entry_word in link_interects:
                matching_words[entry_word] = matching_words[entry_word] * 2

    # Remove any already visited pages
    matching_words = remove_visited_pages(visited_pages, matching_words)

    return matching_words


def remove_visited_pages(visited_pages, word_rankings):
    for page in visited_pages:
        if page in word_rankings:
            del word_rankings[page]

    return word_rankings


def extract_dict_words(datamuse_dict):
    return [entry['word'] for entry in datamuse_dict]


def check_winning_page(curr_page, curr_links, end_page, results):
    if curr_page == end_page:
        results['successful'] = True
    elif end_page.title.lower() in curr_links:
        results['current_path'].append(end_page.title.lower())
        results['successful'] = True 

    return results


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

    links = [link.lower() for link in wiki_page.links]
    return (wiki_page, links)


if __name__ == "__main__":
    main()