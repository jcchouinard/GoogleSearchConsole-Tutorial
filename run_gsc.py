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

from oauth import authorize_creds, execute_request

site = 'https://www.jcchouinard.com'# Property to extract              
creds = 'client_secrets.json'       # Credential file from GSC
output = 'gsc_data.csv'
start_date = '2020-07-01'       


from gsc_by_url import gsc_by_url

list_of_urls = ['/chrome-devtools-commands-for-seo/','/learn-selenium-python-seo-automation/']
list_of_urls = [site + x for x in list_of_urls]

gsc_by_url(site,list_of_urls,creds,start_date)


from gsc_with_filters import gsc_with_filters
'''
1. Export Daily Datafiltering for "Python" Queries
'''
gsc_with_filters(site,creds,start_date)


from gsc_to_csv_by_month import gsc_to_csv
'''
1. Create Folder Using Property Name
2. Extract all Google Search Console Data
3. Export to CSV by Month
'''
gsc_to_csv(site,output,creds,start_date)