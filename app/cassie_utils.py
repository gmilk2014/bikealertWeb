from operator import itemgetter
from collections import defaultdict
from cassandra.cluster import Cluster
from cassandra.query import *
from datetime import datetime, timedelta

class CassieUtilities(object):

    def __init__(self, ip_addr, keyspace):
        cluster = Cluster([ip_addr])
        self.session = cluster.connect()
        self.session.set_keyspace(keyspace)

    def fetch_rebalance_stream(self, id, date=None):
        """Fetches json records Cassandra table by date range
        Retrieves json records that within a specified date range in UTC time 
        zone. Dates must be specified in a specific format.
        Args:
            start_date: Date in string format (%Y-%m-%d %H:%M:%S) 
                e.g. 2015-05-05 20:43:25
            end_date: Date in string format (%Y-%m-%d %H:%M:%S) 
                e.g. 2015-05-05 20:43:25.
                If no end date is specified, the current date time is used.
            table: Cassandra table name in the keyspace specified when 
                initializing.
                Default to 'fashion' table under the execed keyspace
        Returns:
            A list of the records in the specified Cassandra table. This 
            includes the Primary Key for each record. The last field represents
            the actual json record.
        """
        table = 'rebalance_batch'
        if date is None:
            date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        print 'date is ' + str(date)
      
        record_lookup_stmt = "SELECT * FROM {} WHERE stationid=%s AND date_hour<%s".format(table)
        #self.session.row_factory = tuple_factory        
        record_list = []
        record_list += self.session.execute(record_lookup_stmt, [id, date])
        table = 'rebalance_stream'
        record_lookup_stmt = "SELECT * FROM {} WHERE stationid=%s AND date_hour<%s".format(table)
        record_list += self.session.execute(record_lookup_stmt, [id, date])
        return record_list

    def fetch_data(self, area):
        batch_table = 'bikecount_batch'
        stream_table = 'bikecount_stream'
        record_list = []
        batch_results = []
        stream_results = []
        record_lookup_stmt = 'SELECT * FROM {} WHERE area=%s'.format(batch_table)
        batch_results += self.session.execute(record_lookup_stmt, [area])

        record_lookup_stmt = 'SELECT * FROM {} WHERE area=%s'.format(stream_table)
        stream_results += self.session.execute(record_lookup_stmt, [area])
        for r1, r2 in zip(batch_results, stream_results):
            r = {'area':area, 'stationid':r1.stationid, 'count':int(r2.count) + int(r2.count)}
            record_list.append(r)
        record_list = sorted(record_list, key=itemgetter('count'))
        return record_list

    def fetch_location(self, area):
        table = 'location'
        results = []
        record_lookup_stmt = 'SELECT * FROM {} WHERE area=%s'.format(table)
        results += self.session.execute(record_lookup_stmt, [area])
        record_list = [{'area':area, 'id':r.id, 'lat':r.lat, 'lon':r.lon} for r in results]
        return record_list

    def fetch_bikecount(self, id):
        stationid = int(id)
        area = (stationid - 1) / 100 + 1
        batch_table = 'bikecount_batch'
        stream_table = 'bikecount_stream'
        record_list = []
        batch_results = []
        stream_results = []
        record_lookup_stmt = 'SELECT * FROM {} WHERE area=%s AND stationid=%s'.format(batch_table)
        batch_results += self.session.execute(record_lookup_stmt, [area, stationid])

        record_lookup_stmt = 'SELECT * FROM {} WHERE area=%s AND stationid=%s'.format(stream_table)
        stream_results += self.session.execute(record_lookup_stmt, [area, stationid])
        
        return int(batch_results[0].count) + int(stream_results[0].count)


