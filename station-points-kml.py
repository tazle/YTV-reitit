import sys
from storage import unmarshal
import simplekml

def gen_points(services):
    stations = set()
    for n, service in enumerate(services):
        if 'palvelu' in service.mode:
            continue
        if n%1000 == 0:
            print >> sys.stderr, n
        for stop in service.stops:
            stations.add(stop.station)
    return stations

def kml_points(stations):
    print >> sys.stderr, "Producing KML"
    kml = simplekml.Kml()
    for station in stations:
        descr = u"%s" %(station.uid)
        kml.newpoint(name=u"%s" %(station.name), description=descr, coords=[station.location])
    print >> sys.stderr, "Saving KML"
    return kml.kml(format=False)

def main():
    services = unmarshal(sys.stdin)
    print >> sys.stderr, len(services)
    stations = gen_points(services)
    kml = kml_points(stations)
    sys.stdout.write(kml)

if __name__ == '__main__':
    main()

