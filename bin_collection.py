import unittest
import urllib.request
from icalendar import Calendar


class TestBinCollection(unittest.TestCase):
    
    def setUp(self):
        '''Download test data'''
        self.collection = BinCollection()
        self.collection.download(
        'https://s3-eu-west-1.amazonaws.com/fs-downloads/GM/binfeed.ical')

    def test_summary_missing_date(self):
        '''Test with missing date'''
        self.assertEqual(self.collection.summary('2019-03-20'),
                         'No collection on that date.')

    def test_summary_incorrect_date(self):
        '''Test with date badly formatted'''
        self.assertEqual(self.collection.summary('20180320'),
                         'No collection on that date.')
        
    def test_summary(self):
        '''Test with 2 events on date'''
        self.assertEqual(self.collection.summary('2018-02-06'),
                         'Blue Bin Collection. Green Bin Collection')

    def test_summary__for_ymd(self):
        '''Test with 1 event on date'''
        self.assertEqual(self.collection.summary_for_ymd(2017, 12, 28),
                         'Blue Bin Collection (rescheduled)')

        
    def test_summary_for_ymd2(self):
        '''Test with 2 events on date'''
        self.assertEqual(self.collection.summary_for_ymd(2018, 2, 6),
                         'Blue Bin Collection. Green Bin Collection')
        

class BinCollection:
    def __init__(self):
        '''Initialise dictionary to hold collection data'''
        self.cal_dict = {}

    def download(self, url):
        '''Download data and rewrite dictionary'''
        ##
        ## download data directly to memory
        ##
        with urllib.request.urlopen(url) as f:
            data = f.read().decode('utf-8')
        ##
        ## parse data into a Calendar object
        ##
        cal = Calendar.from_ical(data)
        ##
        ## Clear dictionary and reload.
        ## Only the start date and the summary text are retained,
        ## the dictionary is indexed on the start date as a string
        ## in the form YYYY-MM-DD. If there are several events on
        ## a single day the summary texts are concatenated.
        ##
        self.cal_dict = {}
        for event in cal.walk('vevent'):
            start_date = str(event['DTSTART'].dt)
            summary = str(event['SUMMARY'])
            if start_date in self.cal_dict:
                prev_summary = self.cal_dict[start_date]
                self.cal_dict[start_date] = prev_summary + '. ' + summary
            else:
                self.cal_dict[start_date] = summary
        
            
    def summary(self, date):
        '''return summary for a date as 'YYYY-MM_DD'''
        if date in self.cal_dict:
            return(self.cal_dict[date])
        else:
            ##
            ## If the date is not present in
            ## the dictionary report no collection.
            ##
            return('No collection on that date.')
        

    def summary_for_ymd(self, year, month, day):
        '''return summary for a date as integer year, month and day''' 
        return(self.summary('%4.4d-%02.2d-%02.2d' % (year, month, day)))
        

if __name__ == '__main__':
    unittest.main()
