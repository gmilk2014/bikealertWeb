var SF = new google.maps.LatLng(37.552,-122.1419);
var markers = [];
var infowindows = [];
var map;
var top3 = [];
var low3 = [];

function deploy_stations() {
    $.getJSON('/location',
              function(data) {
                  var locations = data.locations;
                  console.log(locations)
                  for (var i = 0; i < locations.length; i = i + 1) {
                      for (var j = 0; j < locations[i].length; j = j + 1) {
                          var l = locations[i][j];
                          addMarker(new google.maps.LatLng(l.lat, l.lon), l.id);

                      }
                  }
            });
}

function initialize() {
    var mapOptions = {
        zoom: 9,
        center: SF
    };
    var mapDiv = document.getElementById('map-canvas')
    map = new google.maps.Map(document.getElementById('map-canvas'),
                              mapOptions);
}

function update_values() {
    $.getJSON('/realtime',
              function(data) {
                  var bikes = data.bikes;
                  for (var i = 0; i < bikes.length; i = i + 1) {
                      var l = [];
                      var t = [];
                      for (var j = 0; j < 3; j = j + 1){
                          var id = [bikes[i][j].stationid, bikes[i][bikes[i].length - 1 - j].stationid];
                          var index = [parseInt(id[0]) - 1, parseInt(id[1]) - 1];
                          var info = [infowindows[index[0]], infowindows[index[1]]];
                          var marker = [markers[index[0]], markers[index[1]]];
                          l.push(index[0]);
                          t.push(index[1]);
                          if (low3.length < 10) {
                              marker[0].setIcon(null);
                              marker[1].setIcon('https://maps.gstatic.com/mapfiles/ms2/micons/green-dot.png');
                              marker[1].setAnimation(google.maps.Animation.BOUNCE);
                          }
                          else {
                              var low_index = low3[i][j];
                              var m = markers[low_index];
                              m.setIcon('https://maps.gstatic.com/mapfiles/ms2/micons/blue-dot.png');
                              if (m.getAnimation() != null) {
                                  m.setAnimation(null);
                              }
                              marker[0].setIcon(null);
                              
                              var top_index = top3[i][j];
                              m = markers[top_index];
                              m.setIcon('https://maps.gstatic.com/mapfiles/ms2/micons/blue-dot.png');
                              if (m.getAnimation() != null) {
                                  m.setAnimation(null);
                              }
                              marker[1].setIcon('https://maps.gstatic.com/mapfiles/ms2/micons/green-dot.png');
                              if (marker[1].getAnimation() == null) {
                                  marker[1].setAnimation(google.maps.Animation.BOUNCE);
                              }                                           
                          }
                          setInfoContent(id[0], index[0]);
                          setInfoContent(id[1], index[1]);

                      } // end inner for
                  top3[i] = t;
                  low3[i] = l;
                  } // end outer for
            }); // end function
    window.setTimeout(update_values, 10000);
}
update_values();

function setInfoContent(id, index) {
  var info = infowindows[index];
  $.getJSON('/bikecount/' + id, function(data) {
    var count = data.count;
    info.setContent('<div>'
                    + '<p> ID:' + id + '</p>'
                    + '<p> number of bikes:' + count + '</p>'
                    + '</div>');
  });

}

function drop(lat, lng) {
    var point  = new google.maps.LatLng(lat,lng);
    clearMarkers();
    addMarker(point);
}
function addMarker(position, id) {
    var m = new google.maps.Marker({
        position: position,
        map: map,
        title: id.toString(),
        icon:'https://maps.gstatic.com/mapfiles/ms2/micons/blue-dot.png'
    });
    var infowindow = new google.maps.InfoWindow({
        content: '<div>'
                 + '<p> ID:' + id + '</p>'
                 + '</div>'
    });

    google.maps.event.addListener(m, 'click', function() {
        infowindow.open(map, m);
    });

    infowindows.push(infowindow);
    markers.push(m);
}


function clearMarkers() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
}
deploy_stations();
google.maps.event.addDomListener(window, 'load', initialize);

