## Copyright 2017 Aaron Chazhoor
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
## http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

import csv
import sys
import argparse

from elasticsearch import Elasticsearch

# create_index creates an elasticsearch index from a csv file
#
# @param (string) file_path: the path to the file
# @param (dict) es_host: dictionary containing the host and port of the machine running elasticsearch
# @param (string) index_name: name of index to be created 
# @param (string) type_name: name of type
# @param (int) num_shard: number of shards for index
# @param (int) num_replicas: number of replicas for index
# @param (string) seperator: the delimiter for the file
# @param (boolean) update: boolean indicating wheter or not you are updating an existing index
#
def create_index(file_path, es_host, index_name, type_name, num_shards, num_replicas, seperator, update):
    # open file
    with open(file_path) as f:
        # create csv reader and parse headers
        csv_file = csv.reader(f, delimiter=seperator)
        header = next(csv_file)
        header = [item.lower() for item in header]

        # create bulk data
        bulk_data = [] 
        for row in csv_file:
            data_dict = {}
            for i in range(len(row)):
                data_dict[header[i]] = row[i]
            op_dict = {
                "index": {
                    "_index": index_name, 
                    "_type": type_name
                }
            }
            bulk_data.append(op_dict)
            bulk_data.append(data_dict)

        # create ES client and create index
        es = Elasticsearch(hosts = [es_host])

        # if index already exists and update flag is true, delete the existing index, else exit the program
        if es.indices.exists(index_name):
            if update:  
                print("deleting existing index")
                res = es.indices.delete(index = index_name)
            else:
                print("index already exists")
                sys.exit()

        # create the index
        print("creating index " + index_name)
        request_body = {
            "settings" : {
                "number_of_shards": num_shards,
                "number_of_replicas": num_replicas
            }               
        }
        res = es.indices.create(index = index_name, body = request_body)

        # bulk index the data
        res = es.bulk(index = index_name, body = bulk_data, refresh = True)

def main():
    # create command line argument parser
    parser = argparse.ArgumentParser(description="Python script to load a csv file into an index in elasticsearch")
    parser.add_argument("file_path", help='path to the file', type=str)
    parser.add_argument("index_name", help='name of index to be created', type=str)
    parser.add_argument("type_name", help='name of type', type=str)
    parser.add_argument("-host", help='host name of machine running Elasticsearch [default=localhost]', type=str)
    parser.add_argument("-port", help='port of machine running Elasticsearch [default=9200]', type=int)
    parser.add_argument("-num_shards", help='number of shards for index [default=1]', type=int)
    parser.add_argument("-num_replicas", help='number of replicas for index [default=0]', type=int)
    parser.add_argument("-delimiter", help='the delimiter for the file [default=,]', type=str)
    parser.add_argument("-update", help='boolean indicating wheter or not you are updating an existing index [default=False]', type=bool)
    args = parser.parse_args()

    # set default variables for optional parameters
    host = "localhost"
    port = 9200
    num_shards = 1
    num_replicas = 0
    seperator = ','
    update = False

    # set optional parametes is they are defined
    if args.host is not None:
        host = args.host
    if args.port is not None:
        port = args.port
    if args.num_shards is not None:
        num_shards = args.num_shards
    if args.num_replicas is not None:
        num_replicas = args.num_replicas
    if args.delimiter is not None:
        seperator = args.delimiter
    if args.update is not None:
        update = args.update
    es_host = {"host" : host, "port" : port}

    # create the index
    create_index(args.file_path, es_host, args.index_name, args.type_name, num_shards, num_replicas, seperator, update)

if __name__ == "__main__":
    main()

