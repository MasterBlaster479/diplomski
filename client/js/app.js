var myModule = angular.module('my_app', ['ngResource','ngRoute', 'ngMessages', 'AuthServices', 'StockService']);

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
        when("/stock-category", {
            templateUrl: "/partials/stock_category.html", controller:"StockCategoryCtrl"
        }).
        when("/stock-category/new", {
            templateUrl: "/partials/stock_category_edit.html", controller:"StockCategoryNewCtrl"
        }).
        when("/stock-category/edit/:id", {
            templateUrl: "/partials/stock_category_edit.html", controller:"StockCategoryEditCtrl"
        }).
        when("/stock-category/remove/:id", {
            templateUrl: "/partials/stock_category.html", controller:"StockCategoryRemoveCtrl"
        }).
        otherwise({redirectTo:'/'})
});

myModule.controller('AppCtrl', function ($scope, $rootScope, $location, Auth) {
    $rootScope.logout = function(){
        Auth.logout();
        $location.path("/login");
      };
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
    $scope.errors = {};
    $scope.login = function() {
        Auth.login($scope.user.login, $scope.user.password)
          .then(function() {
              event.preventDefault();
              $location.path("/");
          }, function(response) {
              angular.forEach(response.data.errors, function(errors, field){
                  // notify form that field is invalid
                  $scope.form[field].$setValidity('server', false);
                  // store the error messages from the server
                  $scope.errors[field] = errors.join(', ');
              });
              $scope.failed = true;
          });
    };
});

myModule.controller('RegisterCtrl', function($scope, $location, Auth) {
    $scope.new_user = {first_name: '',last_name: '', e_mail: '', password: '', login: ''};
    $scope.failed = false;
    $scope.register = function() {
        Auth.register($scope.new_user.first_name, $scope.new_user.last_name, $scope.new_user.e_mail,
         $scope.new_user.password, $scope.new_user.login)
          .then(function() {
              $location.path("/");
          }, function() {
              $scope.failed = true;
          });
    };
});

myModule.controller('StockCtrl', function ($scope, $rootScope, $location, Stock) {
    /*Get All Stock Data*/
    Stock.getStockData().$promise.then(function(data){
        $scope.stocks = Stock.StockData.Stock;
    });

});

myModule.controller('StockNewCtrl', function ($scope, $location, Stock) {
    $scope.stock = {code: '',name: '', category: {}};
    Stock.category_resource.get().$promise.then(function(data){
        $scope.stock_categories = data.StockCategory;
    });
    $scope.resource = Stock.resource;
    $scope.save = function() {
        var s = this.stock;
        this.resource.save({code: s.code, name: s.name, category: s.category.id}, function(response) {
            $location.path("/stock");
        });
    }
});

myModule.controller('StockEditCtrl', function ($scope, $location, $routeParams, Stock) {
    $scope.stock = Stock.StockData.Stock[$routeParams.id];
    $scope.history_lines = _.filter(Stock.StockData.StockHistory, function(sh) {return $scope.stock.history_lines.indexOf(sh.id) > -1 })
    Stock.category_resource.get().$promise.then(function(data){
        $scope.stock_categories = data.StockCategory;
    });
    $scope.resource = Stock.resource;
    $scope.save = function() {
        var s = this.stock;
        this.resource.update({id: s.id}, {code: s.code, name: s.name, category: s.category}, function(response) {
            $location.path("/stock");
        });
    }
    $scope.populate_lines = function() {
        var s = this.stock;
        this.resource.populate_lines({id: s.id}, function(response) {
            $scope.history_lines = response.StockHistory;
        });
    }
});

myModule.controller('StockRemoveCtrl', function ($scope, $location, $routeParams, Stock) {
    Stock.resource.remove({id: $routeParams.id}, function(response) {
            $location.path("/stock");
    });
});

myModule.controller('StockCategoryCtrl', function ($scope, $rootScope, $location, Stock) {
    /*Get All Stock Category Data*/
    Stock.getStockCategoryData().$promise.then(function(data){
        $scope.categories = Stock.StockData.StockCategory;
    });
});

myModule.controller('StockCategoryNewCtrl', function ($scope, $location, Stock) {
    $scope.stock_category = {code: '',name: '', stocks: {}};
    $scope.resource = Stock.category_resource;
    $scope.save = function() {
        var s = this.stock_category;
        this.resource.save({code: s.code, name: s.name}, function(response) {
            $location.path("/stock-category");
        });
    }
});

myModule.controller('StockCategoryEditCtrl', function ($scope, $location, $routeParams, Stock) {
    $scope.stock_category = Stock.StockData.StockCategory[$routeParams.id];
    $scope.stocks = _.filter(Stock.StockData.Stock, function(stock) {return $scope.stock_category.stocks.indexOf(stock.id) > -1 })
    $scope.resource = Stock.category_resource;
    $scope.save = function() {
        var c = this.stock_category;
        this.resource.update({id: c.id}, {code: c.code, name: c.name}, function(response) {
            $location.path("/stock-category");
        });
    }
});

myModule.controller('StockCategoryRemoveCtrl', function ($scope, $location, $routeParams, Stock) {
    Stock.category_resource.remove({id: $routeParams.id}, function(response) {
            $location.path("/stock-category");
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