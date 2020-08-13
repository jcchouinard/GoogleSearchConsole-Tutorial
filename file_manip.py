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

import json
import glob
import os
import pandas as pd

from urllib.parse import urlparse

from date_manip import get_dates, date_to_YM

def create_project(directory):
    '''
    Create a project if it does not exist
    '''
    if not os.path.exists(directory):
        print('Create project: '+ directory)
        os.makedirs(directory)
    else:
        print(f'{directory} project exists')

def get_domain_name(start_url):
    '''
    Get Domain Name in the www_domain_com format
    1. Parse URL
    2. Get Domain
    3. Replace dots to make a usable folder path
    '''
    url = urlparse(start_url)               # Parse URL into components
    domain_name = url.netloc                # Get Domain (or network location)
    domain_name = domain_name.replace('.','_')# Replace . by _ to create usable folder
    return domain_name

def write_to_csv(data,filename):
    '''
    Write or append data to a CSV file
    1. If file does not exist...
    2. ... create it using data
    3. If it exists...
    4. Append it without header
    '''
    if not os.path.isfile(filename): 
        data.to_csv(filename, index=False)
    else:
        data.to_csv(filename, mode='a', header=False, index=False)

def get_full_path(site,filename,date):
    '''
    Defines where to export CSVs
    1. Find the folder location...
    2. Merge date and filename to an output...
    3. Merge folder and output
    Returns: www_domain_com/YYYY-MM_filename
    '''
    domain_name = get_domain_name(site)     # Get domain from site URL
    data_path = domain_name + '/' 
    YM_date = get_dates(date)[0]            # Get date as YYYY-MM
    output_path = YM_date + '_' + filename  # Add file location
    output = os.path.join(output_path)      # Merge to create YYYY-MM_filename.csv
    full_path = data_path + output          # Output will be at /your_site_com/YYYY-MM_filename.csv
    return output, domain_name, full_path, data_path

def loop_csv(full_path,filename,start_date):
    '''
    Read all csvs ending with the filename
    Returns: 
    [
        'www_domain_com/2020-04_filename',
        'www_domain_com/2020-05_filename',
        'www_domain_com/2020-06_filename'
    ]
    '''
    date = date_to_YM(start_date)
    file_list = []                          # Initialize empty list
    for file in os.listdir(full_path):      # Check All files in directory
        if file.endswith('_'+ filename):    # Check that it ends with filename
            file_date = file.split('_')[0] 
            if file_date >= date:
                print(f'Checking {file}')
                file_list.append(file)          # Add file to list
                file_list.sort()                # Sort files
    print('Done With loop_csv')
    return file_list

def get_dates_from_csv(path):
    '''
    Read CSV if it exists.
    From CSV, get unique dates.
    '''
    if os.path.isfile(path):
        data = pd.read_csv(path)
        data = pd.Series(data['date'].unique())
        return data
    else:
        pass

def get_dates_csvs(full_path,site,filename,start_date):
    '''
    Get a list of all existing dates.
    1. Check all CSV files in project
    2. Read each CSVs and get unique dates
    3. Combine unique dates from all CSVs in a set
    '''
    print(f'Checking existing dates in {full_path}')
    dset = set()                        # Initialize a set()
    csvs = loop_csv(full_path,filename,start_date) # Read all csvs
    for csv in csvs:                    # For each CSV
        path = os.path.join(full_path + csv)# Get file path
        dates = get_dates_from_csv(path)# Get unique dates
        for date in dates:              # For each date
            dset.add(date)              # Add to a set of unique values
    print('Done getting dates from CSV')
    return dset

def date_to_index(df,datecol):
    '''
    Convert date column of a DF to a datetime index.
    '''
    if df.index.name == datecol:
        if isinstance(df.index, pd.DatetimeIndex):
            print(f'{datecol} is already a datetime index')
        else:
            df[datecol] = pd.to_datetime(df[datecol])
    else:
        df[datecol] = pd.to_datetime(df[datecol])
        df = df.set_index(datecol)
    return df

def csvs_to_df(path,filename):
    '''
    Read all files in path that contains filename
    1. Use glob to get a list of files in directory
    2. Read each file to a dataframe
    3. Concat all dataframes to a unique DF
    '''
    dfs, files = [],[]
    globs = glob.glob(f'{path}/*{filename}')
    for g in globs:
        files.append(g)
    for f in files:
        print(f)
        df = pd.read_csv(f)
        dfs.append(df)
    full_df = pd.concat(dfs)
    return full_df

def return_df(site,filename):
    '''
    From a given URL, find all existing GSC data
    Return them to a unique dataframe.
    '''
    folder = get_domain_name(site)
    df = csvs_to_df(folder,filename)  
    return df