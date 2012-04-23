var helsinki_center = new google.maps.LatLng(60.1701, 24.9385);

var line_data = [];

var lines = [];

var map = "";

var start_time = 7*60;
var end_time = 9*60;

var c_short = 5;
var c_medium = 10;
var c_long = 20;
var c_superlong = 30;

function update_slider_range() {
    var min = 36*60;
    var max = 0;
    $.each(line_data, function(i, segment) {
        var stop_times = segment[2];
        var first = stop_times[0];
        var last = stop_times[stop_times.length-1];
        if (first < min) {
            min = first;
        }
        if (last > max) {
            max = last;
        }
    });

    reset_time_slider(min, max);
}

function min(v1, v2) {
    if (v1 < v2) {
        return v2;
    } else {
        return v2;
    }
}

function max(v1, v2) {
    if (v1 > v2) {
        return v1;
    } else {
        return v2;
    }
}

var update_timers = 0;

function start_timer() {
    update_timers += 1;
    setTimeout(end_timer, 200)
}

function end_timer() {
    update_timers -= 1;
    if (update_timers == 0) {
        update_lines();
    }
}

function prevent_line_update() {
    update_timers += 1;
}

function enable_line_update() {
    end_timer();
}

function reset_time_slider(begin, end) {
    $( "#time-slider" ).slider({
	range: true,
	min: begin,
	max: end,
	values: [ max(begin, start_time), min(end, end_time) ],
	slide: function( event, slider ) {
            start_time = slider.values[0];
            end_time = slider.values[1];
            update_ui();
            start_timer();
	},
        start: function(event, slider) {
            prevent_line_update();
        },
        stop: function(event, slider) {
            enable_line_update();
        }
    });
    $("#range-begin").text(format_hhmm(begin));
    $("#range-end").text(format_hhmm(end));

}

function init_color_slider() {
    $( "#color-slider" ).slider({
	min: 0,
	max: 60,
	values: [ 5, 10, 20, 30],
	slide: function( event, slider ) {
            c_short = slider.values[0];
            c_medium = slider.values[1];
            c_long = slider.values[2];
            c_superlong = slider.values[3];
            update_ui();
            start_timer();
	},
        start: function(event, slider) {
            prevent_line_update();
        },
        stop: function(event, slider) {
            enable_line_update();
        }
    });

}

function on_line_data(data, status, jqXHR) {
    console.log("Received line data");
    line_data = data;
    update_slider_range();
    update_lines();
}

function load_line_data(url) {
    console.log("Loading line data");
    jQuery.getJSON(url, on_line_data)
}

function prepend_zero(number) {
    if (number < 10) {
        return "0" + number;
    } else {
        return "" + number;
    }
}

function format_hhmm(tot_minutes) {
    var hours = Math.floor(tot_minutes/60);
    var minutes = tot_minutes%60;
    return prepend_zero(hours) + ":" + prepend_zero(minutes);
}

function update_ui() {
    $("#start").text(format_hhmm(start_time));
    $("#end").text(format_hhmm(end_time));
    $("#short").text(c_short);
    $("#medium").text(c_medium);
    $("#long").text(c_long);
    $("#superlong").text(c_superlong);
}

function max_interval(stops, from, to) {
    var max_int = 0;
    var prev = from;
    $.each(stops, function (i, time) {
        if (time >= from && time <= to) {
            max_int = max(max_int, time - prev);
        }
        prev = time;
    });
    var last = to - prev;
    if (max_int == 0) {
        // Handle empty intervals
        return to-from;
    }
    return max(max_int, last);
}

function get_color(interval) {
    if (interval < c_short) {
        return "#14ff14";
    } else if (interval < c_medium) {
        return "#ffff14"
    } else if (interval < c_long) {
        return "#ff1414";
    } else if (interval < c_superlong) {
        return "#141414";
    } else {
        return null;
    }
}

function format_stops(stops) {
    var result = [];
    result.push("<ul>");
    $.each(stops, function(i, time) {
        if (time >= start_time && time <= end_time) {
            result.push("<li>" + format_hhmm(time) + "</li>");
        }
    });
    result.push("</ul>");
    return result.join("");
}

var zs = {
    "#14ff14": 4,
    "#ffff14": 3,
    "#ff1414": 2,
    "#141414": 1,
    };

function update_lines() {
    $.each(lines, function(i, line) {
        line.setMap(null);
    });

    lines = [];

    console.log("Updating visual lines");
    $.each(line_data, function (i, segment) {
        var from = segment[0];
        var to = segment[1];
        var stops = segment[2];
        var max_int = max_interval(stops, start_time, end_time);
        var color = get_color(max_int);
        var z = zs[color];
        if (color != null) {
            var path = [new google.maps.LatLng(from[1][1], from[1][0]), new google.maps.LatLng(to[1][1], to[1][0])];
            var line = new google.maps.Polyline({map: map, path: path, strokeColor: color, zIndex: z});
            var infowindow = null;
            google.maps.event.addListener(line, 'click', function(event) {
                if (infowindow == null) {
                    infowindow = new google.maps.InfoWindow({
                        content: format_stops(stops),
                        position: event.latLng,
                    });
                }
                infowindow.setPosition(event.latLng);
                infowindow.open(map);
            });
            lines.push(line);
        }
    });
}

function selected_url() {
    return $('input:radio[name=day]:checked').val();
}

function on_click() {
    var infowindow = new google.maps.InfoWindow({
        content: contentString
    });
}

function initialize() {
    var myOptions = {
        zoom: 16,
        center: helsinki_center,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
    map.setCenter(helsinki_center);
    map.setZoom(16);

    $('input:radio[name=day]').click(function () {
        console.log("Clicked radiobutton");
        load_line_data(selected_url());
    });

    init_color_slider();
    load_line_data(selected_url());
    update_ui();
}

window.onload = initialize;
