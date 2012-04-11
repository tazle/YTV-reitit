class Station(object):

    def __init__(self, uid, name, location):
        """
        @param uid Unique identifier
        @param name Station name
        @param location WGS84 coordinates or station as (lon, lat) tuple
        """
        self.uid = uid
        self.name = name
        self.location = location

    def __unicode__(self):
        return u"Station(%s, %s)" % (self.name, self.location)

    def __eq__(self, other):
        return self.uid == other.uid and self.name == other.name and self.location == other.location

    def __hash__(self):
        return hash((self.uid, self.name, self.location))

class Stop(object):

    __slots__ = ['station', 'time']

    def __init__(self, station, time):
        """
        @param station Station where this stop happens

        @param time Time when this stop happens, as timedelta from
        previous day change (36-hour clock is used, so late night
        lines have times like 26:35 meaning 02:35 on the next day)
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

    def __eq__(self, other):
        return self.station == other.station and self.time == other.time

    def __hash__(self):
        return hash((self.station, self.time))

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

    def __eq__(self, other):
        return self.line_id == other.line_id and self.mode == other.mode and self.stops == other.stops and self.valid_dates == other.valid_dates

    def __hash__(self):
        return hash((self.line_id, self.mode, self.stops, self.valid_dates))
