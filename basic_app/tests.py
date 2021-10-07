from django.test import TestCase
from basic_app.management.commands.update_db import extract_data
from basic_app.models import News
from datetime import datetime

# Create your tests here.

class NewTestCase(TestCase):
    def setUp(self):
        News.objects.create(source_web='Mashable', title='Title 1', creation_time=datetime.fromisoformat('2021-10-01 00:00:01.123+00:00'), url='http://url1.com')
        News.objects.create(source_web='The Verge', title='Title 2', creation_time=datetime.fromisoformat('2021-10-02 00:00:02.124+00:00'), url='http://url2.com')
        News.objects.create(source_web='TechCrunch', title='Title 3', creation_time=datetime.fromisoformat('2021-10-03 00:00:03.125+00:00'), url='http://url3.com')
    
    def test_get_all_data(self):
        '''Test the counter with all data that is saved in database'''
        all_database = News.objects.all()
        self.assertEqual(len(all_database),3)
    
    def test_update_counter(self):
        '''Test update_counter method'''
        clicks_list = ['Mashable','Mashable','Mashable','The Verge','The Verge','TechCrunch']
        for value in clicks_list:
            News.objects.get(source_web=value).update_counter()
        self.assertEqual(News.objects.get(source_web='Mashable').clicks_counter,3)
        self.assertEqual(News.objects.get(source_web='The Verge').clicks_counter,2)
        self.assertEqual(News.objects.get(source_web='TechCrunch').clicks_counter,1)
    
    def test_extract_data(self):
        '''Test the extraction data from web pages'''
        full_data = extract_data()
        self.assertGreater(len(full_data),0)
    