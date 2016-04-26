;(function () {
    'use strict';
    angular.module('anu2app')

    .controller('HomeController', ['$scope', '$http', '$window', 'GeolocFinder', function HomeController ($scope, $http, $window, GeolocFinder) {

        $scope.page['title'] = tr("Anuncios Clasificados", []);
        $scope.page['h1'] = $scope.page['title'];
        $scope.page['description'] = tr("Anuncios clasificados locales de tu ciudad, encuentra todas las mejores ofertas y artículos interesantes.", []);
        setTitle($scope.page['title']);
        setDescription($scope.page['description']);

        // Return a list of matches for the autocomplete input city finder.
        $scope.getMatches = function (searchText) {
            if (searchText.length < 2) return [];
            var url = '/dtrcity/api/v1/autocomplete-crc.json';
            var params = { 'params': { 'q': searchText, 'fields':'crc url' }};
            return $http.get(url, params).then(
                function(response){
                    return response.data;
                }
            );
        };

        // Once we have a geolocation, call this to redirect to geoloc's page.
        $scope.locationSelected = function (item) {
            if (item) $window.location.href = item.url;
        }

        // Try to get the user's geolocation and redirect them to their own city's
        // content page automatically. See http://diveintohtml5.info/geolocation.html
        // The browser's "loc" object contains user's latitude and longitude in the
        // loc.coords.latitude and loc.coords.longitude properties. Look up  the
        // nearest city in Geonames database.
        $scope.isManualCityFinder = false; // don't show manual input field.
        $scope.isSearchingLocation = true; // do show loading indicator.
        $scope.GeolocFinderPromise = GeolocFinder.then(
            function (cityItem) {
                log('Geolocation received from API, our city is "' + cityItem.crc + '", now redirecting...');
                $scope.isSearchingLocation = false;
                $scope.locationSelected(cityItem);
            },
            function () {
                log('No geolocation from API, switch to manual!')
                $scope.isSearchingLocation = false;
                $scope.isManualCityFinder = true;
            }
        );
    }])
    
    .controller('LocationController', ['$scope', '$q', '$routeParams', 'Geoloc', function LocationController ($scope, $q, $routeParams, Geoloc) {
        $scope.geolocPromise = Geoloc.getByUrl().then(function (data) { $scope.geoloc = data });

        $q.all([$scope.geolocPromise, $scope.categoriesPromise]).then(function () {
            $scope.addFabStatus = false;
            $scope.category = $scope.getCategory($routeParams['category']);
            $scope.page['home_url'] = '/';
            $scope.page['title'] = tr("Anuncios Clasificados en {0}", [$scope.geoloc['crc']]);
            $scope.page['h1'] = $scope.page['title'];
            $scope.page['description'] = tr("Todos los anuncios clasificados para {0} y alrrededores, encuentra las mejores ofertas para {1} y artículos raros mas interesantes de {2}.", [$scope.geoloc['crc'], $scope.geoloc['name'], $scope.geoloc['country_name']]);
            setTitle($scope.page['title']);
            setDescription($scope.page['description']);
        });
    }])

    .controller('CategoryController', ['$scope', '$routeParams', 'Geoloc', 'Posts', function CategoryController ($scope, $routeParams, Geoloc, Posts) {
        $scope.crcUrl = url_path_join($routeParams.country, $routeParams.region, $routeParams.city);
        $scope.fabUrl = url_path_join($scope.crcUrl, $routeParams.cgroup, $routeParams.category, 'add');
        $scope.posts = { results: [] };
        $scope.geolocPromise = Geoloc.getByUrl();
        $scope.load = function (url) {
            // Load the url and show the resulting page of Post items.
            $scope.loading = true;
            $scope.postsPromise = Posts.getList(url);

            // When city data and category data promises resolve, show the page with all ads for this city.
            Promise.all([$scope.geolocPromise, $scope.postsPromise]).then(
                function (dataList) {
                    $scope.category = $scope.getCategory($routeParams['category']);
                    $scope.geoloc = dataList[0];

                    var posts = dataList[1];
                    $scope.posts.next = posts.next;
                    $scope.posts.count = posts.count;
                    $scope.posts.results.push.apply($scope.posts.results, posts.results.map(function (k, i) {
                        k['url'] = url_path_join('/', $scope.geoloc['url'], $scope.category['parent']['slug'], $scope.category['slug'], k['id']);
                        return k;
                    }));

                    $scope.page['home_url'] = '/' + $scope.geoloc['url'];
                    $scope.page['title'] = tr("{2} > {0} > {1} > {3} Clasificados", [$scope.category['parent']['title'], $scope.category['title'], $scope.geoloc['city_name'], $scope.posts.count || 0]);
                    $scope.page['h1'] = $scope.page['title'];
                    $scope.page['description'] = tr("{0} de {1} en {2} y alrrededores. Publica y encuentra anuncions clasificados sobre {1} para {3} en esta seccion.", [$scope.category['parent']['title'], $scope.category['title'], $scope.geoloc['crc'], $scope.geoloc['city_name']]);
                    setTitle($scope.page['title']);
                    setDescription($scope.page['description']);

                    $scope.loading = false;
                    $scope.$apply();
                }
            );
        }

        var postUrl = Posts.getListUrl($scope.crcUrl, $routeParams.cgroup, $routeParams.category, $routeParams.page || 1);
        $scope.load(postUrl);
    }])
    
    .controller('CategoryGroupController', ['$scope', '$routeParams', 'Geoloc', function CategoryGroupController ($scope, $routeParams, Geoloc) {
        $scope.geolocPromise = Geoloc.getByUrl();

        Promise.all([$scope.geolocPromise, $scope.categoriesPromise]).then(
            function (dataList) {
                $scope.geoloc = dataList[0];
                $scope.page['home_url'] = '/' + $scope.geoloc['url'];
                $scope.page['title'] = tr("", []);
                $scope.page['h1'] = $scope.page['title'];
                $scope.page['description'] = "";
                setTitle($scope.page['title']);
                setDescription($scope.page['description']);
            }
        );
    }])
    
    .controller('PostDetailController', ['$scope', '$routeParams', 'Geoloc', 'Posts', function PostDetailController ($scope, $routeParams, Geoloc, Posts) {
        $scope.geolocPromise = Geoloc.getByUrl();
        $scope.postPromise = Posts.getItem($routeParams.postid);
        $scope.crcUrl = url_path_join($routeParams.country, $routeParams.region, $routeParams.city);
        $scope.fabUrl = url_path_join($scope.crcUrl, $routeParams.cgroup, $routeParams.category, 'add');

        Promise.all([$scope.postPromise, $scope.geolocPromise, $scope.categoriesPromise]).then(
            function (dataList) {
                $scope.post = dataList[0];
                $scope.geoloc = dataList[1];
                $scope.category = $scope.getCategory($routeParams['category']);

                $scope.page['home_url'] = url_path_join($scope.geoloc['url'], $routeParams.cgroup, $routeParams.category);
                $scope.page['title'] = $scope.post['title'] + ' (' + $scope.geoloc['crc'] + ')';
                $scope.page['h1'] = $scope.post['title'];
                $scope.page['description'] = "";
                setTitle($scope.page['title']);
                setDescription($scope.page['description']);

                $scope.$apply();
            }
        );
    }])
    
    .controller('AppController', ['$scope', '$mdMedia', '$mdSidenav', '$mdDialog', '$routeParams', 'Geoloc', function AppController ($scope, $mdMedia, $mdSidenav, $mdDialog, $routeParams, Geoloc) {
        $scope.isSidenavOpen = false;
        $scope.toggleSidenav = function (menuId) { $mdSidenav(menuId).toggle() };

        $scope.sidebarList = [
            { title: "Some title", description: "And the description for the some title.", done: true },
            { title: "Another one", description: "Another description for another title.", done: false }];

        $scope.addPostDialog = function (ev) {
            var useFullScreen = ($mdMedia('sm') || $mdMedia('xs'))  && $scope.customFullscreen;
            $mdDialog.show({
                controller: ['$rootScope', '$scope', '$http', '$routeParams', 'Geoloc', 'Posts', addPostDialogController],
                templateUrl: 'add-post-dialog.html',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                fullscreen: useFullScreen,
            })
            .then(function(answer) {
                $scope.setAddFabStatus(1);
                $scope.status = 'You said the information was "' + answer + '".';
            }, function() {
                $scope.setAddFabStatus(1);
                $scope.status = 'You cancelled the dialog.';
            });

            $scope.$watch(function() {
                return $mdMedia('xs') || $mdMedia('sm');
            }, function(wantsFullScreen) {
                $scope.customFullscreen = (wantsFullScreen === true);
            });
        };
    }])

    .controller('PostCreateController', ['$rootScope', '$scope', '$http', '$routeParams', 'Geoloc', 'Posts', function PostCreateController ($rootScope, $scope, $http, $routeParams, Geoloc, Posts) {
        $rootScope.setAddFabStatus(0); // 0=hide fab
        $scope.geolocPromise = Geoloc.getByUrl();
        $scope.postPromise = Posts.getItem($routeParams.postid);

        Promise.all([$scope.postPromise, $scope.geolocPromise, $scope.categoriesPromise]).then(
            function (dataList) {
                $scope.post = dataList[0];
                $scope.geoloc = dataList[1];
                $scope.category = $scope.getCategory($routeParams['category']);

                $scope.expiresDeltaOptions = [["7", "1 semana"], ["30", "1 mes"], ["91", "3 meses"], ["365", "1 año"], ["1095", "3 años"]];
                $scope.page['home_url'] = '/' + $scope.geoloc['url'] + '/' + $routeParams.cgroup  + '/' +  $routeParams.category;
                $scope.page['title'] = tr('Agregar nuevo anuncio');
                $scope.page['h1'] = $scope.page['title'];
                $scope.page['description'] = tr('Agregar nuevo anuncio a la categoria {0} en la ciudad de {1}, {2}.', [$scope.category['title'], $scope.geoloc['city_name'], $scope.geoloc['country_name'] ]);
                setTitle($scope.page['title']);
                setDescription($scope.page['description']);

                $scope.addpost = {
                  'lat': $scope.geoloc.lat,
                  'lng': $scope.geoloc.lng,
                  'category': $routeParams['category'],
                  'pics': [{}, {}, {}, {}], // show 4 empty pic slots.
                };

                $scope.addpostSubmit = function (ev) { // Submit new post.
                    var url = "api/v1/posts/";
                    var params = $scope.addpost;
                    log('Pics length: ' + $scope.addpost['pics'].length);

                    for (var i=0; i<params['pics'].length; i++) { //submit only the resized base64 values.
                        log('Doing pic '+i);
                        if (params['pics'][i]['resized'] && params['pics'][i]['resized']['dataURL']) {
                            log('Attach pic "'+i+'" with "'+params['pics'][i]['resized']['dataURL'].length+'" Bytes.')
                            params['pics'][i] = params['pics'][i]['resized']['dataURL'];
                        } else {
                            params['pics'][i] = '';
                        }
                    }

                    $http.post(url, { params: params }).then(
                        function (response) {
                            log('OK');
                            log(response);
                        },
                        function (response) {
                            log('ERROR');
                            log(response);
                        }
                    );
                };
            },
            function () {
            }
        );
    }]);

})();
