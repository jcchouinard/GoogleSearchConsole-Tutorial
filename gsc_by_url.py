'''
@author:    Jean-Christophe Chouinard. 
@role:      Sr. SEO Specialist at SEEK.com.au
@website:   jcchouinard.com
@LinkedIn:  linkedin.com/in/jeanchristophechouinard/ 
@Twitter:   twitter.com/@ChouinardJC

Learn Python for SEO
jcchouinard.com/python-for-seo

Get API Keys
jcchouinard.com/how-to-get-google-search-console-api-keys/

How to format your request
jcchouinard.com/what-is-google-search-console-api/
'''
# Standard library imports
import pandas as pd

# Third party modules imports
from collections import defaultdict
import datetime
from dateutil import relativedelta

# Local modules imports
from date_manip import date_to_str
from oauth import authorize_creds, execute_request

'''
Initialize default end_date.
Set 3 days in the past.
GSC doesn't allow more recent dates.
This'll be used when end_date is not defined.
'''
today = datetime.date.today()
days = relativedelta.relativedelta(days=3)
default_end = today - days 

def gsc_by_url(site,list_of_urls,creds,start_date,end_date=default_end):
    '''
    Extracts clicks and impressions from a list of URLs.
    '''
    # Authorize credentials to log in the API
    ws = authorize_creds(creds) 

    # Make sure dates are in string format
    start_date = date_to_str(start_date)
    end_date = date_to_str(end_date)

    # Initialize empty dictionary
    scDict = defaultdict(list)

    for url in list_of_urls:    # For each URL
        '''
        Request Format
        jcchouinard.com/what-is-google-search-console-api/
        '''
        request = {
                    'startDate': start_date,
                    'endDate': end_date,
                    'dimensionFilterGroups': [{
                    'filters': [{
                        'dimension': 'page',              
                        'operator': 'equals',           #contains, equals, notEquals, notContains
                        'expression': url
                    }]
                    }]
            }
        response = execute_request(ws, site, request)
        scDict['page'].append(url)
        try:
            for row in response['rows']:
                scDict['clicks'].append(row['clicks'] or 0)
                scDict['impressions'].append(row['impressions'] or 0)
        except Exception as e:
            print(f'An error occurred while extracting {url}: {e}')
    # Add response to dataframe 
    df = pd.DataFrame(data = scDict)
    return df