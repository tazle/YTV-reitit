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
            if elem.tag == 'Service':
                services.append(parse_service(elem, modes, stations))
                elem.clear()
            elif elem.tag == 'Trnsmode':
                mode_id = elem.get('TrnsmodeId')
                mode_name = elem.get('Name')
                modes[mode_id] = mode_name
                elem.clear()
            elif elem.tag == 'Station':
                station_id = elem.get('StationId')
                if elem.get('X'):
                    try:
                        stations[station_id] = parse_station(elem)
                    except Exception, e:
                        print >> sys.stderr, "Error parsing station", e, station_id
                elem.clear()
    return services


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
    service_id = intern(service_elem.get('ServiceId'))

    line_id = intern(service_elem.find('ServiceNbr').get('Variant'))
    line_mode_id = service_elem.find('ServiceTrnsmode').get('TrnsmodeId')
    line_mode = modes[line_mode_id]

    stops = []
    for stop_el in service_elem.iter('Stop'):
        station_id = intern(stop_el.get('StationId'))
        stop_station = stations[station_id]
        departure = stop_el.get('Departure')
        arrival = stop_el.get('Arrival')

        if departure is None and arrival is None:
            print >> sys.stderr, "No departure or arrival time", service_id

        stop_time = departure if departure is not None else arrival
        stop_time = intern(stop_time)

        stops.append(Stop(stop_station, stop_time))
        
        stop_type = stop_el.get('Type')
        if stop_type is not None:
            print stop_type

    return Service(line_id, line_mode, stops)

