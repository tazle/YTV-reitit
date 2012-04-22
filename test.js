var helsinki_center = new google.maps.LatLng(60.1701, 24.9385);

var line_data = [];

var lines = [];

var map = "";

function on_line_data(data, status, jqXHR) {
    console.log("Received line data");
    line_data = data;
    update_lines();
}

function load_line_data() {
    console.log("Loading line data");
    jQuery.getJSON("/test.json", on_line_data)
}

function update_lines() {
    $.each(lines, function(i, line) {
        line.setMap(null);
    });

    lines = [];
    
    console.log("Updating visual lines");
    $.each(line_data, function (i, segment) {
        if (i == 0) {
            console.log(segment);
            console.log(segment[0]);
            console.log(segment[0][1]);
            console.log(segment[0][1][0]);
            console.log(segment[0][1][1]);
        }
        var from = segment[0];
        var to = segment[1];
        var stops = segment[2];
        var path = [new google.maps.LatLng(from[1][1], from[1][0]), new google.maps.LatLng(to[1][1], to[1][0])];
        if (i == 0) {
            console.log(path);
        }
        var line = new google.maps.Polyline({map: map, path: path});
        lines.push(line);
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

    load_line_data();
}



window.onload = initialize;
