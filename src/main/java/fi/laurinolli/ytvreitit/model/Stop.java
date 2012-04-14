package fi.laurinolli.ytvreitit.model;

import java.sql.Time;
import java.util.Date;

/**
 * Date: 2012-04-14 Time: 14:25
 *
 * @author Tuure Laurinolli, Portalify Ltd.
 */
public class Stop {
    private final Station station;
    private final Time time;

    public Stop(final Station station, final Time time) {
        this.station = station;
        this.time = time;
    }

    public Station getStation() {
        return station;
    }

    public Time getTime() {
        return time;
    }

    @Override
    public boolean equals(final Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }

        final Stop stop = (Stop) o;

        if (station != null ? !station.equals(stop.station) : stop.station != null) {
            return false;
        }
        if (time != null ? !time.equals(stop.time) : stop.time != null) {
            return false;
        }

        return true;
    }

    @Override
    public int hashCode() {
        int result = station != null ? station.hashCode() : 0;
        result = 31 * result + (time != null ? time.hashCode() : 0);
        return result;
    }

    @Override
    public String toString() {
        return "Stop{" +
                "station=" + station +
                ", time=" + time +
                '}';
    }
}
