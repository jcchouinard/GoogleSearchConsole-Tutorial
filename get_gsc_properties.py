#!/usr/bin/env python
'''
Retrieve a list of validated properties from Google Search Console.
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

from oauth import authorize_creds, execute_request

creds = 'client_secrets.json'

webmasters_service = authorize_creds(creds) 

site_list = webmasters_service.sites().list().execute()

# Filter for verified websites
verified_sites_urls = [s['siteUrl'] for s in site_list['siteEntry']
                       if s['permissionLevel'] != 'siteUnverifiedUser'
                          and s['siteUrl'][:4] == 'http']

