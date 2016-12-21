from Download import request
from mongodb_queue import MogoQueue
from bs4 import BeautifulSoup

spider_queue=MogoQueue('meinvxiezhenji','crawl_queue')
def start(start_url):
    start_html = request.get(start_url, 3)
    soup = BeautifulSoup(start_html.text, 'lxml')
    li_list = soup.find('div', {'class': 'all'}).find_all('a')
    for li in li_list:
        title = li.get_text()
        url=li['href']
        spider_queue.push(url,title)

if __name__ == '__main__':
    start('http://www.mzitu.com/all')