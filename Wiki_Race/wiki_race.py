import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import wikipedia


def main():
    main_url = 'https://en.wikipedia.org/'

    start = 'wiki/bananas'
    # start = 'wiki/fruit'
    end = 'wiki/Apples'
    url_attempts = 2

    soup = get_body_content(main_url + start)

    end_target_links = find_links(soup, 'apples')

    if end_target_links != []:
        # navigate the links
        return

    all_valid_links = find_links(soup)

    for link in all_valid_links:
        print(link)

    return
    if all_valid_links != []:

        return 
    else:
        print(f'Could not find a connection between {start} and {end}.')

    return


# def navigate_links(links, depth, )



def check_winning_page(end_target, url):
    '''
    Used to decide if we have reached the end target page by providing the url. 
    We split the URL on / and grab the last word in the list and compare to our end target word that is sentence capitalized (wiki specific).
    Next it will grab the first body content url in the case of a redirect (still valid) and compare to that.
        i.e. apples redirects to apple in the wiki url and will be counted as valid.

    
    Args:
        end_target (str): Target page we want to end up on
        url (str): Wiki valid URL
    
    Returns:
        bool: True if we believe to have found the page and false otherwise
    '''
    url_word = url.split('/')
    url_word = url_word[-1]
    end_target = end_target.capitalize()

    if url_word == end_target:
        return True 

    soup = get_body_content(url)
    links = find_links(soup, wiki_only=False)
    links = links[0]

    if end_target in links and 'redirect' in links:
        return True 

    return False


def get_body_content(url):
    '''
    Gets the body contents of a wikipedia page
    
    Args:
        url (str): URL to a wiki page
    
    Returns: 
        bs4 object: bs4 object contained the body content HTML data of the wiki page
        False: Occurs if the page fails to open or does not exist
    '''
    page = open_page(url)

    if page == False:
        return False

    soup = BeautifulSoup(page, 'html.parser')

    for div in soup.find_all('div', {'class': 'reflist'}):
        div.decompose()

    soup = soup.find(id='bodyContent')

    return soup


def find_links(soup, find_me='', wiki_only=True):
    '''
    Finds all links with the find_me keyword in them using Beautiful soup
    
    Args:
        soup (bs4 object): A beautiful soup object
        find_me (str): Keyword to find. Defaults to find all links.
        wiki_only (bool): Grabs only the links that start with /wiki/
    
    Returns:
        list: List of links found in the search
    '''
    if wiki_only:
        return [link['href'] for link in soup.find_all('a', href=True, string=find_me) if link['href'].startswith('/wiki/') and ':' not in link['href'] and '#' not in link['href']]
    else :
        return [link['href'] for link in soup.find_all('a', href=True, string=find_me) if ':' not in link['href'] and '#' not in link['href']]


def open_page(url):
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


if __name__ == "__main__":
    main()