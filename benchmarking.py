import time
import psutil
from pymongo import MongoClient
from elasticsearch import Elasticsearch, helpers

# Setup MongoDB
mongo_client = MongoClient('mongodb://root:root@localhost:27019')
mongo_db = mongo_client['benchmark_db']
mongo_collection = mongo_db['benchmark_collection']

# Setup Elasticsearch
es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "test_password"),
    verify_certs=False,
    request_timeout=9999
)
index_name = 'benchmark_index'

# Sample Data
num_docs = 10000
small_doc = {"name": "John Doe", "age": 30, "address": "123 Main St"}
large_doc = {"name": "John Doe", "age": 30, "address": "123 Main St", "bio": "x" * 1000000}

def measure_performance(func):
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        
        cpu_usage_before = process.cpu_percent(interval=None)
        mem_usage_before = process.memory_info().rss

        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        cpu_usage_after = process.cpu_percent(interval=None)
        mem_usage_after = process.memory_info().rss

        cpu_usage = cpu_usage_after - cpu_usage_before
        mem_usage = (mem_usage_after - mem_usage_before) / (1024 * 1024)  # Convert to MB

        print(f"{func.__name__} - Time Taken: {end_time - start_time} seconds")
        print(f"{func.__name__} - CPU Usage: {cpu_usage}%")
        print(f"{func.__name__} - Memory Usage: {mem_usage} MB")
        
        return result

    return wrapper

@measure_performance
def bulk_insert_mongo(docs):
    mongo_collection.insert_many(docs)

def bulk_insert_mongo_caller(doc, num_docs):
    docs = []
    for i in range(num_docs):
        temp_doc = doc.copy()
        temp_doc['test'] = 'test' + str(i) + 'abc'
        docs.append(temp_doc)
    bulk_insert_mongo(docs)

@measure_performance
def bulk_insert_es(docs):
    helpers.bulk(es, docs)

def bulk_insert_es_caller(doc, num_docs):
    docs = []
    for i in range(num_docs):
        temp_doc = doc.copy()
        temp_doc['test'] = 'test' + str(i) + 'abc'
        docs.append({"_index": index_name, "_source": temp_doc})
    bulk_insert_es(docs)

@measure_performance
def single_insert_mongo(doc, num_docs):
    for i in range(num_docs):
        temp_doc = doc.copy()
        temp_doc['test'] = 'test' + str(i) + 'abc'
        mongo_collection.insert_one(temp_doc)

@measure_performance
def single_insert_es(doc, num_docs):
    for i in range(num_docs):
        temp_doc = doc.copy()
        temp_doc['test'] = 'test' + str(i) + 'abc'
        es.index(index=index_name, document=temp_doc)

@measure_performance
def search_mongo():
    query_string = {'$regex': '.*346.*'}
    query = {'test': query_string}
    res = mongo_collection.find(query)
    if res:
        print('search_mongo result found')

@measure_performance
def search_es():
    query = {"test": "*346*"}
    res = es.search(index=index_name, body={"query": {"wildcard": query}})
    if res:
        print('search_es result found')

# Clear previous data
mongo_collection.delete_many({})
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
es.indices.create(index=index_name)

# Benchmark Bulk Inserts
print("Bulk Insert - Small Document")
bulk_insert_mongo_caller(small_doc, num_docs)
bulk_insert_es_caller(small_doc, num_docs)

print("\nBulk Insert - Large Document")
bulk_insert_mongo_caller(large_doc, num_docs)
bulk_insert_es_caller(large_doc, num_docs)

# Clear previous data again
mongo_collection.delete_many({})
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
es.indices.create(index=index_name)

# Benchmark Single Inserts
print("\nSingle Insert - Small Document")
single_insert_mongo(small_doc, num_docs)
single_insert_es(small_doc, num_docs)

print("\nSingle Insert - Large Document")
single_insert_mongo(large_doc, num_docs)
single_insert_es(large_doc, num_docs)

# Benchmark Search Operations
print("\nSearch Operation")
search_mongo()
search_es()
