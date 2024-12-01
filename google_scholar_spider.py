import datetime
import os
import pandas as pd
import requests
import warnings
from dataclasses import dataclass
from time import sleep
from typing import List
from bs4 import BeautifulSoup
from tqdm import tqdm

MAX_CSV_FNAME = 255

now = datetime.datetime.now()
current_year = now.year

# Websession Parameters
GSCHOLAR_URL = 'https://scholar.google.com/scholar?start={}&q={}&hl=en&as_sdt=0,5'
ROBOT_KW = ['unusual traffic from your computer network', 'not a robot']
STARTYEAR_URL = '&as_ylo={}'
ENDYEAR_URL = '&as_yhi={}'

@dataclass
class ArgsConfig:
    task: str = "no task",
    keyword: str = "machine learning"
    nresults: int = 50
    save_csv: bool = True
    csvpath: str = "."
    sortby: str = "Citations"
    year: int = 2000
    source: str = 'ACL'


def google_scholar_spider(GoogleScholarConfig: ArgsConfig):
    gscholar_main_url = create_main_url(GoogleScholarConfig)

    session = requests.Session()

    with tqdm(total=GoogleScholarConfig.nresults) as pbar:
        data = fetch_data(GoogleScholarConfig, session, gscholar_main_url, pbar)

    data_ranked = process_data(data, GoogleScholarConfig.sortby)

    save_data_to_csv(data_ranked, GoogleScholarConfig.csvpath, f'{GoogleScholarConfig.source}_{GoogleScholarConfig.keyword}')


def create_main_url(GoogleScholarConfig: ArgsConfig) -> str:
    if GoogleScholarConfig.year:
        gscholar_main_url = GSCHOLAR_URL + STARTYEAR_URL.format(GoogleScholarConfig.year)
    else:
        gscholar_main_url = GSCHOLAR_URL

    if GoogleScholarConfig.year != current_year:
        gscholar_main_url = gscholar_main_url + ENDYEAR_URL.format(GoogleScholarConfig.year)
    
    return gscholar_main_url


def fetch_data(GoogleScholarConfig: ArgsConfig, session: requests.Session, gscholar_main_url: str,
               pbar: tqdm) -> pd.DataFrame:
    links: List[str] = []
    title: List[str] = []
    citations: List[int] = []
    year: List[int] = []
    author: List[str] = []
    venue: List[str] = []
    publisher: List[str] = []
    rank: List[int] = [0]
    describe: List[str] = []

    if pbar is not None:
        pbar.reset(total=GoogleScholarConfig.nresults)

    for n in range(0, GoogleScholarConfig.nresults, 10):
        if pbar is not None:
            pbar.update(10)

        source = GoogleScholarConfig.source.split(',')
        source_text = ''
        for i, s in enumerate(source):
            source_text += f'source:{s}'
            if i != len(source)-1:
                source_text += f' OR '
        url = gscholar_main_url.format(str(n), f'{GoogleScholarConfig.keyword.replace(",", "+")} ({source_text})')


        page = session.get(url)
        c = page.content

        if any(kw in c.decode('ISO-8859-1') for kw in ROBOT_KW):
            print("Robot checking detected, handling with selenium (if installed)")
            c = get_content_with_selenium(url)

        soup = BeautifulSoup(c, 'html.parser', from_encoding='utf-8')
        mydivs = soup.findAll("div", {"class": "gs_or"})

        for div in mydivs:
            try:
                links.append(div.find('h3').find('a').get('href'))
            except:
                links.append('Look manually at: ' + url)

            try:
                title.append(div.find('h3').find('a').text)
            except:
                title.append('Could not catch title')

            try:
                citations.append(get_citations(str(div.format_string)))
            except:
                citations.append(0)

            try:
                year.append(get_year(div.find('div', {'class': 'gs_a'}).text))
            except:
                year.append(0)

            try:
                author.append(get_author(div.find('div', {'class': 'gs_a'}).text))
            except:
                author.append("Author not found")

            try:
                publisher.append(div.find('div', {'class': 'gs_a'}).text.split("-")[-1])
            except:
                publisher.append("Publisher not found")

            try:
                venue.append(" ".join(div.find('div', {'class': 'gs_a'}).text.split("-")[-2].split(",")[:-1]))
            except:
                venue.append("Venue not found")

            try:
                describe.append(get_author(div.find('div', {'class': 'gs_rs'}).text))
            except:
                describe.append("Describe not found")

            rank.append(rank[-1] + 10)

        sleep(0.5)

    data = pd.DataFrame(list(zip(author, title, citations, year, publisher, venue, describe, links)), index=rank[1:],
                        columns=['Author', 'Title', 'Citations', 'Year', 'Publisher', 'Venue', 'describe', 'Source'])
    data.index.name = 'Rank'
    return data


def get_citations(content):
    citation_start = content.find('Cited by ')
    if citation_start == -1:
        return 0
    citation_end = content.find('<', citation_start)
    return int(content[citation_start + 9:citation_end])


def get_year(content):
    for char in range(0, len(content)):
        if content[char] == '-':
            out = content[char - 5:char - 1]
    if not out.isdigit():
        out = 0
    return int(out)


def get_author(content):
    author_end = content.find('-')
    return content[2:author_end - 1]


def get_content_with_selenium(url):
    print("Selenium method not implemented yet.")
    return ''


def process_data(data: pd.DataFrame, sortby: str) -> pd.DataFrame:
    """Process the data by sorting it."""
    try:
        data_ranked = data.sort_values(by=sortby, ascending=False)
    except Exception as e:
        print(f"Error sorting by {sortby}, sorting by Citations instead.")
        data_ranked = data.sort_values(by='Citations', ascending=False)
        print(e)
    return data_ranked


def save_data_to_csv(data: pd.DataFrame, path: str, keyword: str) -> None:
    """Save the processed data to a CSV file."""
    if not os.path.exists(path):
        os.makedirs(path)
    fpath_csv = os.path.join(path, keyword.replace(' ', '_').replace(':','-') + '.csv')
    fpath_csv = fpath_csv[:MAX_CSV_FNAME]
    data.to_csv(fpath_csv, encoding='utf-8')
