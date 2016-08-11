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
import signal
import sys
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

class Main:
    def __init__(self):
        self.create_workers()
        self.crawl()

    # Create worker threads (will die when main exits)
    def create_workers(self):
        for _ in range(NUMBER_OF_THREADS):
            t = threading.Thread(target=self.work)
            t.daemon = True
            t.start()

    # Do the next job in the queue
    def work(self):
        while True:
            url = queue.get()
            Spider.crawl_page(threading.current_thread().name, url)
            queue.task_done()

    # Each queued link is a new job
    def create_jobs(self):
        for link in file_to_set(QUEUE_FILE):
            queue.put(link)
        queue.join()
        self.crawl()

    #Check if there are items in the queue, if so crawl them
    def crawl(self):
            queued_links = file_to_set(QUEUE_FILE)
            if len(queued_links) > 0:
                print(str(len(queued_links)) + ' links in the queue')
                self.create_jobs()


''' The watcher is a concurrent process (not thread) that 
    waits for a signal and the process that contains the 
    threads.  See Appendix A of The Little Book of Semaphores. 
    http://greenteapress.com/semaphores/ 
'''
class Watcher:  
    def __init__(self):  
        """ Creates a child thread, which returns.  The parent 
            thread waits for a KeyboardInterrupt and then kills 
            the child thread. 
        """  
        self.child = os.fork()  
        if self.child == 0:  
            return  
        else:  
            self.watch()  

    def watch(self):  
        try:  
            os.wait()  
        except KeyboardInterrupt:  
            print '\nKeyBoardInterrupt'  
            self.kill()  
        sys.exit()  
  
    def kill(self):  
        try:  
            os.kill(self.child, signal.SIGKILL)  
        except OSError: pass 


Watcher() 
if __name__ == "__main__":
    main = Main()
