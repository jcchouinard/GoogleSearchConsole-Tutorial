#!/usr/bin/env python
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

import argparse
import os
import pandas as pd
import re
import time

from collections import defaultdict
import datetime
from datetime import date, timedelta
from dateutil import relativedelta

import date_manip as dm
import file_manip as fm
from oauth import authorize_creds, execute_request

'''
Initialize default end_date.
Set 3 days in the past.
GSC doesn't allow more recent dates.
This'll be used when end_date is not defined.
'''                     
today = datetime.datetime.now()
days = relativedelta.relativedelta(days=3)
default_end = today - days 

# Create function to extract all the data
def gsc_to_csv(webmasters_service,site,output,creds,start_date,end_date=default_end,gz=False):
    '''
    Extract 100% of the data from Google Search Console.
    Checks output folder if dates are already extracted.
    Dates that are already extracted are skipped.
    Day by day, it requests lines by batch of 25K.
    It iterates until all lines are extracted for that day.
    New dates are appended to the existing CSV
    '''
    print(f'gsc_to_csv gz: {gz}')
    get_path = fm.get_full_path(site,output,start_date)
    domain_name = get_path[1]                       # Get Domain From URL
    output_path = get_path[3]                       # Folder created with your domain name
    fm.create_project(domain_name)                  # Create a new project folder
    csv_dt = fm.get_dates_csvs(site,output,start_date,gz=gz)# Read existing CSVs

    # Set up Dates
    dates = dm.get_dates(start_date)
    start_date = dates[1]                           # Start first day of the month.
    end_date = dm.str_to_date(end_date)                # End 3 days in the past, since GSC don't show latest data.
    delta = datetime.timedelta(days=1)              # This will let us loop one day at the time
    scDict = defaultdict(list)                      # initialize empty Dict to store data
    while start_date <= end_date:                   # Loop through all dates until start_date is equal to end_date.
        curr_month = dm.date_to_YM(start_date)
        full_path = os.path.join(output_path + curr_month + '_' + output)
        # If a GSC csv file exists from previous extraction
        # and dates in the file match to dates we are extracting...
        if csv_dt is not None and \
            dm.date_to_str(start_date) in csv_dt:
            print('Existing Date: %s' % start_date) #... Print the date
            start_date += delta                     #... and increment without extraction  
        else:                                       # If the file doesn't exist, or date don't match...
            # ... Print and start the extraction
            print('Start date at beginning: %s' % start_date)

            maxRows = 25000 # Maximum 25K per call 
            numRows = 0     # Start at Row Zero
            status = ''     # Initialize status of extraction

            while (status != 'Finished') : # As long as today's data have not been fully extracted.
                # Extract this information from GSC
                dt = dm.date_to_str(start_date)
                print(f'date = {dt}')
                request = {
                    'startDate': dt,                        # Get today's date (while loop)
                    'endDate': dt,                          # Get today's date (while loop)
                    'dimensions': ['date','page','query'],  # Extract This information
                    'rowLimit': maxRows,                    # Set number of rows to extract at once (max 25k)
                    'startRow': numRows                     # Start at row 0, then row 25k, then row 50k... until with all.
                }
                response = execute_request(webmasters_service, site, request)
                #Process the response
                try:
                    for row in response['rows']:
                        scDict['date'].append(row['keys'][0] or 0)    
                        scDict['page'].append(row['keys'][1] or 0)
                        scDict['query'].append(row['keys'][2] or 0)
                        scDict['clicks'].append(row['clicks'] or 0)
                        scDict['ctr'].append(row['ctr'] or 0)
                        scDict['impressions'].append(row['impressions'] or 0)
                        scDict['position'].append(row['position'] or 0)
                    print('successful at %i' % numRows)

                except:
                    print('error occurred at %i' % numRows)

                # Add response to dataframe 
                df = pd.DataFrame(data = scDict)
                df['clicks'] = df['clicks'].astype('int')
                df['ctr'] = df['ctr']*100
                df['impressions'] = df['impressions'].astype('int')
                df['position'] = df['position'].round(2)

                # Increment the 'start_row'
                print('Numrows at the start of loop: %i' % numRows)
                try: 
                    numRows = numRows + len(response['rows'])
                except:
                    status = 'Finished'                 # If no response left, change status
                print('Numrows at the end of loop: %i' % numRows)
                if numRows % maxRows != 0:              # If numRows not divisible by 25k...
                    status = 'Finished'                 # change status, you have covered all lines.                
            #print(f'DF to write {df.head()}')
            to_write = df[df['date'].str.contains(dm.date_to_str(start_date))]
            if gz == False:
                fm.write_to_csv(to_write,full_path)
            elif gz == True:
                fm.write_to_csv_gz(to_write,full_path)
            start_date += delta                         # Increment start_date to continue the loop
    print(f'Done extracting {site}')