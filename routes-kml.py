import sys
from storage import unmarshal
import simplekml

def gen_pairs(services):
    pairs = set()
    for n, service in enumerate(services):
        if 'palvelu' in service.mode:
            continue
        if n%1000 == 0:
            print >> sys.stderr, n
        stop_pairs = zip(service.stops, service.stops[1:])
        frm = None
        for to in service.stops:
            if frm is None:
                frm = to
                continue
            station_pair = (frm.station, to.station)
            pairs.add(station_pair)
            frm = to
    return pairs

def kml_pairs(pairs):
    print >> sys.stderr, "Producing KML"
    kml = simplekml.Kml()
    for (frm, to) in pairs:
        descr = u"%s %s" %(frm.uid, to.uid)
        kml.newlinestring(name=u"%s %s" %(frm.name, to.name), description=descr, coords=[frm.location, to.location])
    print >> sys.stderr, "Saving KML"
    return kml.kml(format=False)

def main():
    services = unmarshal(sys.stdin)
    print >> sys.stderr, len(services)
    pairs = gen_pairs(services)
    kml = kml_pairs(pairs)
    sys.stdout.write(kml)

if __name__ == '__main__':
    main()

