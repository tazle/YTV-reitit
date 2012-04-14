package fi.laurinolli.ytvreitit.model;

/**
 * Date: 2012-04-14 Time: 14:27
 *
 * @author Tuure Laurinolli, Portalify Ltd.
 */
public class Coord {
    private final double longitude, latitude;

    public Coord(final double longitude, final double latitude) {
        this.longitude = longitude;
        this.latitude = latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public double getLatitude() {
        return latitude;
    }

    @Override
    public String toString() {
        return "Coord{" +
                "longitude=" + longitude +
                ", latitude=" + latitude +
                '}';
    }
}
