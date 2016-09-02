#!/usr/bin/env python
'''
:mod:`csv2redis.csv2redis` is a module containing classes for importing CSV files to Redis.
'''

import csv
from optparse import OptionParser
import redis
import sys

def import_csv(csv_file, key_col, redis_host='localhost', redis_port=6379):
    pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=0)
    r = redis.Redis(connection_pool=pool)
    pipe = r.pipeline()
    with open(csv_file, 'rb') as cf:
        cfreader = csv.reader(cf)
        headers = cfreader.next()
        for row in cfreader:
            record = {}
            for h, v in zip(headers, row):
                record[h] = v
            pipe.hmset(row[key_col], record)
    pipe.execute()

if __name__ == "__main__":
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file", dest="csvfile", help="CSV file to import", metavar="FILE")
    parser.add_option("-n", "--name-column", dest="namecolumn", help="Column number to use as name")
    parser.add_option("-r", "--redis-host", dest="redishost", help="Redis host name", default="localhost")
    parser.add_option("-p", "--redis-port", dest="redisport", help="Redis port", default=6379)

    (options, args) = parser.parse_args()

    if options.csvfile is None:
        parser.error("Missing reqiured option csv file")

    if options.namecolumn is None:
        parser.error("Missing required option name column")

    import_csv(options.csvfile, int(options.namecolumn), options.redishost, options.redisport)

