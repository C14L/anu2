;(function () {
    'use strict';
    angular.module('anu2app')

    .controller('HomeController', ['$scope', '$http', '$window', 'GeolocFinder', function ($scope, $http, $window, GeolocFinder) {
    
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
    
    .controller('LocationController', ['$scope', '$q', '$routeParams', 'Geoloc', function ($scope, $q, $routeParams, Geoloc) {
        $scope.geolocPromise = Geoloc.getByUrl().then(function (data) { $scope.geoloc = data });
        $q.all([$scope.geolocPromise, $scope.categoriesPromise]).then(function () {
            $scope.category = $scope.getCategory($routeParams['category']);
            $scope.page['home_url'] = '/';
            $scope.page['title'] = tr("Anuncios Clasificados en {0}", [$scope.geoloc['crc']]);
            $scope.page['h1'] = $scope.page['title'];
            $scope.page['description'] = tr("Todos los anuncios clasificados para {0} y alrrededores, encuentra las mejores ofertas para {1} y artículos raros mas interesantes de {2}.", [$scope.geoloc['crc'], $scope.geoloc['name'], $scope.geoloc['country_name']]);
            setTitle($scope.page['title']);
            setDescription($scope.page['description']);
        });
    }])
    
    .controller('CategoryController', ['$scope', '$q', '$routeParams', 'Geoloc', 'Posts', function ($scope, $q, $routeParams, Geoloc, Posts) {
        var item_url = $routeParams.country + '/' + $routeParams.region + '/' + $routeParams.city;
        var fab_url = item_url  + '/' + $routeParams.cgroup  + '/' + $routeParams.category;

        $scope.setAddFabStatus(fab_url);
        $scope.geolocPromise = Geoloc.getByUrl().then(function(data){ $scope.geoloc = data });
        $scope.postsPromise = Posts.getList(item_url, $routeParams.cgroup, $routeParams.category, $routeParams.page||1).then(function (data) { $scope.posts = data; });
        // When city data and category data promises resolve, show the page with all ads for this city.
        $q.all([$scope.postsPromise, $scope.geolocPromise, $scope.categoriesPromise]).then(_resolve, _reject);

        function _resolve () {
            $scope.category = $scope.getCategory($routeParams['category']);

            // If any results, prepare URL properties for each post.
            if ($scope.posts.results)
                for (var i=0; i<$scope.posts.results.length; i++)
                    $scope.posts.results[i]['url'] = '/' + $scope.geoloc['url'] + '/' + $scope.category['parent']['slug'] + '/' + $scope.category['slug'] + '/' + $scope.posts.results[i]['id'];

            // Prepare page values.
            $scope.page['home_url'] = '/' + $scope.geoloc['url'];
            $scope.page['title'] = tr("{2} > {0} > {1} > {3} Clasificados", [$scope.category['parent']['title'], $scope.category['title'], $scope.geoloc['city_name'], $scope.posts.count||0]);
            $scope.page['h1'] = $scope.page['title'];
            $scope.page['description'] = tr("{0} de {1} en {2} y alrrededores. Publica y encuentra anuncions clasificados sobre {1} para {3} en esta seccion.", [$scope.category['parent']['title'], $scope.category['title'], $scope.geoloc['crc'], $scope.geoloc['city_name']]);
            setTitle($scope.page['title']);
            setDescription($scope.page['description']);
        }

        function _reject () {}
    }])
    
    .controller('CategoryGroupController', ['$scope', '$q', '$routeParams', 'Geoloc', function ($scope, $q, $routeParams, Geoloc) {
        $scope.geolocPromise = Geoloc.getByUrl().then(function(data){ $scope.geoloc = data });

        $q.all([$scope.geolocPromise, $scope.categoriesPromise]).then(
            function () {
                $scope.page['home_url'] = '/' + $scope.geoloc['url'];
                $scope.page['title'] = tr("", []);
                $scope.page['h1'] = $scope.page['title'];
                $scope.page['description'] = "";
                setTitle($scope.page['title']);
                setDescription($scope.page['description']);
            }
        );
    }])
    
    .controller('PostItemController', ['$scope', '$q', '$routeParams', 'Geoloc', 'Posts', function ($scope, $q, $routeParams, Geoloc, Posts) {
        var item_url = $routeParams.country + '/' + $routeParams.region + '/' + $routeParams.city;
        var fab_url = item_url  + '/' + $routeParams.cgroup  + '/' + $routeParams.category;

        $scope.setAddFabStatus(fab_url);
        $scope.geolocPromise = Geoloc.getByUrl().then(function (data) { $scope.geoloc = data });
        $scope.postPromise = Posts.getItem($routeParams.postid).then(function (data) { $scope.post = data; });

        $q.all([$scope.postPromise, $scope.geolocPromise, $scope.categoriesPromise]).then(
            function () {
                $scope.category = $scope.getCategory($routeParams['category']);
                $scope.page['home_url'] = '/' + $scope.geoloc['url'] + '/' + $routeParams.cgroup  + '/' +  $routeParams.category;
                $scope.page['title'] = $scope.post['title'] + ' (' + $scope.geoloc['crc'] + ')';
                $scope.page['h1'] = $scope.post['title'];
                $scope.page['description'] = "";
                setTitle($scope.page['title']);
                setDescription($scope.page['description']);
            }
        );
    }])
    
    .controller('AddPostItemController', ['$scope', '$q', '$http', '$routeParams', 'Geoloc', 'Posts', function ($scope, $q, $http, $routeParams, Geoloc, Posts) {
        $scope.setAddFabStatus(0); // 0=hide fab
        $scope.geolocPromise = Geoloc.getByUrl().then(function(data){ $scope.geoloc = data });
        $scope.postPromise = Posts.getItem($routeParams.postid).then(function(data){ $scope.post = data; });

        $q.all([$scope.postPromise, $scope.geolocPromise, $scope.categoriesPromise]).then(_run);

        function _run () {
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
        }
    }])
    
    .controller('AppController', ['$scope', '$mdSidenav', '$mdDialog', '$routeParams', 'Geoloc', function ($scope, $mdSidenav, $mdDialog, $routeParams, Geoloc) {
        $scope.addFabPath = '';  // ???

        $scope.toggleSidenav = function (menuId) {
            $mdSidenav(menuId).toggle();
        }
        $scope.sidebarList = [
            { title: "Some title", description: "And the description for the some title.", done: true },
            { title: "Another one", description: "Another description for another title.", done: false }];

        $scope.addFabInfoDialog = function (ev) {
            $mdDialog
                .show($mdDialog.alert()
                .parent(angular.element(document.querySelector('#popupContainer')))
                .clickOutsideToClose(true).title(tr('Selecciona la categoria'))
                .content(tr('Para agregar un anuncio, primero selecciona la categoria en la cual lo quieres publicar.'))
                .ariaLabel(tr('Selecciona una categoria'))
                .ok(tr('Cerrar'))
                .targetEvent(ev));
        }
    }]);

})();
