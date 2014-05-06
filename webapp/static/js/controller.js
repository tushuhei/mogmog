/* Controllers */

var mogmogControllers = angular.module('mogmogControllers', []);

mogmogControllers.controller('BaseCtrl', ['$scope', 'Facebook',
    function($scope, Facebook) {
        $scope.fbuser = {};
        $scope.$watch(function() {
            return Facebook.isReady();
        }, function(newVal) {
            if (newVal == true) {
                Facebook.getLoginStatus(function(response) {
                    if (response.status == 'connected') {
                        $scope.me(); 
                    }
                });
            }
        });

        $scope.login = function() {
            Facebook.login(function(response) {
                if (response.status == 'connected') {
                    $route.reload();
                }
            });
        };

        $scope.me = function() {
            Facebook.api('/me', function(response) {
                $scope.$apply(function() {
                    $scope.fbuser = response;
                });

            });
        };
    }
]);

mogmogControllers.controller('ArticleListCtrl', ['$scope', '$http', '$modal', '$controller',
    function($scope, $http, $modal, $controller) {
        $controller('BaseCtrl', {$scope: $scope});

        $http.get('/api/latest').success(function(data) {
            $scope.articles = data.res;
        });

        $scope.picked = [];

        $scope.pick = function(article) {
            if (!$scope.fbuser.id) {
                $modal.open({
                    templateUrl:"/static/partial/login.html", 
                    controller: PickModalCtrl,
                    scope: $scope
                });
            }
            if (!article.picked) {
                article.picked = true;
                $scope.picked.push(article);
            }
        };

    }]
);

mogmogControllers.controller('ArticleDetailCtrl', ['$scope', '$routeParams', '$http',
    function($scope, $routeParams, $http) {
        $http.get('/api/article?article_id=' + $routeParams.articleId).success(function(data) {
            $scope.article = data.res;
        });
    }]
);

mogmogControllers.controller('ArticlePreviewCtrl', ['$scope', '$routeParams', '$http',
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

