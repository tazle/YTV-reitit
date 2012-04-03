import sys
from kalkati import parse_services, parse_stations

#stations = parse_stations(sys.argv[1])
#print len(stations)
#print stations.values()[0]

services = parse_services(sys.stdin)
print len(services)
