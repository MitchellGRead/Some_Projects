import urllib.request
import urllib.error
from bs4 import BeautifulSoup


def main():
    main_url = 'https://en.wikipedia.org/'

    start = 'wiki/bananas'
    # start = 'wiki/fruit'
    end = 'wiki/apples'

    page = open_page(main_url + start)

    soup = BeautifulSoup(page, 'html.parser')

    for div in soup.find_all('div', {'class': 'reflist'}):
        div.decompose()

    soup = soup.find(id='bodyContent')

    end_target_links = [link['href'] for link in soup.find_all('a', href=True, string='apples') if ':' not in link['href'] and '#' not in link['href']]

    if end_target_links != []:
        # navigate the links
        return

    all_valid_links = [link['href'] for link in soup.find_all('a', href=True) if ':' not in link['href'] and '#' not in link['href']]

    if all_valid_links != []:

        return 
    else:
        print(f'Could not find a connection between {start} and {end}.')

    return


def navigate_link(url):
    return


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