#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
import time
from bs4 import BeautifulSoup
import requests
import re

###################################################
#                   PART 1
###################################################
def scrape(author):
    print("\nRETRIEVING DATA FOR:", author, "\n")
    print("\nINITIALIZING CRAWLER\n")
    # Visit URL
    browser = Browser(driver_name='chrome', headless=True) #headless=False will show the browser navigation
    url = "https://scholar.google.com.br/"
    browser.visit(url)
    browser.fill('q', author)

    # Find and click the 'search' button
    button = browser.find_by_name('btnG')
    time.sleep(1) # needs to sleep for the button to become active
    button.click()

    # If the profile doesn't exist, stop.    
    profile_check = browser.html
    if "feather-72.png" not in profile_check:
        print("\nERROR: PROFILE DOES NOT EXIST. PLEASE CHECK YOUR QUERY OR TYPE ANOTHER NAME.\n")
        return
    
    # Find and click the first link (if profile exists).
    button = browser.find_link_by_partial_href('citations?user=')
    time.sleep(1)
    button.click()
    
    #expand the page until button is disabled
    button = browser.find_by_id('gsc_bpf_more')    
    check_button = browser.evaluate_script('document.getElementById("gsc_bpf_more").disabled')
    while check_button == False:
        time.sleep(1)
        check_button = browser.evaluate_script('document.getElementById("gsc_bpf_more").disabled')
        button.click()

    #get html
    #return browser.html
    soup = BeautifulSoup(browser.html, 'html.parser')
    soup.findAll("td", {"class": "gsc_a_t"})

    print("\nBUILDING PAPERS DICIONARY.\n")
    papers = []
    table = soup.find("table", id="gsc_a_t") 
    for tr in table.find_all('tr')[2:]:
        for td in tr.find_all("td", {"class": "gsc_a_t"}):
            paper = {}
            text = re.sub("[\'\"]", "", tr.find("a", {"class": "gsc_a_at"}).get_text()).strip() # evita erro de sintaxe no sql
            paper['title'] = text
            authors = tr.find("div", {"class": "gs_gray"}).get_text().split(',')[:4]
            authors = [a.strip().upper() for a in authors] #remove espaçamento antes de alguns nomes e resolve case sensitiveness
            authors = [re.sub("[\'\"]", "", a) for a in authors] # evita erro de sintaxe no sql
            paper['authors'] = authors
            papers.append(paper)
    return papers