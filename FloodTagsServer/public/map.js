var myCenter = new google.maps.LatLng(51.508742, -0.120850);
var map;
function initialize() {
    var mapProp = {
        center: myCenter,
        zoom: 5,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
    /*
    var marker = new google.maps.Marker({
        position: myCenter,
    });

    marker.setMap(map);*/
}

function addMark() {
    var loc = new google.maps.LatLng(52.073762, 4.33314);
    var marker = new google.maps.Marker({
        position: loc,
    });
    marker.setMap(map);
}
function addMark(lat, long) {
    var loc = new google.maps.LatLng(lat, long);
    var marker = new google.maps.Marker({
        position: loc,
    });
    marker.setMap(map);
}

function codeAddress() {
    geocoder = new google.maps.Geocoder();
    var address = document.getElementById("my-address").value;
    geocoder.geocode({'address': address}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            addMark(results[0].geometry.location.lat(), results[0].geometry.location.lng())
            alert("Latitude: " + results[0].geometry.location.lat());
            alert("Longitude: " + results[0].geometry.location.lng());
        }

        else {
            alert("Geocode was not successful for the following reason: " + status);
        }
    });
    //var location = $.getJSON("/get_location/" + )
}

function codeAddress(location) {
    geocoder = new google.maps.Geocoder();

    geocoder.geocode({'address': location}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            addMark(results[0].geometry.location.lat(), results[0].geometry.location.lng())
            //alert("Latitude: " + results[0].geometry.location.lat());
            //alert("Longitude: " + results[0].geometry.location.lng());
        }
        else {
            console.log("we oopsed")
            //alert("Geocode was not successful for the following reason: " + status);
        }
    });

}

function ownAddress(location){
    var address
    $.getJSON("/get_location?location=" + location, function(data){
        addMark(data.lat, data.lon)
    })
}

google.maps.event.addDomListener(window, 'load', initialize);