#!/usr/bin/env python
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import urlparse
import re

class HTMLHanlder(HTMLParser):

    def __init__(self, base_url, page_url):
        HTMLParser.__init__(self) 
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()
        self.datas = set()

    # When we call HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = value
                    mt = re.match(r'(http://www|www|https://www)\.[a-z0-9-]*\.([a-z]{2,3}|com\.cn)', value, re.I)
                    if not mt:
                        url = urlparse.urljoin(self.base_url, value)
                    self.links.add(url)

    def handle_data(self, data):
        mt = re.findall(ur"([\u4e00-\u9fa5]+).+", data)
        for val in mt:
            if len(val) > 1:
                self.datas.add(val)

    def page_links(self):
        return self.links

    def error(self, message):
        pass
