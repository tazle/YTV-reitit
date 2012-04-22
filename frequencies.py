import datetime as dt
from collections import defaultdict

ZERO_TIME = dt.time(0, 0, 0)

def instant(cur_date, td):
    return dt.datetime.combine(cur_date, ZERO_TIME) + td

def stop_iter(services, cur_date):
    for service in services:
        if not cur_date in service.valid_dates:
            continue
        for stop in service.stops:
            yield stop

def hour_floor(td):
    return dt.timedelta(seconds=int(td.total_seconds())/3600*3600)

def hour_ceil(td):
    return dt.timedelta(seconds=int(td.total_seconds())/3600*3600 + 3600)

def gen_time_intervals(services, cur_date):
    min_stop_time = min(stop.time for stop in stop_iter(services, cur_date))
    max_stop_time = max(stop.time for stop in stop_iter(services, cur_date))

    def gen_intervals(min_time, max_time):
        interval_start = hour_floor(min_time)
        while interval_start < max_time:
            interval_end = interval_start + dt.timedelta(seconds=3600)
            yield (instant(cur_date, interval_start), instant(cur_date, interval_end))
            interval_start = interval_end

    return list(gen_intervals(min_stop_time, max_stop_time))

def single_time_interval(services, cur_date):
    min_stop_time = min(stop.time for stop in stop_iter(services, cur_date))
    max_stop_time = max(stop.time for stop in stop_iter(services, cur_date))

    interval_start = hour_floor(min_stop_time)
    interval_end = hour_ceil(max_stop_time)

    return [(instant(cur_date, interval_start), instant(cur_date, interval_end))]
    
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
