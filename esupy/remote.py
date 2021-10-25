# remote.py (esupy)
# !/usr/bin/env python3
# coding=utf-8
"""
Functions for handling remote requests and parsing
"""
import logging as log
import requests
# This code exists because requests_ftp is only required for downloading data to create FBA datasets, so 
# if it's not available, I want to be able to do other things.
try:
    import requests_ftp
except ModuleNotFoundError as e:
    print(f'{str(e)}, so downloading data to create Flow-By-Activity datasets will not be possible.')
    

def make_http_request(url):
    """
    Makes http request using requests library
    :param url: URL to query
    :return: request Object
    """
    r = []
    try:
        r = requests.get(url)
    except requests.exceptions.InvalidSchema: # if url is ftp rather than http
        requests_ftp.monkeypatch_session()
        r = requests.Session().get(url)
    except requests.exceptions.ConnectionError:
        log.error("URL Connection Error for " + url)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        log.error('Error in URL request!')
        r = None
    return r

