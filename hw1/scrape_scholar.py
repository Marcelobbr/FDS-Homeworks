#!/usr/bin/env python
# coding: utf-8

# * download chrome driver, stable release win-32: http://chromedriver.chromium.org/
# * unzip and move it to C:\Windows
# * more: https://sites.google.com/a/chromium.org/chromedriver/getting-started

# In[3]:


from splinter import Browser
from bs4 import BeautifulSoup
import requests
#import re
import time
#import pandas as pd
#import sqlite3
#import matplotlib.pyplot as plt
#import networkx as nx


# # google scholar navigation
executable_path = {'executable_path':r'C:\Windows\chromedriver.exe'}
# In[4]:


def scrape(name):
    #with Browser('chrome', **executable_path) as browser:
    # Visit URL
    browser = Browser(driver_name='chrome', headless=True) #headless=False will show the browser navigation
    url = "https://scholar.google.com.br/"
    browser.visit(url)
    browser.fill('q', 'Jeffrey Heer')

    # Find and click the 'search' button
    button = browser.find_by_name('btnG')
    time.sleep(1) # needs to sleep for the button to become active
    button.click()

    # Find and click the first link
    button = browser.find_link_by_partial_href('citations?user=')
    time.sleep(1)
    button.click()
    
    #expand the page
    button = browser.find_by_id('gsc_bpf_more')    
    check_button = browser.evaluate_script('document.getElementById("gsc_bpf_more").disabled')
    while check_button == False:
        time.sleep(1)
        check_button = browser.evaluate_script('document.getElementById("gsc_bpf_more").disabled')
        button.click()

    #get html
    return browser.html

