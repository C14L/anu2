;(function () {
    'use strict';
    angular.module('anu2app')

    .factory('GeolocFinder', ['$q', '$http', '$window', function GeolocFinderFactory ($q, $http, $window) {
        // Return the geolocation from the browser API, then query dtrcity for the
        // name of the nearest city and resolve by returning the city's data object.
        var deferred = $q.defer();

        if ($window.navigator && $window.navigator.geolocation) {
            $window.navigator.geolocation.getCurrentPosition(
                function (loc, timestamp) {
                    var url = 'dtrcity/api/v1/city-by-latlng.json';
                    var params = { 'latitude': loc.coords.latitude,
                                   'longitude': loc.coords.longitude,
                                   'accuracy': loc.coords.accuracy };
                    $http.get(url, {params:params}).then(
                        function (response) {
                            deferred.resolve(response.data);
                        },
                        function (response) {
                            log('No city data received from server.');
                            deferred.reject();
                        }
                    );
                },
                function (error) {
                    log('Browser geolocation API returned an error.');
                    deferred.reject();
                },
                {
                    maximumAge: 0, // age of the location data in cache
                    timeout: 10000, // request timeout
                    enableHighAccuracy: true, // may give more accurate results
                });
        } else {
            log('Browser geolocation API not found.');
            deferred.reject();
        }

        return deferred.promise;
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

        function getItem (postid) {
            // Load a single post by Id, either from cache or from server.
            return new Promise(function (resolve, reject) {
                $http.get('api/v1/posts/' + postid + '/').then(
                    function (response) { resolve(_complete_fields(response.data)); },
                    function (response) { reject(); }
                );
            });
        }

        function getList (city_url, cgroup, category, page) {
            // Get a list of items by URL.
            //
            // city_url - URL fragment "country/region/city".
            // cgroup - Category group slug.
            // category - Category slug.

            // Check for cache.
            var deferred = $q.defer();
            var basepath = '/' + city_url + '/' + cgroup  + '/' + category;
            var list_for = basepath + '?page=' + page;

            // Check if the data in cache is for this item's URL.
            if (list_cache_for && list_cache_for === list_for){
                deferred.resolve(list_cache);
            }

            // Not cached, get from server.
            var url = 'api/v1/posts/';
            var params = { city_url:city_url, cgroup:cgroup, category:category, dist:50, page:page };

            $http.get(url, {params:params}).then(
                function (response) {
                    list_cache_for = list_for;
                    list_cache = response.data;

                    // Fill in addition fields.
                    if (list_cache.results)
                        for (var i=0; i<list_cache.results.length; i++)
                          list_cache.results[i] = _complete_fields(list_cache.results[i]);

                    // Extract the actual "previous" and "next" page numbers.
                    var result = (/\Wpage=(\d+)/g).exec(list_cache['previous']);
                    list_cache['previous_page'] = result ? result[1] : null;
                    list_cache['previous'] = result ? basepath + '?page=' + result[1] : null;
                    if (page == 2) list_cache['previous'] = basepath // special case, only the path with no page number.
                    var result = (/\Wpage=(\d+)/g).exec(list_cache['next']);
                    list_cache['next_page'] = result ? result[1] : null;
                    list_cache['next'] = result ? basepath + '?page=' + result[1] : null;

                    // Resolve.
                    deferred.resolve(list_cache);
                },
                function (response) {
                    deferred.reject();
                }
            );

            return deferred.promise;
        }

        return {
            getItem: getItem,
            getList: getList,
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