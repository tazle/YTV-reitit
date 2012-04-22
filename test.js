var helsinki_center = new google.maps.LatLng(60.1701, 24.9385);

var line_data = [];

var lines = [];

var map = "";

var start_time = 7*60;
var end_time = 9*60;

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

    reset_slider(min, max);
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
    setTimeout("end_timer();",200)
}

function end_timer() {
    update_timers -= 1;
    if (update_timers == 0) {
        update_lines();
    }
}

function reset_slider(begin, end) {
    $( "#slider" ).slider({
	range: true,
	min: begin,
	max: end,
	values: [ max(begin, start_time), min(end, end_time) ],
	slide: function( event, slider ) {
            start_time = slider.values[0];
            end_time = slider.values[1];
            update_ui();
            start_timer();
	}
    });
    $("#range-begin").text(format_hhmm(begin));
    $("#range-end").text(format_hhmm(end));

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
    return max(max_int, last);
}

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
        if (i < 10) {
            console.log(from, to, max_int);
        }
        if (max_int < 10) {
            var path = [new google.maps.LatLng(from[1][1], from[1][0]), new google.maps.LatLng(to[1][1], to[1][0])];
            var line = new google.maps.Polyline({map: map, path: path});
            lines.push(line);
        }
    });
}

function selected_url() {
    return $('input:radio[name=day]:checked').val();
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

    load_line_data(selected_url());
    update_ui();
}

window.onload = initialize;
