import sys
from storage import unmarshal
import datetime as dt
import simplekml
import time
import json
import calendar
from collections import defaultdict

def gen_interval_pair_stoppings(services, cur_date, time_intervals):
    interval_pair_stoppings = defaultdict(lambda: defaultdict(lambda: []))

    for n, service in enumerate(services):
        if not cur_date in service.valid_dates:
            continue
        stop_pairs = zip(service.stops, service.stops[1:])
        for _from, _to in stop_pairs:
            station_pair = (_from.station, _to.station)
            stop_time = instant(cur_date, _from.time)
            for interval in time_intervals:
                if stop_time >= interval[0] and stop_time < interval[1]:
                    interval_pair_stoppings[interval][station_pair].append((service.line_id, stop_time))

    return interval_pair_stoppings

def json_stoppings(services, stream, cur_date):
    stoppings = defaultdict(lambda : [])
    service_id_counter = 0
    for n, service in enumerate(services):
        if n%1000 == 0:
            print >> sys.stderr, n
        if not cur_date in service.valid_dates:
            continue

        stop_pairs = zip(service.stops, service.stops[1:])
        for _from, _to in stop_pairs:
            station_pair = ((_from.station.name, _from.station.location), (_to.station.name, _to.station.location))
            hours = int(_from.time.total_seconds()/60)
            stoppings[station_pair].append(hours)

    out = []
    for (frm, to), stops in stoppings.iteritems():
        stops.sort()
        out.append([frm, to, stops])

    json.dump(out, stream)

def main():
    services = unmarshal(sys.stdin)
    print >> sys.stderr, len(services)
    sel_date = dt.date(2012, 04, 10)
    print >> sys.stderr, "Generating JSON"
    json_stoppings(services, sys.stdout, sel_date)

if __name__ == '__main__':
    main()
