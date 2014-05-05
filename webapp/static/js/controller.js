/* Controllers */

var gamepicksControllers = angular.module('gamepicksControllers', []);

gamepicksControllers.controller('ArticleListCtrl', ['$scope', '$http', '$modal',
    function($scope, $http, $modal) {
        $http.get('/api/latest').success(function(data) {
            $scope.articles = data.res;
        });
        $scope.pick = function() {
            var modalInstance = $modal.open({
                templateUrl:"/static/partial/login.html", 
                controller: PickModalCtrl,
                scope: $scope
            });
        };
    }]
);

gamepicksControllers.controller('ArticleDetailCtrl', ['$scope', '$routeParams', '$http',
    function($scope, $routeParams, $http) {
        $http.get('/api/article?article_id=' + $routeParams.articleId).success(function(data) {
            $scope.article = data.res;
        });
    }]
);

gamepicksControllers.controller('ArticlePreviewCtrl', ['$scope', '$routeParams', '$http',
    function($scope, $routeParams, $http) {
        $http.get('/api/article?article_id=' + $routeParams.articleId).success(function(data) {
            $scope.article = data.res;
        });
    }]
);

var PickModalCtrl = function($scope, $modalInstance) {
    $scope.cancel = function () { 
        $modalInstance.dismiss('close');
    }
};

