package fi.laurinolli.ytvreitit.model;

/**
 * Date: 2012-04-14 Time: 14:25
 *
 * @author Tuure Laurinolli, Portalify Ltd.
 */
public class Station {
    private final String uid;
    private final String name;
    private final Coord location;

    public Station(final String uid, final String name, final Coord location) {
        this.uid = uid;
        this.name = name;
        this.location = location;
    }

    public String getUid() {
        return uid;
    }

    public String getName() {
        return name;
    }

    public Coord getLocation() {
        return location;
    }

    @Override
    public boolean equals(final Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }

        final Station station = (Station) o;

        if (location != null ? !location.equals(station.location) : station.location != null) {
            return false;
        }
        if (name != null ? !name.equals(station.name) : station.name != null) {
            return false;
        }
        if (uid != null ? !uid.equals(station.uid) : station.uid != null) {
            return false;
        }

        return true;
    }

    @Override
    public int hashCode() {
        int result = uid != null ? uid.hashCode() : 0;
        result = 31 * result + (name != null ? name.hashCode() : 0);
        result = 31 * result + (location != null ? location.hashCode() : 0);
        return result;
    }

    @Override
    public String toString() {
        return "Station{" +
                "uid='" + uid + '\'' +
                ", name='" + name + '\'' +
                ", location=" + location +
                '}';
    }
}
