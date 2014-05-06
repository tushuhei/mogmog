/* App Module */

var mogmogApp = angular.module('mogmogApp', [
        'ngRoute',
        'mogmogControllers',
        'ui.bootstrap',
        'facebook'
        ]);

mogmogApp.config(['FacebookProvider', 
    function(FacebookProvider) {
        FacebookProvider.init('706563022740412');
    }
]);

mogmogApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
        when('/articles', {
            templateUrl: '/static/partial/article-list.html',
            controller: 'ArticleListCtrl'
        }).
        when('/pick', {
            templateUrl: '/static/partial/article-list.html',
            controller: 'ArticlePickCtrl'
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
