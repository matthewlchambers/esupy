# remote.py (esupy)
# !/usr/bin/env python3
# coding=utf-8
"""
Functions for handling remote requests and parsing
"""
import logging as log
import requests
import requests_ftp
from urllib.parse import urlsplit


def make_url_request(url, *, params=None, set_cookies=False):
    """
    Makes http request using requests library
    :param url: URL to query
    :return: request Object
    """
    session = (requests_ftp.ftp.FTPSession if urlsplit(url).scheme == 'ftp'
               else requests.Session)
    with session() as s:
        try:
            # The session object s preserves cookies, so the second s.get()
            # will have the cookies that came from the first s.get()
            if set_cookies:
                s.get(url, params=params)
            response = s.get(url, params=params)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            log.error("URL Connection Error for %s", url)
        except requests.exceptions.HTTPError:
            log.error('Error in URL request!')
    return response


# Alias for backward compatibility
def make_http_request(url):
    log.warning('esupy.remote.make_http_request() has been renamed to '
                'esupy.remote.make_url_request(). '
                'esupy.remote.make_http_request() will be removed in the '
                'future. Please modify your code accordingly.')
    return make_url_request(url)
