var myModule = angular.module('my_app', ['ngResource','ngRoute', 'AuthServices']);

myModule.config(function ($routeProvider, $locationProvider){
    $locationProvider.html5Mode({enabled:true, requireBase:false});
    $routeProvider.
        when("/", {
            templateUrl: "/index.html", controller:"AppCtrl"
        }).
        when("/new", {
            templateUrl: "/partials/edit.html", controller:"NewCtrl"
        }).
        when("/edit:id", {
            templateUrl: "/partials/edit.html", controller:"EditCtrl"
        }).
        when("/login", {
            templateUrl: "/partials/login.html", controller:"LoginCtrl"
        }).
        otherwise({redirectTo:'/'})
});
myModule.controller('AppCtrl', function ($scope, $rootScope, $location, Auth) {
    $rootScope.logout = function(){
        Auth.logout();
        $location.path("/login");
      };

    $scope.crew = [
        {name:"Picard", description:"Captain"},
        {name:"Riker", description:"Number One"},
        {name:"Worf", description:"Security"},
    ];
});

myModule.controller('NewCtrl', function ($scope, $location) {
    $scope.person = {name: '',description: ''};

    $scope.save = function() {
        $scope.crew.push($scope.person);
        $location.path("/");
    }
});

myModule.controller('EditCtrl', function ($scope, $location, $routeParams) {
    $scope.person = $scope.crew[$routeParams.id];

    $scope.save = function() {
        $location.path("/");
    }
});

myModule.controller('LoginCtrl', function($scope, $location, Auth) {
    $scope.email = "";
    $scope.password = "";
    $scope.failed = false;

    $scope.login = function() {
        Auth.login($scope.email, $scope.password)
          .then(function() {
              $location.path("/");
          }, function() {
              $scope.failed = true;
          });
    };
});

myModule.run(['$rootScope', '$location', 'Auth', function ($rootScope, $location, Auth) {
    Auth.init();
    $rootScope.$on('$routeChangeStart', function (event, next) {
        if (!Auth.isLoggedIn()){
            if (next.templateUrl === '/partials/login.html') {
            }
            else {
                event.preventDefault();
                $location.path("/login");
            }
        }
    });
  }]);