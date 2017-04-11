# CSV-to-Elasticsearch
Python script to load a csv file into an index in elasticsearch

Requirements:    
Python 2 or 3  
Elasticsearch: https://elasticsearch-py.readthedocs.io/en/master/  
  
Usage:    
usage: es_csv_loader.py [-h] [-host HOST] [-port PORT]
                        [-num_shards NUM_SHARDS] [-num_replicas NUM_REPLICAS]
                        [-delimiter DELIMITER] [-update UPDATE]
                        file_path index_name type_name

positional arguments:
  file_path             path to the file
  index_name            name of index to be created
  type_name             name of type

optional arguments:
  -h, --help            show this help message and exit
  -host HOST            host name of machine running Elasticsearch
                        [default=localhost]
  -port PORT            port of machine running Elasticsearch [default=9200]
  -num_shards NUM_SHARDS
                        number of shards for index [default=1]
  -num_replicas NUM_REPLICAS
                        number of replicas for index [default=0]
  -delimiter DELIMITER  the delimiter for the file [default=,]
  -update UPDATE        boolean indicating wheter or not you are updating an
                        existing index [default=False]
