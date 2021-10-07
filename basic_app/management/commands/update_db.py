import time
import requests
import pytz
from datetime import datetime
from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
from basic_app.models import News


def convert_date(web_page_of_origin,date_value,datetime_format_string):
    '''Convert the different types of date to a datetime.datetime value'''
    datetime_value = datetime.strptime(date_value, datetime_format_string)
    utc_datetime_value = datetime_value.astimezone(pytz.utc)

    return utc_datetime_value

class NewsWebPageTags():

    def __init__(self, title_tag = str, url_tag = str, creation_time_tag = str) -> None:
        self.title_tag = title_tag
        self.url_tag = url_tag
        self.creation_time_tag = creation_time_tag

class NewsWebPage(NewsWebPageTags):

    def __init__(self, name: str, url: str, title_tag = str, url_tag = str, creation_time_tag = str, datetime_format_string = str, xml_levels = int) -> None:
        NewsWebPageTags.__init__(self, title_tag, url_tag, creation_time_tag)
        self._name = name
        self._url = url
        self._datetime_format_string = datetime_format_string
        self._xml_levels = xml_levels

    @property
    def name(self) -> str:
        '''Get name of NewsWebPage'''
        return self._name

    @name.setter
    def name(self, name) -> None:
        '''Set name to NewsWebPage'''
        self._name = name

    @property
    def url(self) -> str:
        '''Get url of NewsWebPage'''
        return self._url
    
    @url.setter
    def url(self, url) -> None:
        '''Set url to NewsWebPage'''
        self._url = url
    
    @property
    def datetime_format_string(self) -> str:
        '''Get datetime format of NewsWebPage'''
        return self._datetime_format_string
    
    @datetime_format_string.setter
    def datetime_format_string(self, datetime_format_string) -> None:
        '''Set datetime format to NewsWebPage'''
        self._datetime_format_string = datetime_format_string

    @property
    def xml_levels(self) -> int:
        '''Get xml levels of NewsWebPage'''
        return self._xml_levels
    
    @xml_levels.setter
    def xml_levels(self, xml_levels) -> None:
        '''Set xml levels to NewsWebPage'''
        self._xml_levels = xml_levels

    @property
    def tags(self) -> dict:
        '''Get tags of NewsWebPage'''
        return {self.title_tag: 'title', self.url_tag: 'url', self.creation_time_tag: 'creation_time'}
    
    @property
    def default_single_data(self) -> dict:
        '''Get initial dictionary for prepare single data in order to analyze it'''
        return {'source_web': self.name}

def get_children(fathers):
    '''Get children list from fathers obtained by XML extraction'''
    children_list = []
    for father in fathers:
        children = father.getchildren()
        children_list.extend(children)
    return children_list

def add_data_to_full_data(data, web_page, elements):
    '''Add single data to full data'''
    single_data = web_page.default_single_data.copy()
    for element in elements:
        if element.tag in web_page.tags:
            single_data[web_page.tags[element.tag]] = element.text
    if len(single_data) == 4:
        single_data['creation_time'] = convert_date(single_data['source_web'],single_data['creation_time'],web_page.datetime_format_string)
        data.append(single_data.copy())
        return data

def extract_data():
    '''Download and prepare data from the origin web pages'''
    news_web_pages = [
        NewsWebPage('Mashable','https://mashable.com/feeds/rss/tech','title','link','pubDate','%a, %d %b %y %H:%M:%S %z',2), # Mon, 27 Sep 21 21:53:56 +0000
        NewsWebPage('The Verge','https://www.theverge.com/rss/tech/index.xml','{http://www.w3.org/2005/Atom}title','{http://www.w3.org/2005/Atom}id','{http://www.w3.org/2005/Atom}published','%Y-%m-%dT%H:%M:%S%z',1), # 2021-10-02T09:30:00-04:00
        NewsWebPage('TechCrunch','https://techcrunch.com/feed/','title','link','pubDate','%a, %d %b %Y %H:%M:%S %z',2) # Fri, 01 Oct 2021 21:50:17 +0000
    ]

    full_data = []

    for web_page in news_web_pages:
        web_page_url = web_page.url
        response = requests.get(web_page_url)
        root = ET.fromstring(response.text)
        elements = root.getchildren()
        for counter in range(web_page.xml_levels):
            elements = get_children(elements)
        full_data = add_data_to_full_data(full_data,web_page,elements).copy()
    
    return full_data

def update_news(actual_data):
    '''Save to database the new news'''
    for single_actual_data in actual_data:
        obj, created = News.objects.get_or_create(
            source_web = single_actual_data['source_web'],
            title = single_actual_data['title'],
            creation_time = single_actual_data['creation_time'],
            url = single_actual_data['url']
        )

def load_data():
    '''Proceed to update the database'''
    actual_data = extract_data()
    update_news(actual_data)


class Command(BaseCommand):
    help = 'Update the database'

    def handle(self, *args, **options):
        while True:
            time.sleep(300)
            load_data()
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            message = 'Current Time = ' + current_time + ' ----> Successfully updated database'
            self.stdout.write(self.style.SUCCESS(message))
