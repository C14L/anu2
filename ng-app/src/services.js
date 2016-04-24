;(function () {
    'use strict';
    angular.module('anu2app')

    .factory('GeolocFinder', ['$http', '$window', function GeolocFinderFactory ($http, $window) {
        // Return the geolocation from the browser API, then query dtrcity for the
        // name of the nearest city and resolve by returning the city's data object.
        return new Promise(function (_resolve, _reject) {
            if ($window.navigator && $window.navigator.geolocation) {
                $window.navigator.geolocation.getCurrentPosition(
                    function (loc, timestamp) {
                        var url = 'dtrcity/api/v1/city-by-latlng.json';
                        var params = { 'latitude': loc.coords.latitude,
                                       'longitude': loc.coords.longitude,
                                       'accuracy': loc.coords.accuracy };
                        $http.get(url, {params:params}).then(
                            function (response) {
                                _resolve(response.data);
                            },
                            function (response) {
                                log('No city data received from server.');
                                _reject();
                            }
                        );
                    },
                    function (error) {
                        log('Browser geolocation API returned an error.');
                        _reject();
                    },
                    {
                        maximumAge: 0, // age of the location data in cache
                        timeout: 10000, // request timeout
                        enableHighAccuracy: true, // may give more accurate results
                    });
            } else {
                log('Browser geolocation API not found.');
                _reject();
            }
        });
    }])

    .factory('Categories', ['$q', '$http', function CategoriesFactory($q, $http){
        // TODO: Return the list of categories. First from $http then from buffer.
    }])

    .factory('Posts', ['$q', '$http', '$sce', function PostsFactory ($q, $http, $sce) {
        var list_cache_for = null; // URL path for cached list.
        var list_cache = []; // List of Post data items.

        function _complete_fields (post) {
            post['text_html'] = $sce.trustAsHtml(textfilter(post['text']));
            // Set true or false if the ad is already expired.
            post['expired'] = (new Date(post['expires'])) < (new Date());
            return post;
        }

        // Load a single post by Id, either from cache or from server.
        function getItem (postid) {
            return new Promise(function (_resolve, _reject) {
                $http.get('api/v1/posts/' + postid + '/').then(
                    function (response) { _resolve(_complete_fields(response.data)); },
                    function (response) { _reject(); }
                );
            });
        }

        // Return the ready-made URL to load a Post list for the given values.
        function getListUrl (city_url, cgroup, category, page) {
            var url = '/api/v1/posts/';
            var params = { city_url: city_url, cgroup: cgroup, category: category, dist: 50, page: page||'1' };
            return url + '?' + Object.keys(params).map(function (k) { return encodeURIComponent(k) + "=" + encodeURIComponent(params[k]) }).join('&');
        }

        // Get a list of items by URL.
        function getList (url) {
            return new Promise(function (_resolve, _reject){
                $http.get(url).then(
                    function (response) {
                        response.data.results.map(function (k) { k = _complete_fields(k) });
                        _resolve(response.data);
                    },
                    function (response) {
                        _reject();
                    });
                }
            );
        }

        return {
            getItem: getItem,
            getList: getList,
            getListUrl: getListUrl,
        };
    }])

    .factory('Geoloc', ['$q', '$http', '$routeParams', function GeolocFactory ($q, $http, $routeParams) {
        /* Return data on current geographic location, either from buffer or $http request */
        var buffer = [];  // Buffer previous location items.
        var maxbuf = 100; // Fifo-remove older items.

        function getByUrl (item_url) {
            var deferred = $q.defer();
            var found = false;

            if (typeof(item_url) === 'undefined') {
                if ($routeParams.country && $routeParams.region && $routeParams.city) {
                    // log($routeParams.country, $routeParams.region, $routeParams.city);
                    var item_url = $routeParams.country + '/' + $routeParams.region + '/' + $routeParams.city;
                }
            }

            if (typeof(item_url) === 'undefined') {
                deferred.reject();
            } else {
                for (var i=0; i<buffer.length; i++) {
                    // Try to find in buffer
                    if (buffer[i]['url'] == item_url) {
                        deferred.resolve(buffer[i]);
                        found = true;
                    }
                }

                if (!found) {
                    // Not in buffer, load from server.
                    var url = '/dtrcity/api/v1/' + item_url + '.json';
                    $http.get(url).then(
                        function(response) { deferred.resolve(response.data); },
                        function (response) { deferred.reject(); }
                    );
                }
            }

            return deferred.promise;
        }

        return {
            getByUrl: getByUrl,
        };
    }]);

})();