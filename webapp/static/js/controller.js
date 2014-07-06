/* Controllers */

var mogmogControllers = angular.module('mogmogControllers', []);

mogmogControllers.controller('BaseCtrl', ['$scope', '$http', 'Facebook',
    function($scope, $http, Facebook) {
        $scope.fbuser = {};
        $scope.picked = [];
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
                    location.href = "/";
                }
            });
        };

        $scope.me = function() {
            Facebook.api('/me', function(response) {
                $scope.$apply(function() {
                    $scope.fbuser = response;
                    $http({
                        url: '/api/pick',
                        method: 'GET',
                        params: {
                            "user_id": $scope.fbuser.id
                        }
                    }).success(function(data) {
                        $scope.picked = data.res;
                    });
                });
            });
        };
    }
]);

mogmogControllers.controller('ArticleListCtrl', ['$scope', '$http', '$modal', '$controller',
    function($scope, $http, $modal, $controller) {
        $controller('BaseCtrl', {$scope: $scope});
        $scope.page = "latest";

        $http({
            url: '/api/latest',
            method: 'GET',
        }).success(function(data) {
            $scope.articles = data.res;
        });

        $scope.pick = function(article) {
            // 未ログインならばログイン画面を表示する
            if (!$scope.fbuser.id) {
                $modal.open({
                    templateUrl:"/static/partial/login.html", 
                    controller: PickModalCtrl,
                    scope: $scope
                });
            }
            if ($scope.picked.indexOf(article.id) == -1) {
                $http({
                    url: '/api/pick',
                    method: 'POST',
                    params: {
                        'article_id': article.id,
                        'user_id': $scope.fbuser.id,
                        'hide': 0
                    },
                }).success(function(data) {
                    $scope.picked.push(article.id);
                    if ($scope.fbuser.id) article.user_ids.push($scope.fbuser.id);
                });
            } else {
                $http({
                    url: '/api/pick',
                    method: 'POST',
                    params: {
                        'article_id': article.id,
                        'user_id': $scope.fbuser.id,
                        'hide': 1
                    },
                }).success(function(data) {
                    $scope.picked.splice($scope.picked.indexOf(article.id), 1);
                    if ($scope.fbuser.id) article.user_ids.splice(article.user_ids.indexOf($scope.fbuser.id), 1);
                });
            }
        };
    }]
);

mogmogControllers.controller('ArticlePickCtrl', ['$scope', '$http', '$controller',
    function($scope, $http, $controller) {
        $controller('BaseCtrl', {$scope: $scope});
        $scope.page = "pick";
        $scope.$watch(function() {
            return $scope.picked;
        }, function() {
            $http({
                url: '/api/article',
                method: 'GET',
                params: {
                    'article_ids': $scope.picked.join(",")
                }
            }).success(function(data) {
                $scope.articles = data.res;
            });
        });
    }]
);


mogmogControllers.controller('ArticleDetailCtrl', ['$scope', '$routeParams', '$http', '$controller',
    function($scope, $routeParams, $http, $controller) {
        $controller('BaseCtrl', {$scope: $scope});
        $http({
            url: '/api/article',
            method: 'GET',
            params: {
                'article_ids': $routeParams.articleId
            }
        }).success(function(data) {
            $scope.article = data.res[0];
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

