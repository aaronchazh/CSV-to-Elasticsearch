# CSV-to-Elasticsearch
Python script to load a csv file into an index in elasticsearch

Requirements:    
Python 2 or 3  
Elasticsearch: https://elasticsearch-py.readthedocs.io/en/master/  
  
Usage:  
Run "python es_csv_loader.py -h" for usage details
  
Examples:  
python es_csv_loader.py test.csv testname testype  
  
python es_csv_loader.py test.csv testname testype -host localhost -num_shards 1 -update True  
  
python es_csv_loader.py test.csv testname testype -host localhost -port 9200 -num_shards 1 -num_replicas 0 -delimiter \t -update True  
