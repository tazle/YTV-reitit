package fi.laurinolli.ytvreitit.model;

import org.omg.CORBA.PRIVATE_MEMBER;

import java.util.Date;
import java.util.List;
import java.util.Set;

/**
 * Date: 2012-04-14 Time: 14:25
 *
 * @author Tuure Laurinolli, Portalify Ltd.
 */
public class Service {
    private final String lineId;
    private final String mode;
    private final List<Stop> stops;
    private final Set<Date> validDates;

    public Service(final String lineId, final String mode, final List<Stop> stops, final Set<Date> validDates) {
        this.lineId = lineId;
        this.mode = mode;
        this.stops = stops;
        this.validDates = validDates;
    }

    public String getLineId() {
        return lineId;
    }

    public String getMode() {
        return mode;
    }

    public List<Stop> getStops() {
        return stops;
    }

    public Set<Date> getValidDates() {
        return validDates;
    }

    @Override
    public boolean equals(final Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }

        final Service service = (Service) o;

        if (lineId != null ? !lineId.equals(service.lineId) : service.lineId != null) {
            return false;
        }
        if (mode != null ? !mode.equals(service.mode) : service.mode != null) {
            return false;
        }
        if (stops != null ? !stops.equals(service.stops) : service.stops != null) {
            return false;
        }
        if (validDates != null ? !validDates.equals(service.validDates) : service.validDates != null) {
            return false;
        }

        return true;
    }

    @Override
    public int hashCode() {
        int result = lineId != null ? lineId.hashCode() : 0;
        result = 31 * result + (mode != null ? mode.hashCode() : 0);
        result = 31 * result + (stops != null ? stops.hashCode() : 0);
        result = 31 * result + (validDates != null ? validDates.hashCode() : 0);
        return result;
    }

    @Override
    public String toString() {
        return "Service{" +
                "lineId='" + lineId + '\'' +
                ", mode='" + mode + '\'' +
                ", stops=" + stops +
                ", validDates=" + validDates +
                '}';
    }
}
