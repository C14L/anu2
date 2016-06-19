
window.addEventListener('AutocompleteItemSelected', function(event){
    event.target.style.display = 'none';
    event.target.nextElementSibling.style.display = 'none';
    event.target.parentNode.submit();
});

function getUserCity() {
    return new Promise(function(resolve, reject) {
        if (window.navigator && window.navigator.geolocation) {
            window.navigator.geolocation.getCurrentPosition(
                function(loc, timestamp) {

                    var url = 'dtrcity/api/v1/city-by-latlng.json?latitude=' + loc.coords.latitude + '&longitude=' + loc.coords.longitude + '&accuracy=' + loc.coords.accuracy;

                    var req = new XMLHttpRequest();
                    req.open('GET', url);
                    req.addEventListener('load', function() {
                        if (this.status == 200 && this.response != null) {
                            resolve(JSON.parse(this.response));
                        }
                    });
                    req.addEventListener('loadend', function(){    });
                    req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
                    req.send();
                },
                function (error) {
                    reject();
                },
                {
                    maximumAge: 0, // age of the location data in cache
                    timeout: 10000, // request timeout
                    enableHighAccuracy: true, // may give more accurate results
                }
            );
        } else {
            reject();
        }
    });
}
