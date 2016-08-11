#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         main
# Purpose:      Main function for calling all spider modules
#
# Author:      Dandan
#
# Created:     11/08/2016
# -------------------------------------------------------------------------------

import threading
import Queue
from spider import Spider
from domain import *
from general import *

CRAWLED_FILE_PATH = 'CrawledFiles'
QUEUE_FILE = 'queue.txt'
BASE_URL = 'http://www.xinhuanet.com/'
DOMAIN_NAME = get_domain_name(BASE_URL)
NUMBER_OF_THREADS = 8

queue = Queue.Queue()
Spider(BASE_URL, DOMAIN_NAME, QUEUE_FILE, CRAWLED_FILE_PATH)

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()

#Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

if __name__ == "__main__":
    try:
        create_workers()
        crawl()
    except KeyboardInterrupt, e:
        print '\nBreak out.'
        sys.exit()
