package fi.laurinolli.ytvreitit;

import fi.laurinolli.ytvreitit.model.Coord;
import fi.laurinolli.ytvreitit.model.Service;
import fi.laurinolli.ytvreitit.model.Station;
import fi.laurinolli.ytvreitit.model.Stop;

import java.io.DataInput;
import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.Charset;
import java.sql.Time;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

public class Codec {
    private static final Charset UTF_8 = Charset.forName("UTF-8");

    private static final int DI4Y = 1461;    /* days_before_year(5); days in 4 years */
    private static final int DI100Y = 36524;   /* days_before_year(101); days in 100 years */
    private static final int DI400Y = 146097;  /* days_before_year(401); days in 400 years  */

    private static int _days_in_month[] = {
            0, /* unused; this vector uses 1-based indexing */
            31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
    };

    static int _days_before_month[] = {
            0, /* unused; this vector uses 1-based indexing */
            0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334
    };

    public List<Service> unmarshal(final InputStream in) throws IOException {
        final DataInput dataInput = new DataInputStream(in);

        final byte[] read = new byte[4];
        final byte[] expected = new byte[] {(byte)'Y', (byte)'T', (byte)'V', (byte)'F'};

        dataInput.readFully(read);
        if (!Arrays.equals(read, expected)) {
            throw new IllegalArgumentException("Invalid input data");
        }

        final List<String> strings = decodeStrings(dataInput);
        final List<Set<Date>> validityPeriods = decodeValidityPeriods(dataInput);
        final List<Station> stations = decodeStations(dataInput, strings);
        return decodeServices(dataInput, strings, stations, validityPeriods);
    }

    private List<Service> decodeServices(final DataInput dataInput, final List<String> strings, final List<Station> stations, final List<Set<Date>> validityPeriods) throws IOException {
        final int count = dataInput.readInt();
        final List<Service> services = new ArrayList<Service>(count);
        for (int i = 0; i < count; i++) {
            final String lineId = strings.get(dataInput.readUnsignedShort());
            final String mode = strings.get(dataInput.readUnsignedShort());
            final Set<Date> validityPeriod = validityPeriods.get(dataInput.readUnsignedShort());
            final int nStops = dataInput.readUnsignedShort();
            final List<Stop> stops = new ArrayList<Stop>(nStops);
            for (int j = 0; j < nStops; j++) {
                final Station station = stations.get(dataInput.readUnsignedShort());
                final int _time = dataInput.readUnsignedShort();
                final Time time = new Time(_time/60, _time%60, 0);
                stops.add(new Stop(station, time));
            }
            services.add(new Service(lineId, mode, stops, validityPeriod));
        }
        return services;
    }

    private List<Station> decodeStations(final DataInput dataInput, final List<String> strings) throws IOException {
        final int count = dataInput.readInt();
        final List<Station> stations = new ArrayList<Station>(count);
        for (int i = 0; i < count; i++) {
            final String uid = strings.get(dataInput.readInt());
            final String name = strings.get(dataInput.readInt());
            final double lon = dataInput.readDouble();
            final double lat = dataInput.readDouble();
            stations.add(new Station(uid, name, new Coord(lon, lat)));
        }
        return stations;
    }

    private List<Set<Date>> decodeValidityPeriods(final DataInput dataInput) throws IOException {
        final int count = dataInput.readInt();
        final List<Set<Date>> validityPeriods = new ArrayList<Set<Date>>(count);
        for (int i = 0; i < count; i++) {
            final int dateCount = dataInput.readInt();
            final Set<Date> dates = new TreeSet<Date>();
            for (int j = 0; j < dateCount; j++) {
                final int ordinal = dataInput.readInt();
                final Date date = ord2Date(ordinal);
                dates.add(date);
            }
            validityPeriods.add(dates);
        }
        return validityPeriods;
    }

    private List<String> decodeStrings(final DataInput dataInput) throws IOException {
        final int count = dataInput.readInt();
        final List<String> strings = new ArrayList<String>(count);
        for (int i = 0; i < count; i++) {
            strings.add(decodeString(dataInput));
        }
        return strings;
    }

    private final String decodeString(final DataInput in) throws IOException {
        final int length = in.readUnsignedShort();
        final byte[] bytes = new byte[length];
        in.readFully(bytes);
        return new String(bytes, UTF_8);
    }

    private final Date ord2Date(int ordinal) {
        // Copied from Python. PSF license.

        int n, n1, n4, n100, n400, preceding;
        int year, month, day;

        /* ordinal is a 1-based index, starting at 1-Jan-1.  The pattern of
        * leap years repeats exactly every 400 years.  The basic strategy is
        * to find the closest 400-year boundary at or before ordinal, then
        * work with the offset from that boundary to ordinal.  Life is much
        * clearer if we subtract 1 from ordinal first -- then the values
        * of ordinal at 400-year boundaries are exactly those divisible
        * by DI400Y:
        *
        *    D  M   Y            n              n-1
        *    -- --- ----        ----------     ----------------
        *    31 Dec -400        -DI400Y       -DI400Y -1
        *     1 Jan -399         -DI400Y +1   -DI400Y      400-year boundary
        *    ...
        *    30 Dec  000        -1             -2
        *    31 Dec  000         0             -1
        *     1 Jan  001         1              0          400-year boundary
        *     2 Jan  001         2              1
        *     3 Jan  001         3              2
        *    ...
        *    31 Dec  400         DI400Y        DI400Y -1
        *     1 Jan  401         DI400Y +1     DI400Y      400-year boundary
        */
        --ordinal;
        n400 = ordinal / DI400Y;
        n = ordinal % DI400Y;
        year = n400 * 400 + 1;

        /* Now n is the (non-negative) offset, in days, from January 1 of
        * year, to the desired date.  Now compute how many 100-year cycles
        * precede n.
        * Note that it's possible for n100 to equal 4!  In that case 4 full
        * 100-year cycles precede the desired day, which implies the
        * desired day is December 31 at the end of a 400-year cycle.
        */
        n100 = n / DI100Y;
        n = n % DI100Y;

        /* Now compute how many 4-year cycles precede it. */
        n4 = n / DI4Y;
        n = n % DI4Y;

        /* And now how many single years.  Again n1 can be 4, and again
        * meaning that the desired day is December 31 at the end of the
        * 4-year cycle.
        */
        n1 = n / 365;
        n = n % 365;

        year += n100 * 100 + n4 * 4 + n1;
        if (n1 == 4 || n100 == 4) {
            year -= 1;
            month = 12;
            day = 31;
            return new Date(year, month, day);
        }

        /* Now the year is correct, and n is the offset from January 1.  We
        * find the month via an estimate that's either exact or one too
        * large.
        */
        final boolean leapyear = (n1 == 3) && (n4 != 24 || n100 == 3);

        month = (n + 50) >> 5;
        preceding = (_days_before_month[month] + ((month > 2 && leapyear) ? 1 : 0));
        if (preceding > n) {
            /* estimate is too large */
            month -= 1;
            preceding -= days_in_month(year, month);
        }
        n -= preceding;

        day = n + 1;
        return new Date(year, month, day);
    }

    private static int days_in_month(int year, int month) {
        if (month == 2 && is_leap(year)) {
            return 29;
        } else {
            return _days_in_month[month];
        }
    }

    private static boolean is_leap(final int year) {
        /* Cast year to unsigned.  The result is the same either way, but
        * C can generate faster code for unsigned mod than for signed
        * mod (especially for % 4 -- a good compiler should just grab
        * the last 2 bits when the LHS is unsigned).
        */
        return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);
    }
}
