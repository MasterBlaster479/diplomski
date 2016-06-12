angular.module('StockService', ['ngResource'])
.factory('Stock', function($resource, $rootScope){
    /**
     *  Stock Resource factory
     */
    var proxy_dict = {};
    proxy_dict.resource = $resource('/api/stocks/:id',{id: ''},{update: {method: 'PUT'}});
    proxy_dict.category_resource = $resource('/api/stock_categories/:id',{id: ''},{update: {method: 'PUT'}});
    proxy_dict.StockData = {};
    proxy_dict.StockData.Stock = {};
    proxy_dict.StockData.StockCategory = {};
    proxy_dict.getStockData = function(){
         return proxy_dict.resource.get(function(response) {
                proxy_dict.StockData.Stock = response.Stock;
                if (response.StockCategory){
                    proxy_dict.StockData.StockCategory = response.StockCategory;
                }
         });
    };
    return proxy_dict;
});