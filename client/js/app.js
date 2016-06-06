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
         when("/register", {
            templateUrl: "/partials/register.html", controller:"RegisterCtrl"
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
    $scope.user = {login: '', password: ''};
    $scope.failed = false;
    $scope.login = function() {
        debugger;
        Auth.login($scope.user.login, $scope.user.password)
          .then(function() {
              $location.path("/");
          }, function() {
              $scope.failed = true;
          });
    };
});

myModule.controller('RegisterCtrl', function($scope, $location, Auth) {
    $scope.new_user = {first_name: '',last_name: '', e_mail: '', password: '', login: ''};
    $scope.failed = false;
    $scope.register = function() {
        Auth.register($scope.new_user.first_name, $scope.new_user.last_name, $scope.new_user.e_mail, $scope.new_user.password, $scope.new_user.login)
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
            if (next.templateUrl === '/partials/login.html' || next.templateUrl === '/partials/register.html') {
            }
            else {
                event.preventDefault();
                $location.path("/login");
            }
        }
    });
  }]);