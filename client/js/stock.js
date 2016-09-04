angular.module('StockService', ['ngResource'])
.factory('Stock', function($resource, $rootScope){
    /**
     *  Stock Resource factory
     */
    var proxy_dict = {};
    proxy_dict.resource = $resource('/api/stocks/:id/:verb',{id: '', verb:''},
                                    {
                                        update: {method: 'PUT'},
                                        populate_lines: {method: 'GET', params: {verb:'populate_lines'}}
                                    });
    proxy_dict.category_resource = $resource('/api/stock_categories/:id',{id: ''},{update: {method: 'PUT'}});
    proxy_dict.user_resource = $resource('/api/users/:id/:verb',{id: '', verb:''},
                                        {
                                            update: {method: 'PUT'},
                                            stock_portfolio: {method: 'GET', params: {verb:'stock_portfolio'}}
                                        });
    proxy_dict.transaction_resource = $resource('/api/stock_transactions/:id',{id: ''},{update: {method: 'PUT'}});
    proxy_dict.market_resource = $resource('/api/stock_market');
    proxy_dict.StockData = {};
    proxy_dict.StockData.Stock = {};
    proxy_dict.StockData.StockCategory = {};
    proxy_dict.StockData.StockHistory = {};
    proxy_dict.getStockData = function(kwargs){
         return proxy_dict.resource.get(kwargs, function(response) {
                angular.merge(proxy_dict.StockData.Stock, response.Stock);
                if (response.StockCategory){
                    angular.merge(proxy_dict.StockData.StockCategory, response.StockCategory);
                }
                if (response.StockHistory){
                    angular.merge(proxy_dict.StockData.StockHistory, response.StockHistory);
                }
         });
    };
    proxy_dict.getStockCategoryData = function(){
         return proxy_dict.category_resource.get(function(response) {
                angular.merge(proxy_dict.StockData.StockCategory, response.StockCategory);
                if (response.Stock){
                    angular.merge(proxy_dict.StockData.Stock, response.Stock);
                }
         });
    };
    proxy_dict.getNewStockData = function(kwargs){
         return proxy_dict.resource.get(kwargs, function(response) {
                proxy_dict.StockData.Stock = response.Stock;
                proxy_dict.StockData.StockCategory = response.StockCategory;
                if (response.StockHistory){
                    proxy_dict.StockData.StockHistory = response.StockHistory;
                }
         });
    };
    return proxy_dict;
});