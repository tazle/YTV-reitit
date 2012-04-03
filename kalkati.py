import xml.etree.cElementTree as ET
import sys
from model import Station, Stop, Service

def parse_services(kalkati_file):
    """
    Parse kalkati file into a list of Services
    
    @param kalkati_tree Kalkati XML file name or file object
    """
    
    stations = {}
    modes = {}
    services = []
    
    count = 0
    for event, elem in ET.iterparse(kalkati_file):
        if event == 'end':
            if elem.tag == 'Station':
                station_id = elem.get('StationId')
                try:
                    stations[station_id] = parse_station(elem)
                except Exception, e:
                    print >> sys.stderr, "Error parsing station", station_id
                elem.clear()
            if elem.tag == 'Trnsmode':
                mode_id = elem.get('TrnsmodeId')
                mode_name = elem.get('Name')
                modes[mode_id] = mode_name
            elif elem.tag == 'Service':
                services.append(parse_service(elem, modes, stations))
                elem.clear()
    return services

def parse_stations(kalkati_file):
    """
    Parse kalkati file into a dict that maps StationIds to
    Stations. Meant for testing.
    
    @param kalkati_tree Kalkati XML file name or file object
    """
    
    stations = {}
    services = []
    
    late_tags = ('Trnsattr', 'Trnsmode', 'Synonym', 'Footnote', 'Change', 'Thrusrvc', 'Timetbls')

    level = 0
    count = 0
    for event, elem in ET.iterparse(kalkati_file, events=('start', 'end')):
        if event == 'end':
            level -= 1
            if elem.tag == 'Station':
                count += 1
                station_id = elem.get('StationId')
                try:
                    stations[station_id] = parse_station(elem)
                except Exception, e:
                    print >> sys.stderr, "Error parsing station", station_id
                elem.clear()
                if count % 1000 == 0:
                    print count
        if event == 'start':
            level += 1
            if elem.tag in late_tags:
                return stations
    return stations

def parse_station(station_elem):
    """
    Parse Kalkati Station element

    @param station_elem Station element as ETree Element
    """
    return Station(station_elem.get('Name'),
                   (float(station_elem.get('X')),
                    float(station_elem.get('Y'))))



def parse_service(service_elem, modes, stations):
    """
    Parse Kalkati Service element

    @param service_elem Service element as ETree Element
    @param modes Map from Kalkati TrnsmodeIds to transportation mode names
    @param stations Map from Kalkati StationIds to Station objects
    """
    service_id = service_elem.get('ServiceId')

    line_id = service_elem.find('ServiceNbr').get('Variant')
    line_mode_id = service_elem.find('ServiceTrnsmode').get('TrnsmodeId')
    line_mode = modes[line_mode_id]

    stops = []
    for stop_el in service_elem.find('Stop'):
        station_id = stop_el.get('StationId')
        stop_station = stations[station_id]
        stop_time = stop_el.get('Departure')
        if stop_time is None:
            print >> sys.stderr, "No Departure time", service_id

        if stop_el.get('Arrival') is not None:
            print >> sys.stderr, "Has Arrival", service_id

        stops.append(Stop(stop_station, stop_time))
    return Service(line_id, line_mode, stops)

