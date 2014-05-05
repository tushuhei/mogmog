/* App Module */

var gamepicksApp = angular.module('gamepicksApp', [
        'ngRoute',
        'gamepicksControllers',
        'ui.bootstrap'
        ]);

gamepicksApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
        when('/articles', {
            templateUrl: '/static/partial/article-list.html',
            controller: 'ArticleListCtrl'
        }).
        when('/articles/:articleId', {
            templateUrl: '/static/partial/article-detail.html',
            controller: 'ArticleDetailCtrl'
        }).
        when('/preview/:articleId', {
            templateUrl: '/static/partial/article-preview.html',
            controller: 'ArticlePreviewCtrl'
        }).
        otherwise({
            redirectTo: '/articles'
        });
    }
]);
