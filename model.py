class Station(object):
    def __init__(self, name, location):
        """
        @param name Station name
        @param location WGS84 coordinates or station as (lon, lat) tuple
        """
        self.name = name
        self.location = location

    def __repr__(self):
        return u"Station({}, {})".format(self.name, self.location)

    def __str__(self):
        return repr(self)


class Stop(object):
    def __init__(self, station, time):
        """
        @param station Station where this stop happens
        @param time Time when this stop happens
        """
        self.station = station
        self.time = time

class Service(object):
    def __init__(self, line_id, mode, stops):
        """
        @param line_id Human-readable identifier of the service
        @param mode Mode of service - bus, tram, metro
        @param stops List of stop objects describing stops of this service
        """
        self.line_id = line_id
        self.mode = mode
        self.stops = stops
