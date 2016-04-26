angular.module('anu2app', ['ngRoute', 'ngMaterial', 'ng-showdown', 'imageupload'])

.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider){
    $locationProvider.html5Mode(true);
    $routeProvider
    .when( '/', {
        controller: 'HomeController', // show home page
        templateUrl: 'home.html'
    })
    .when( '/:country/:region/:city', {
        controller: 'LocationController',
        templateUrl: 'location.html'
    })
    .when( '/:country/:region/:city/:cgroup', {
        controller: 'CategoryGroupController',
        templateUrl: 'categorygroup.html'
    })
    .when( '/:country/:region/:city/:cgroup/:category', {
        controller: 'CategoryController',
        templateUrl: 'category.html'
    })
    .when( '/:country/:region/:city/:cgroup/:category/add', {
        controller: 'PostCreateController',
        templateUrl: 'post-create.html'
    })
    .when( '/:country/:region/:city/:cgroup/:category/:postid', {
        controller: 'PostDetailController',
        templateUrl: 'post-detail.html'
    })
    .otherwise({ redirectTo: '/' });
}])

.run(['$rootScope', '$window', '$location', '$http', function($rootScope, $window, $location, $http){
  $rootScope.addFabStatus = true;
  $rootScope.categories = [];
  $rootScope.categoryTree = {};
  $rootScope.site = {
    'title': 'Anuncios1.com'
  };
  $rootScope.page = {
    'h1': 'Anuncios Clasificados',
    'title': 'Anuncios Clasificados - Anuncios1.com',
    'home_url': '/',
  };

  $rootScope.categoriesPromise = $http.get('/api/v1/categories/').then(
    function(res){
      $rootScope.categories = res['data']['categories'];

      // Build a tree from the categories list.
      for (var i=0; i<$rootScope.categories.length; i++){
        var item = $rootScope.categories[i];
        if (!item['parent']){
          $rootScope.categoryTree[item['slug']] = item;
          $rootScope.categoryTree[item['slug']]['children'] = [];
        }
      }

      for (var i=0; i<$rootScope.categories.length; i++){
        var item = $rootScope.categories[i];
        if (item['parent']){
          if ($rootScope.categoryTree[item['parent']]){
            $rootScope.categoryTree[item['parent']]['children'].push(item)
          } else {
            log('Can not add item "'+item['slug']+'", because parent "'+item['parent']+'" does not exist!');
          }
        }
      }
    }
  );

  // Allow the FAB "add" button to show the "add post" page.
  $rootScope.setAddFabStatus = function(val) {
    $rootScope.addFabStatus = val;
  }

  // Do stuff each time the route successfully changes.
  $rootScope.$on('$routeChangeSuccess', function(event) {
      $rootScope.path = $location.path();
      //$window.ga('send', 'pageview', { page: $location.path() });
  });

  // Wrapper for the tr() translation function.
  $rootScope.tr = function (str, arr) {
    return tr(str, arr);
  }

  // Return category by slug, including parent etc data.
  $rootScope.getCategory = function(slug){
    var li = $rootScope.categories.filter(function(el){ return el.slug == slug; });
    if (li.length < 1) return null;
    if (li.length > 0) {
      if (typeof(li[0]['parent']) === 'string'){
        li[0]['parent'] = $rootScope.getCategory(li[0]['parent']);
      }
      return li[0];
    }
  };
}]);
