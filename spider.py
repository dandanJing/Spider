#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import urlopen
from html_finder import LinkFinder
from domain import *
from general import *

class Spider:
    base_url = ''
    domain_name = ''
    queue = set()
    crawled = set()

    def __init__(self, base_url, domain_name, queue_file, crawled_file_path):
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = queue_file
        Spider.crawled_file_path = crawled_file_path
        self.boot()

      # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_dir(Spider.crawled_file_path)
        create_queue_file(Spider.queue_file, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

     # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.info().getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print("gather_links: " + str(e))
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
