#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs

# Each website is a separate project (folder)
def create_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# Create queue file (if not created)
def create_queue_file(queue_file, base_url):
    queue = os.path.join(queue_file)
    if not os.path.isfile(queue):
        write_file(queue, base_url)

# Create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)

def write_data_to_file(data, file_name):
    with codecs.open(file_name, 'w', 'utf-16') as f:
        for d in data:
            f.write(d + "\n")

# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()


# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_name):
    with open(file_name,"w") as f:
        for l in sorted(links):
            try:
                f.write(l + "\n")
            except Exception as e:
                print("set_to_file: " + str(e))
                print l
