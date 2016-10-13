# Change original to include ConfigParser and make it a function

import string
import datetime, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from bs4 import BeautifulSoup, Tag
import pandas as pd
import ConfigParser
import DailyOIstd

path = 'DailySPYrun.cfg'

config = ConfigParser.ConfigParser()
config.read(path)

URL_PREFIX = config.get('Settings', 'url_prefix')
SPYOIFile = config.get('Settings', 'spyoptfile')


def expirationDate():
    today = datetime.date.today()
    todayAt17 = datetime.datetime(today.year, today.month, today.day, 17)
    nextFridayAt17 = todayAt17 + datetime.timedelta(12 - today.isoweekday())
    str_friday = nextFridayAt17.strftime("%Y-%m-%d")
    return str_friday

def nextFriAt17():
    today = datetime.date.today()
    todayAt17 = datetime.datetime(today.year, today.month, today.day, 17)
    nextFridayAt17 = todayAt17 + datetime.timedelta(11 - today.isoweekday())

    #print ("nextFridayAt17="), nextFridayAt17
    str_fridayAt17 = nextFridayAt17.strftime("%Y-%m-%d-%H")
    unix_fridayAt17 = time.mktime(datetime.datetime.strptime(str_fridayAt17, "%Y-%m-%d-%H").timetuple())
    next_Friday = str(int(unix_fridayAt17))
    return next_Friday


def rm_quotes(txt):
    if not isinstance(txt, basestring):
        return txt
    return ''.join(ch for ch in txt if ch != '"')


def rm_non_ascii(s):
    """
    remove any non ascii characters
    """
    if not isinstance(s, basestring):
        return s
    s = s.strip()
    s = ''.join(filter(lambda x: ord(x)<128, s))
    return str(s)


def rm_punct(txt):
    """
    remove all punctuation except for underscore.
    """
    txt = txt.strip().replace('\n', ' ')
    txt = rm_non_ascii(txt).strip()
    exclude = ''.join(ch for ch in string.punctuation if ch != '_')
    s = ''.join([c for c in txt if c not in exclude])
    return s


def snakify(txt):
    """
    downcases and swap spaces for underscore.
    """
    if not isinstance(txt, basestring):
        txt = str(txt)
    s = rm_punct(txt)
    s = '_'.join(s.split()).lower()
    return s


def to_dataframe(table):
    """
    Takes a list of lists. Returns a DataFrame. Assumes columns are in table[0].
    """
    data = extract_all_data(table)
    if len(data) < 2:
        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame(data[1:], columns=data[0])
    # drop columns which are entirely null
    # mostly this will be link columns we've added which never have links
    df = df.replace({'': None})
    df.columns = map(snakify, df.columns)
    df = df.apply(lambda x: x.apply(rm_quotes)) # rm double quoted strings
    df = df.apply(lambda x: x.str.replace('\n', ' '), axis=1) # rm new lines
    return df


def extract_links(tag, sep=','):
    cells = extract_txt(tag)
    links_lists = [el.find_all('a') for el in tag if isinstance(el, Tag)]
    hrefs = [sep.join([a.attrs.get('href', '') for a in links]) for links in links_lists]
    return hrefs


def add_column(colname, suffix):
    return colname+'_'+suffix


def extract_txt(tag):
    return [el.get_text().strip() for el in tag if isinstance(el, Tag)]


def extract_all_data(table):
    data = []
    if isinstance(table, Tag):
        table = [tr for tr in table.find_all('tr')]
    for i, row in enumerate(table):
        if i == 0:
            colnames = extract_txt(row)
            colnames += map(lambda x: add_column(x, suffix='link'), colnames)
            data.append(colnames)
        else:
            row_values = extract_txt(row)
            row_values += extract_links(row)
            if len(row_values) == len(colnames):
                data.append(row_values)
    return data


def dailyOICollector():

    #driver = webdriver.Firefox()
    driver = webdriver.PhantomJS()
    driver.implicitly_wait(30)
    _fullurl = URL_PREFIX + "&date=" + DailyOIstd.next_thursdayAt17()
    driver.get(_fullurl)
   # driver.get("http://finance.yahoo.com/quote/SPY/options?ltr=1&straddle=true")
    driver.maximize_window()
    time.sleep(10)

    FullHtml = driver.page_source
    mysoup = BeautifulSoup(FullHtml, "html.parser")
    # num_tables = len(list(mysoup.find_all('table')))
    all_tables = [table for table in mysoup.find_all('table')]
    if not all_tables:
            print ("NO TABLE!")
    lengths = [len(table) for table in all_tables]
    # print ("lengths=",lengths)
    max_length = max(lengths)
    # print ("max_length=", max_length)
    biggest_idx = lengths.index(max_length)
    # print ("biggest_idx=", biggest_idx)

    table = all_tables[biggest_idx]
    table_df = to_dataframe(table)

   # table_df.columns = ['Index', 'ExpirationDate', 'CallsLastPrice', 'CallsChange']

    table_df.insert(0,'ExpirationDate',expirationDate())
    table_df.index.names = ['Index']

    table_df.columns = [
        'ExpirationDate','CallsLastPrice','CallsChange',
        'CallsChangePct','CallsVolume','CallsOI','Strike','PutsLastPrice',
        'PutsChange','PutsChangePct','PutsVolume','PutsOI','last_price_link'
        ,'change_link','change_link','volume_link','open_interest_link','strike_link',
           'last_price_link','change_link','change_link','volume_link','open_interest_link']


    table_df.to_csv(SPYOIFile, sep=',', encoding='utf=8')

# ######################## Main ########################
if __name__ == '__main__':

    dailyOICollector()
