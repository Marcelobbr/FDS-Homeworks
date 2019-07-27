#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
import time

# # google scholar navigation 
def scrape(author):
    # Visit URL
    browser = Browser(driver_name='chrome', headless=False) #headless=False will show the browser navigation
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
        print("profile does not exist")
        return
    
    # Find and click the first link (if profile exists).
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
    
