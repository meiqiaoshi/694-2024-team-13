# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# lru_cache.py
import json
from collections import OrderedDict
import time
from bson import ObjectId
from datetime import datetime


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        elif isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime objects to ISO 8601 string
        return super(JSONEncoder, self).default(obj)


class LRUCache:
    def __init__(self, capacity, ttl, persistence_path):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.ttl = ttl
        self.persistence_path = persistence_path

    def get(self, key):
        if key in self.cache and not self.is_expired(key):
            self.cache.move_to_end(key)
            return self.cache[key]['data']
        return None

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = {'data': value, 'timestamp': time.time()}
        if len(self.cache) > self.capacity:
            oldest = next(iter(self.cache))
            del self.cache[oldest]

    def is_expired(self, key):
        return (time.time() - self.cache[key]['timestamp']) > self.ttl

    def persist(self):
        with open(self.persistence_path, 'w') as f:
            json.dump(self.cache, f, cls=JSONEncoder)  # Use the custom encoder

    def restore(self):
        try:
            with open(self.persistence_path, 'r') as f:
                # Check if file is empty
                content = f.read()
                if not content:
                    print("Cache file is empty, starting with an empty cache.")
                    return

                # If not empty, load the content
                loaded_cache = json.loads(content)
                self.cache = OrderedDict(
                    (k, {'data': v['data'], 'timestamp': v['timestamp']}) for k, v in loaded_cache.items())
        except FileNotFoundError:
            print("Cache file not found, starting with an empty cache.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            # Handle corrupted JSON by initializing an empty cache
            self.cache = OrderedDict()

    def print_cache(self):
        print("Cache contents:")
        for key, value in self.cache.items():
            print(
                f"Key: {key}, Data: {value['data']}, Timestamp: {value['timestamp']}, Age: {time.time() - value['timestamp']:.2f} seconds")


# Instantiate the cache
cache = LRUCache(capacity=100, ttl=3600, persistence_path='cache.json')
cache.restore()
