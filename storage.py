from model import Station, Stop, Service
import struct
import datetime as dt

UINT_FORMAT = "!L"
USHORT_FORMAT = "!H"
DOUBLE_FORMAT = "!d"

def makerevmap(a_set):
    """
    Make a map of object -> id from a set of objects.

    @param a_set Set of objects to map into a dense set of integers
    @return (l, m) where l is list of objects and m is a map of objects to their indices in the list.
    """
    l = list(a_set)
    l.sort()

    m = {}
    for i, el in enumerate(l):
        m[el] = i
    return l, m

def marshal(outfile, services):
    """
    Marshal a list of services into a file.
    
    @param outfile File object to write to
    @param services List of Service objects
    """

    stations = set()
    times = set()

    validity_periods = set()
    strings = set()

    for service in services:
        strings.add(service.line_id)
        strings.add(service.mode)
        validity_periods.add(service.valid_dates)
        for stop in service.stops:
            station = stop.station
            strings.add(station.uid)
            strings.add(station.name)
            stations.add(stop.station)
            times.add(stop.time)

    stations_l, stations_r = makerevmap(stations)
    times_l, times_r = makerevmap(times)

    validity_periods_l, validity_periods_r = makerevmap(validity_periods)
    strings_l, strings_r = makerevmap(strings)

    outfile.write('YTVF')

    encode_strings(outfile, strings_l)
    encode_validity_periods(outfile, validity_periods_l)
    encode_stations(outfile, stations_l, strings_r)
    encode_services(outfile, services, strings_r, validity_periods_r, stations_r)
    
def encode_uint(out, i):
    out.write(struct.pack(UINT_FORMAT, i))

def encode_ushort(out, i):
    out.write(struct.pack(USHORT_FORMAT, i))

def encode_double(out, d):
    out.write(struct.pack(DOUBLE_FORMAT, d))

def encode_string(out, string):
    encoded = string.encode('utf-8')
    encode_ushort(out, len(encoded))
    out.write(encoded)

def encode_strings(out, strings_l):
    encode_uint(out, len(strings_l))
    for i, string in enumerate(strings_l):
        encode_string(out, string)

def encode_validity_periods(out, validity_periods_l):
    encode_uint(out, len(validity_periods_l))
    for validity_period in validity_periods_l:
        encode_uint(out, len(validity_period))
        for date_el in validity_period:
            encode_uint(out, date_el.toordinal())

def encode_stations(out, stations_l, strings_r):
    encode_uint(out, len(stations_l))
    for station in stations_l:
        encode_uint(out, strings_r[station.uid])
        encode_uint(out, strings_r[station.name])
        encode_double(out, station.location[0])
        encode_double(out, station.location[1])

def encode_services(out, services, strings_r, validity_periods_r, stations_r):
    encode_uint(out, len(services))
    for service in services:
        encode_ushort(out, strings_r[service.line_id])
        encode_ushort(out, strings_r[service.mode])
        encode_ushort(out, validity_periods_r[service.valid_dates])
        encode_ushort(out, len(service.stops))
        for stop in service.stops:
            encode_ushort(out, stations_r[stop.station])
            encode_ushort(out, int(stop.time.total_seconds())/60)

def unmarshal(infile):
    """
    Unmarshal a list of services from a file.
    
    @param infile File object to read from
    @return List of services parsed
    """

    header = infile.read(4)
    if header != 'YTVF':
        raise Exception("Invalid input file header: {}".format(header))

    strings_l = decode_strings(infile)
    validity_periods_l = decode_validity_periods(infile)
    stations_l = decode_stations(infile, strings_l)
    return decode_services(infile, strings_l, validity_periods_l, stations_l)

def decode_uint(fin):
    return struct.unpack(UINT_FORMAT, fin.read(4))[0]

def decode_ushort(fin):
    return struct.unpack(USHORT_FORMAT, fin.read(2))[0]

def decode_double(fin):
    return struct.unpack(DOUBLE_FORMAT, fin.read(8))[0]

def decode_string(fin):
    length = decode_ushort(fin)
    return fin.read(length).decode('utf-8')

def decode_strings(fin):
    count = decode_uint(fin)
    strings_l = []
    for i in xrange(count):
        strings_l.append(decode_string(fin))
    return strings_l

def decode_validity_periods(fin):
    validity_periods_l = []
    count = decode_uint(fin)
    for _ in xrange(count):
        n_dates = decode_uint(fin)
        dates = set()
        for _ in xrange(n_dates):
            ordinal = decode_uint(fin)
            dates.add(dt.date.fromordinal(ordinal))
        validity_periods_l.append(dates)
    return validity_periods_l

def decode_stations(fin, strings_l):
    count = decode_uint(fin)
    stations_l = []
    for _ in xrange(count):
        uid = strings_l[decode_uint(fin)]
        name = strings_l[decode_uint(fin)]
        lon = decode_double(fin)
        lat = decode_double(fin)
        stations_l.append(Station(uid, name, (lon, lat)))
    return stations_l
        
def decode_services(fin, strings_l, validity_periods_l, stations_l):
    import sys
    print >> sys.stderr, "Decoding services"
    count = decode_uint(fin)
    services = []
    for i in xrange(count):
        if i%1000 == 0:
            print >> sys.stderr, i
        line_id = strings_l[decode_ushort(fin)]
        mode = strings_l[decode_ushort(fin)]
        validity_periods = validity_periods_l[decode_ushort(fin)]
        stop_count = decode_ushort(fin)
        stops = []
        for _ in xrange(stop_count):
            station = stations_l[decode_ushort(fin)]
            time_mins = decode_ushort(fin)
            time = dt.timedelta(hours=time_mins/60, minutes=time_mins%60)
            stops.append(Stop(station, time))
        services.append(Service(line_id, mode, stops, validity_periods))
    print >> sys.stderr, "Finished decoding"
    return services
