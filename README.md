### Below are the results of benchmarking insert and select operations for Mongo vs Elastic search:
- Bulk Insert - Small Document (10k documents)
  - bulk_insert_mongo - Time Taken: 0.13041257858276367 seconds
  - bulk_insert_mongo - CPU Usage: 37.5%
  - bulk_insert_mongo - Memory Usage: 2.57421875 MB
  - bulk_insert_es - Time Taken: 1.253598928451538 seconds
  - bulk_insert_es - CPU Usage: 0.0%
  - bulk_insert_es - Memory Usage: 0.75 MB

- Bulk Insert - Large Document (10k documents)
  - bulk_insert_mongo - Time Taken: 163.25115442276 seconds
  - bulk_insert_mongo - CPU Usage: 7.8%
  - bulk_insert_mongo - Memory Usage: 0.3984375 MB
  - bulk_insert_es - Time Taken: 444.67868208885193 seconds
  - bulk_insert_es - CPU Usage: 14.7%
  - bulk_insert_es - Memory Usage: -0.28515625 MB

- Single Insert - Small Document (10k documents)
  - single_insert_mongo - Time Taken: 11.238045692443848 seconds
  - single_insert_mongo - CPU Usage: 1.7%
  - single_insert_mongo - Memory Usage: 0.0 MB
  - single_insert_es - Time Taken: 157.06708359718323 seconds
  - single_insert_es - CPU Usage: 0.9%
  - single_insert_es - Memory Usage: 0.04296875 MB

- Single Insert - Large Document (10k documents)
  - single_insert_mongo - Time Taken: 193.7089102268219 seconds
  - single_insert_mongo - CPU Usage: 1.3%
  - single_insert_mongo - Memory Usage: 0.87109375 MB
  - single_insert_es - Time Taken: 464.64608240127563 seconds
  - single_insert_es - CPU Usage: 1.9%
  - single_insert_es - Memory Usage: -0.00390625 MB

- Search Operation
  - search_mongo result found
  - search_mongo - Time Taken: 0.0 seconds
  - search_mongo - CPU Usage: 0.0%
  - search_mongo - Memory Usage: 0.0 MB
  - search_es result found
  - search_es - Time Taken: 2.0441648960113525 seconds
  - search_es - CPU Usage: 0.0%
  - search_es - Memory Usage: 8.55078125 MB
