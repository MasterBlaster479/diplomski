var myModule = angular.module('enterprise', ['ngResource','ngRoute']);


myModule.config(function ($routeProvider, $locationProvider){
    $locationProvider.html5Mode({enabled:true, requireBase:false});
    $routeProvider.
        when("/", {
            templateUrl: "/partials/list.html"
        }).
        when("/new", {
            templateUrl: "/partials/edit.html", controller:"NewCtrl"
        }).
        when("/edit:id", {
            templateUrl: "/partials/edit.html", controller:"EditCtrl"
        }).
        otherwise({redirectTo:"/index.html"});
});
myModule.controller('AppCtrl', function ($scope) {
    $scope.crew = [
        {name:"Picard", description:"Captain"},
        {name:"Riker", description:"Number Oe"},
        {name:"Worf", description:"Security"},
    ]
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