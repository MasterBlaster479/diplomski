var myModule = angular.module('my_app', ['ngResource','ngRoute', 'AuthServices', 'StockService']);

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
        when("/stock", {
            templateUrl: "/partials/stock.html", controller:"StockCtrl"
        }).
         when("/stock/new", {
            templateUrl: "/partials/stock_edit.html", controller:"StockNewCtrl"
        }).
         when("/stock/edit/:id", {
            templateUrl: "/partials/stock_edit.html", controller:"StockEditCtrl"
        }).
        when("/stock/remove/:id", {
            templateUrl: "/partials/stock.html", controller:"StockRemoveCtrl"
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
        Auth.login($scope.user.login, $scope.user.password)
          .then(function() {
              event.preventDefault();
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

myModule.controller('StockCtrl', function ($scope, $rootScope, $location, Stock) {
    Stock.stocks = Stock.resource.query(function(){
        $scope.stocks = Stock.stocks;
    });
});

myModule.controller('StockNewCtrl', function ($scope, $location, Stock) {
    $scope.stock = {code: '',name: ''};
    $scope.resource = Stock.resource;
    $scope.save = function() {
        var s = this.stock;
        this.resource.save({code: s.code, name: s.name}, function(response) {
            $location.path("/stock");
        });
    }
});

myModule.controller('StockEditCtrl', function ($scope, $location, $routeParams, Stock) {
    $scope.stock = _.find(Stock.stocks, function(obj){return obj.id == $routeParams.id});
    $scope.resource = Stock.resource;
    $scope.save = function() {
        var s = this.stock;
        this.resource.update({id: s.id}, {code: s.code, name: s.name}, function(response) {
            $location.path("/stock");
        });
    }
});

myModule.controller('StockRemoveCtrl', function ($scope, $location, $routeParams, Stock) {
    Stock.resource.remove({id: $routeParams.id}, function(response) {
            $location.path("/stock");
    });
});

myModule.run(['$rootScope', '$location', 'Auth', 'Stock', function ($rootScope, $location, Auth, Stock) {
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