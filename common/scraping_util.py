import re
import requests
from bs4 import BeautifulSoup # html paser

# user-agent
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
    AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8"
# search url
SEARCH_URL='https://www.google.com/search'

# BE CAREFUL!!! Google may change this ID frequently!
GOOGLE_SEARCH_NUM_ID='result-stats'

def scraper(req_param: dict, scrapings: list, url=SEARCH_URL):
    '''returns scraping result strings taken using requests and bs4
    
    :param req_param: request parameter
    :param scrapings: list of setting scrapings dict data(key:"search_tag", "attrs")
    :param url: target url for web scraping(default: google japan)
    :rtype: List(String data)
     '''

    # response
    res=requests.get(url, headers={"user-agent": UA}, params=req_param)

    # parse html
    soup=BeautifulSoup(res.text.encode('utf-8'), "html.parser")
    result_scrapings = []

    for obj in scrapings:
        # get scraping result(as String)
        text = soup.find(obj["search_tag"], attrs=obj.get("attrs", None)).get_text()
        # delete html tag for result scrapings
        result_scrapings.append(text)
    
    return result_scrapings


def get_search_num(word):
    # Search parameter
    params = {
        'q': word,
        'ie': 'utf-8',
        'hl': 'ja',
    }
    # --> This makes Google search url like below 
    # https://www.google.com/search?q=xxxx&ie=utf-8&hl=ja

    # HTML DOM element to find from the search result
    scraping_target = [{
        'search_tag': 'div',
        'attrs': {'id': GOOGLE_SEARCH_NUM_ID},
    }
    ,{
        'search_tag': 'title',
    }]
    # --> The element like below will be found (Div id may be changed frequently!)
    # <div id='result-stats'>
    #    About 123,456,000 results (0.12 seconds)  
    # </di>

    # Search & Get the number
    search_result_list = scraper(params, scraping_target)
    print('###DEBUG')
    print(search_result_list[0])
    print(search_result_list[1])
    search_num = int(re.findall(r'([0-9,]+)', search_result_list[0])[0].replace(",",""))

    return search_num
