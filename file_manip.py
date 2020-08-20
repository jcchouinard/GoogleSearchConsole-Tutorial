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
import gzip
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

def write_to_csv_gz(data,filename):
    '''
    Write or append data to a CSV file
    1. If file does not exist...
    2. ... create it using data
    3. If it exists...
    4. Append it without header, compressed.
    '''
    filename = filename + '.gz'
    if not os.path.isfile(filename):
        print(f'Creating: {filename}')
        data.to_csv(filename, index=False, compression='gzip')
    else: # else it exists so append without writing the header
        print(f'Appending to: {filename}')
        with gzip.open(filename, 'at') as compressed_file:
            data.to_csv(compressed_file, header=False, index=False)

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
    listdir = os.listdir(full_path)
    for file in listdir:                    # Check All files in directory
        if file.endswith('_'+ filename):    # Check that it ends with filename
            file_date = file.split('_')[0] 
            if file_date >= date:
                print(f'Checking {file}')
                file_list.append(file)          # Add file to list
                file_list.sort()                # Sort files
    return file_list

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

def read_csv_list(path,gz=False):
    '''
    Read CSV if it exists.
    If gz=True, use the compression parameter.
    '''
    if os.path.isfile(path):
        print(f'Reading {path} to CSV')
        if gz == True:
            data = pd.read_csv(path,compression='gzip')
        else:
            data = pd.read_csv(path)
        return data
    else:
        pass

def read_csvs(full_path,site,filename,start_date,gz=False):
    '''
    Get a list of all existing dates.
    1. Check all CSV files in project
    2. Read each CSVs and get unique dates
    3. Combine unique dates from all CSVs in a set
    '''
    if gz == True:
        filename = filename + '.gz'
    print(f'Checking CSVs in {full_path}')
    dfs = []                                        # Initialize a set()
    csvs = loop_csv(full_path,filename,start_date)  # Read all csvs

    if not csvs:
        print('No CSV to read')
        df = pd.DataFrame()
    else:
        for csv in csvs:
            path = os.path.join(full_path + csv)    # Get file path
            df = read_csv_list(path,gz=gz)          # Get unique dates
            dfs.append(df)                          # Add to a set of unique values
        df = pd.concat(dfs)
    print('Done extracting DF from CSVs')
    return df

def get_dates_csvs(site,output,start_date,gz=False):
    '''
    Get a list of all unique existing dates in a set.
    '''
    #print(f'Checking existing dates in {}')
    df = csvs_to_df(site,output,start_date,gz=gz)
    if df.empty:
        return None
    else:
        dset = set(df['date'])
        #print('Done getting dates from CSV')
        return dset
    
def csvs_to_df(site,output,start_date,gz=False):
    '''
    Read all CSVs containing the output name after a specified date.
    '''
    get_path = get_full_path(site,output,start_date)
    output_path = get_path[3]
    df = read_csvs(output_path,site,output,start_date,gz=gz)
    return df