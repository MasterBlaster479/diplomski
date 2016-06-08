angular.module('StockService', ['ngResource'])
.factory('Stock', function($resource, $rootScope){
    /**
     *  Stock Resource factory
     */
    var proxy_dict = {};
    proxy_dict.resource = $resource('/api/stocks/:id',{id: ''},{update: {method: 'PUT'}});
    proxy_dict.stocks = [];
    return proxy_dict;
});