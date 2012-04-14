import sys
from storage import unmarshal
from itertools import ifilter
import datetime as dt
from collections import defaultdict
import simplekml
import time

ZERO_TIME = dt.time(0, 0, 0)

def instant(cur_date, td):
    return dt.datetime.combine(cur_date, ZERO_TIME) + td

def gen_interval_pair_stoppings(services, cur_date, time_intervals):
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
            stop_time = instant(cur_date, _from.time)
            for interval in time_intervals:
                if stop_time >= interval[0] and stop_time < interval[1]:
                    interval_pair_stoppings[interval][station_pair].append((service.line_id, stop_time))

    return interval_pair_stoppings

def calculate_max_interval(times):
    max_interval = dt.timedelta(0)
    prev_td = None
    for stop_td in times:
        if prev_td is None:
            prev_td = stop_td
            continue
        diff = stop_td - prev_td
        if diff > max_interval:
            max_interval = diff
        prev_td = stop_td
    return max_interval

styles = [(dt.timedelta(minutes=7, seconds=30), simplekml.Style(linestyle=simplekml.LineStyle(color="ff14ff14", width=2)), 4),
          (dt.timedelta(minutes=15), simplekml.Style(linestyle=simplekml.LineStyle(color="ff14ffff", width=2)), 3),
          (dt.timedelta(minutes=30), simplekml.Style(linestyle=simplekml.LineStyle(color="ff1414ff", width=2)), 2),
          (None, simplekml.Style(simplekml.LineStyle(color="ffcccccc", width=2)), 1)]

def get_style(interval):
    for td, style, alt in styles:
        if td is None:
            return style
        elif interval <= td:
            return style

def kml_pairs(interval_pair_stoppings, stream):
    print >> sys.stderr, "Producing KML"
    kml = simplekml.Kml()
    layers = {}
    alts = {}
    for td, layer_style, alt in reversed(styles):
        layer = kml.newfolder(name="%s" %td)
        layer.liststyle.listitemtype = "checkHideChildren"
        layers[layer_style] = layer
        alts[layer_style] = alt
        
    print >> sys.stderr, len(interval_pair_stoppings)
    for time_interval, pair_stoppings in sorted(interval_pair_stoppings.iteritems()):
        start_time = time.time()
        stoppings_count = 0
        ls_count = 0

        ts_start = time_interval[0].isoformat()
        ts_end = time_interval[1].isoformat()
        ts = simplekml.TimeSpan(ts_start+"+03:00", ts_end+"+03:00") # timezone hack

        for (frm, to), stoppings in pair_stoppings.iteritems():
            stoppings = sorted(stoppings, key=lambda x: x[1])
            times = [time_interval[0]] + list(sorted([s[1] for s in stoppings])) + [time_interval[1]]

            max_interval = calculate_max_interval(times)

            style = get_style(max_interval)
            layer = layers[style]
            alt = alts[style]

            n = len(stoppings)
            stoppings_count += n
            ls_count += 1

            descr = "\n".join([unicode(n)]+[u"%s %s" %s for s in stoppings])
            ls = layer.newlinestring(name=u"%s, %s" %(frm.name, to.name), description=descr, coords=[frm.location + (alt,), to.location + (alt,)], timespan=ts, altitudemode="ClampToGround")
            #ls.linestyle = style
            ls.style = style
        end_time = time.time()
        time_el = (end_time-start_time)
        print >> sys.stderr, time_interval, stoppings_count, ls_count, time_el
        print >> sys.stderr, time_interval, stoppings_count/time_el, ls_count/time_el

    print >> sys.stderr, "Saving KML"
    kml.stream(stream)

def gen_time_intervals(services, cur_date):
    def stop_iter(services):
        for service in services:
            if not cur_date in service.valid_dates:
                continue
            for stop in service.stops:
                yield stop

    min_stop_time = min(stop.time for stop in stop_iter(services))
    max_stop_time = max(stop.time for stop in stop_iter(services))

    def hour_floor(td):
        return dt.timedelta(seconds=int(td.total_seconds())/3600*3600)

    def gen_intervals(min_time, max_time):
        interval_start = hour_floor(min_time)
        while interval_start < max_time:
            interval_end = interval_start + dt.timedelta(seconds=3600)
            yield (instant(cur_date, interval_start), instant(cur_date, interval_end))
            interval_start = interval_end

    return list(gen_intervals(min_stop_time, max_stop_time))

def main():
    services = unmarshal(sys.stdin)
    print >> sys.stderr, len(services)
    sel_date = dt.date(2012, 04, 10)
    time_intervals = gen_time_intervals(services, sel_date)
    #time_intervals = [(instant(sel_date, dt.timedelta(hours=8)), instant(sel_date, dt.timedelta(hours=9)))]
    ips = gen_interval_pair_stoppings(services, sel_date, time_intervals)
    kml_pairs(ips, sys.stdout)

if __name__ == '__main__':

    main()
