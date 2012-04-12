import xml.etree.cElementTree as ET
import sys
from model import Station, Stop, Service
from datetime import date, timedelta
import re

def station_key_from_elem(elem, groups):
    for group in groups:
        if elem.get('StationId') in group:
            return group[0]
    return elem.get('StationId')

def parse_services(kalkati_file, combination_groups=[]):
    """
    Parse kalkati file into a list of Services
    
    @param kalkati_file Kalkati XML file name or file object
    @param combination_file File that contains combining information for stations
    """
    
    stations_by_key = {}
    stations = {}
    modes = {}
    validity_sets = {}
    services = []
    
    count = 0
    for event, elem in ET.iterparse(kalkati_file):
        if event == 'end':
            if elem.tag == 'Service':
                services.append(parse_service(elem, modes, stations, validity_sets))
                elem.clear()
            elif elem.tag == 'Trnsmode':
                mode_id = elem.get('TrnsmodeId')
                mode_name = elem.get('Name')
                modes[mode_id] = mode_name
                elem.clear()
            elif elem.tag == 'Station':
                if elem.get('X'):
                    try:
                        station = parse_station(elem)
                        station_id = station.uid
                        station_key = station_key_from_elem(elem, combination_groups)
                        if station_key in stations_by_key:
                            station = stations_by_key[station_key]
                        else:
                            stations_by_key[station_key] = station
                        stations[station_id] = station
                    except Exception, e:
                        print >> sys.stderr, "Error parsing station", e, station_id
                elem.clear()
            elif elem.tag == 'Footnote':
                validity_set_id = elem.get('FootnoteId')
                first_date_ = elem.get('Firstdate')
                first_date = date(*map(int, first_date_.split('-')))
                dates = set()
                datebits = map(bool, map(int, elem.get('Vector')))
                for n, is_date_valid in enumerate(datebits):
                    if is_date_valid:
                        dates.add(first_date + timedelta(n))
                validity_sets[validity_set_id] = frozenset(dates)
    return services

def parse_station(station_elem):
    """
    Parse Kalkati Station element

    @param station_elem Station element as ETree Element
    """
    return Station(station_elem.get('StationId'),
                   station_elem.get('Name'),
                   (float(station_elem.get('X')),
                    float(station_elem.get('Y'))))

_timedeltas = {}
def _str2timedelta(s):
    if s in _timedeltas:
        return _timedeltas[s]
    else:
        td = timedelta(hours=int(s[:2]), minutes=int(s[2:]))
        _timedeltas[s] = td
        return td

def parse_service(service_elem, modes, stations, validity_sets):
    """
    Parse Kalkati Service element

    @param service_elem Service element as ETree Element
    @param modes Map from Kalkati TrnsmodeIds to transportation mode names
    @param stations Map from Kalkati StationIds to Station objects
    @param validity_sets Map from FootnoteIds to sets of date objects
    """
    service_id = intern(service_elem.get('ServiceId'))

    line_id = intern(service_elem.find('ServiceNbr').get('Variant'))
    line_mode_id = service_elem.find('ServiceTrnsmode').get('TrnsmodeId')
    line_mode = modes[line_mode_id]

    stops = []
    for stop_el in service_elem.iter('Stop'):
        station_id = intern(stop_el.get('StationId'))
        stop_station = stations[station_id]
        validity_set_id = service_elem.find('ServiceValidity').get('FootnoteId')
        validity_set = validity_sets.get(validity_set_id)
        departure = stop_el.get('Departure')
        arrival = stop_el.get('Arrival')

        if departure is None and arrival is None:
            print >> sys.stderr, "No departure or arrival time", service_id

        stop_time = departure if departure is not None else arrival
        stop_time = _str2timedelta(stop_time)

        stops.append(Stop(stop_station, stop_time))
        
        stop_type = stop_el.get('Type')
        if stop_type is not None:
            print >> sys.stderr, stop_type

    return Service(line_id, line_mode, stops, validity_set)

