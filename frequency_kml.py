import sys
from storage import unmarshal
from itertools import ifilter
from datetime import date, datetime, timedelta, time
from collections import defaultdict
import simplekml

def gen_interval_pair_stoppings(services, cur_date):
    zero_time = time(0, 0, 0)

    def instant(timedelta):
        return datetime.combine(cur_date, zero_time) + timedelta

    time_intervals = [(instant(timedelta(hours=8)),
                       instant(timedelta(hours=9)))]

    interval_pair_stoppings = defaultdict(lambda: defaultdict(lambda: []))

    print >> sys.stderr, "Producing pairs"
    for n, service in enumerate(services):
        if n%1000 == 0:
            print >> sys.stderr, n
        if not cur_date in service.valid_dates:
            continue
        stop_pairs = zip(service.stops, service.stops[1:])
        for _from, _to in stop_pairs:
            station_pair = (_from.station, _to.station)
            stop_time = instant(_from.time)
            for interval in time_intervals:
                if stop_time >= interval[0] and stop_time < interval[1]:
                    interval_pair_stoppings[interval][station_pair].append((service.line_id, stop_time))

    return interval_pair_stoppings

def kml_pairs(interval_pair_stoppings, fname):
    print >> sys.stderr, "Producing KML"
    kml = simplekml.Kml()
    for time_interval, pair_stoppings in interval_pair_stoppings.iteritems():
        for (frm, to), stoppings in pair_stoppings.iteritems():
            stoppings = sorted(stoppings)
            n = len(stoppings)
            descr = "\n".join([unicode(n)]+map(unicode, stoppings))
            kml.newlinestring(name=u"%s, %s" %(frm.name, to.name), description=descr, coords=[frm.location, to.location])
    kml.save(fname)

def main():
    services = unmarshal(sys.stdin)
    print len(services)
    ips = gen_interval_pair_stoppings(services, date(2012, 04, 10), )
    kml_pairs(ips, '2012-04-10.kml')

if __name__ == '__main__':

    main()
