#!/usr/bin/env python
""" Date Manipulations Functions
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
"""

import datetime
import pandas as pd
import re 

from dateutil import relativedelta

def date_to_str(date):
    '''Convert date to a string: "YYYY-MM-DD"'''
    cond_1 = isinstance(date, datetime.datetime)    
    cond_2 = isinstance(date, datetime.date)
    if cond_1 or cond_2:    # If date is datetime or date object
        date = datetime.datetime.strftime(date,'%Y-%m-%d') # Convert to string
    return date

def str_to_date(date):
    '''
    Convert string to a datetime object
    Returns: datetime.datetime(2020, 6, 1, 0, 0)
    '''
    if isinstance(date, str):
        date = datetime.datetime.strptime(date,'%Y-%m-%d')
    return date

def date_to_YM(date):
    '''
    Convert date to get Year and Month as a string.
    Returns: "YYYY-MM"
    '''
    dt = str_to_date(date)
    return datetime.datetime.strftime(dt,'%Y-%m')

def list_dates(startDate,endDate):
    '''List dates between two dates'''
    start_date = str_to_date(startDate) # Get startDate as a datetime object
    end_date = str_to_date(endDate)     # Get endDate as a datetime object
    delta = end_date - start_date       # Show difference as a timedelta object: datetime.timedelta(days=31)
    days = []                           # Initialize empty list
    for i in range(delta.days):         # For each day in .timedelta(days=n)      
        timedelta = datetime.timedelta(days=i) # Create a delta: 1 day, 2 days, ...
        day = start_date + timedelta    # Add delta to start_date: datetime.datetime(2020, 5, 1, 0, 0) + 1 day = datetime.datetime(2020, 5, 2, 0, 0) 
        day = date_to_str(day)          # Convert the datetime object to a string: "2020-05-02"
        days.append(day)                # Add the date to the list
    return days                         # Returns a list ['2020-05-01','2020-05-02', ...]

def get_dates(chosen_date):
    '''
    Get days since the beginning of the month.
    If date is not defined, use current month,
    else use month of the specified date.
    '''
    today = datetime.datetime.now()
    days = relativedelta.relativedelta(days=3) # GSC does not permit date earlier than 3 days
    end_date = today - days  
    if chosen_date is '': 
        delta = end_date - today.replace(day=1) # Get first day of the month
        start_date = end_date - delta # count difference between end date and first day of the month
    else:
        delta = end_date - datetime.datetime.strptime(chosen_date,'%Y-%m-%d') # Get first day of the month
        start_date = end_date - delta # count difference between end date and first day of the month
    YM_date = date_to_YM(start_date)
    return YM_date, start_date, end_date