class Station(object):

    def __init__(self, name, location):
        """
        @param name Station name
        @param location WGS84 coordinates or station as (lon, lat) tuple
        """
        self.name = name
        self.location = location

    def __unicode__(self):
        return u"Station(%s, %s)" % (self.name, self.location)


class Stop(object):

    __slots__ = ['station', 'time']

    def __init__(self, station, time):
        """
        @param station Station where this stop happens
        @param time Time when this stop happens
        """
        self.station = station
        self.time = time

    def __unicode__(self):
        return u'Stop(%s, %s)'% (unicode(self.station), self.time)

    def __getstate__(self):
        return (self.station, self.time)

    def __setstate__(self, pickled):
        self.station = pickled[0]
        self.time = pickled[1]

class Service(object):

    __slots__ = ['line_id', 'mode', 'stops', 'valid_dates']

    def __init__(self, line_id, mode, stops, valid_dates):
        """
        @param line_id Human-readable identifier of the service
        @param mode Mode of service - bus, tram, metro
        @param stops List of stop objects describing stops of this service
        """
        self.line_id = line_id
        self.mode = mode
        self.stops = stops
        self.valid_dates = valid_dates

    def __unicode__(self):
        return u'Service(%s, %s, [%s], [%s])' % (
            self.line_id,
            self.mode,
            ", ".join(unicode(stop) for stop in self.stops),
            ", ".join(unicode(date) for date in self.valid_dates))

    def __getstate__(self):
        return (self.line_id, self.mode, self.stops, self.valid_dates)

    def __setstate__(self, pickled):
        self.line_id = pickled[0]
        self.mode = pickled[1]
        self.stops = pickled[2]
        self.valid_dates = pickled[3]

