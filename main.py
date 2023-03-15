import requests
import argparse
from bs4 import BeautifulSoup as bs
import os

def naver_news(page_num):
    '''
    page_num : 페이지 번호
    '''

    cookies = {
        '_ga': 'GA1.3.1160311499.1678260565',
        'Bigkinds': 'DDF5FF973D02637109DE48B1AB337692',
        '_gid': 'GA1.3.187155468.1678889505',
        '_gat': '1',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8,de;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://www.bigkinds.or.kr',
        'Referer': 'https://www.bigkinds.or.kr/v2/news/index.do',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    json_data = {
        'indexName': 'news',
        'searchKey': '',
        'searchKeys': [
            {},
        ],
        'byLine': '',
        'searchFilterType': '1',
        'searchScopeType': '1',
        'searchSortType': 'date',
        'sortMethod': 'date',
        'mainTodayPersonYn': '',
        'startDate': '2022-12-15',
        'endDate': '2023-03-15',
        'newsIds': None,
        'categoryCodes': [],
        'providerCodes': [],
        'incidentCodes': [],
        'networkNodeType': '',
        'topicOrigin': '',
        'dateCodes': [],
        'editorialIs': False,
        'startNo': f'{page_num}',
        'resultNumber': '100',
        'isTmUsable': False,
        'isNotTmUsable': False,
    }

    response = requests.post('https://www.bigkinds.or.kr/api/news/search.do', cookies=cookies, headers=headers, json=json_data)
    results = response.json()
    for result in results['resultList']:
        reporter = result['BYLINE']
        category = result['CATEGORY_NAMES']
        title = result['TITLE']
        content = bs(result['CONTENT'], 'html.parser').text
        with open('comments/contents.tsv', 'a', encoding='utf-8')as f:
            f.write(f'{title}\t{content}\t{reporter}\t{category}\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", default=1)
    parser.add_argument("-e", "--end", default=10)
    args = parser.parse_args()

    if not os.path.exists("comments"):
        os.mkdir("comments")

    for page_num in range(args.start, args.end, 1):
        naver_news(page_num)