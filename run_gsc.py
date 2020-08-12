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

from dateutil import relativedelta

from gsc_by_url import gsc_by_url
from gsc_with_filters import gsc_with_filters
from gsc_to_csv_by_month import gsc_to_csv
from oauth import authorize_creds, execute_request

site = 'https://www.jcchouinard.com'# Property to extract              
creds = 'client_secrets.json'       # Credential file from GSC
output = 'gsc_data.csv'
start_date = '2020-07-01'      

webmasters_service = authorize_creds(creds) 


list_of_urls = ['/chrome-devtools-commands-for-seo/','/learn-selenium-python-seo-automation/']
list_of_urls = [site + x for x in list_of_urls]
args = webmasters_service,site,list_of_urls,creds,start_date
gsc_by_url(*args)


# Filters
dimension = 'query'     # query, page
operator = 'contains'   # contains, equals, notEquals, notContains
expression = 'python'   # whatever value that you want
args = webmasters_service,site,creds,dimension,operator,expression,start_date

gsc_with_filters(*args)

args = webmasters_service,site,output,creds,start_date
gsc_to_csv(*args)