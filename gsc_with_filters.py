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

import pandas as pd

from collections import defaultdict
import datetime
from dateutil import relativedelta

from date_manip import date_to_str
from oauth import authorize_creds, execute_request

today = datetime.date.today()
days = relativedelta.relativedelta(days=3)
default_end = today - days 

# Run the extraction
def gsc_with_filters(site,creds,start_date,end_date=default_end):

    scDict = defaultdict(list) # Create a dict to populate with extraction
    webmasters_service = authorize_creds(creds) # Authorize the API
    request = {
        'startDate': date_to_str(start_date),
        'endDate': date_to_str(end_date),
        'dimensions': ['date','page','query'],  #country, device, page, query, searchAppearance
        'dimensionFilterGroups': [{
                        'filters': [{
                            'dimension': 'query',              
                            'operator': 'contains',           #contains, equals, notEquals, notContains
                            'expression': 'python'
                        }]
                        }]
    }
    print(request)
    response = execute_request(webmasters_service, site, request)
    print(response)
    try:
        for row in response['rows']:
            scDict['date'].append(row['keys'][0] or 0)    
            scDict['page'].append(row['keys'][1] or 0)
            scDict['query'].append(row['keys'][2] or 0)
            scDict['clicks'].append(row['clicks'] or 0)
            #scDict['ctr'].append(row['ctr'] or 0)
            #scDict['impressions'].append(row['impressions'] or 0)
            #scDict['position'].append(row['position'] or 0)
    except Exception as e:
        print(f'An error occurred: {e}')

    # Add response to dataframe 
    df = pd.DataFrame(data = scDict)
    return df
