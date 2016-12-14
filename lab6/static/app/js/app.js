/**
 * Created by ivan on 30.10.16.
 */
'use strict';

// Declare app level module which depends on views, and components
var lab6App = angular.module('lab6App', [
    'ngRoute',
    'ngSanitize',
    'ngResource',
    'rssScroller'
]);

/* Config */
lab6App.config(
    ['$routeProvider', function($routeProvider){
        $routeProvider
            .when('/index', {
                templateUrl: 'index.html',
                controller: 'index'
            })
            .otherwise({redirectTo: '/'});
    }]);

angular.module('rssScroller', [])

    .controller('RssCtrl', [
        '$scope',
        'rssScrollerService',
        function($scope, rssScrollerService) {
            $scope.tapes = [];
            $scope.currentTape = null;
            $scope.records = [];
            $scope.page = 0;
            $scope.size = 3;
            $scope.newTapeUrl = 'https://habrahabr.ru/rss/';

            function init() {
                function reloadPage() {
                    rssScrollerService.getRecords({
                        tape: $scope.currentTape,
                        page: $scope.page,
                        size: $scope.size
                    }, function (resp) {
                        $scope.records = resp.records;
                        $scope.pagination = resp.pagination;
                        $scope.paginationCollection = [];
                        var _page = 0;
                        for(var i = 0; i < $scope.pagination.total; i+=$scope.size)
                            $scope.paginationCollection.push({number: _page++});
                    })
                }

                rssScrollerService.getTapes({}, function (tapes) {
                    $scope.tapes = tapes;
                    if(tapes.length > 0) {
                        $scope.currentTape = $scope.tapes[0]['_id']['$oid'];
                        reloadPage();
                    }
                }, function () {

                });

                $scope.setPage = function (newPage) {
                    $scope.page = newPage;
                    reloadPage();
                };

                $scope.addTape = function () {
                    if($scope['newTapeUrl'])
                        rssScrollerService.addTape({'url': $scope['newTapeUrl']}, function (tapes) {
                            $scope.tapes = tapes;
                        }, function () {

                        })
                };

                $scope.reloadTape = function () {
                    rssScrollerService.reloadTape({
                        tape: $scope.currentTape
                    }, function () {
                        reloadPage();
                    })
                };

                $scope.setTape = function (id) {
                    $scope.currentTape = id;
                    reloadPage();
                }
            }

            init();

        }])
    .factory('rssScrollerService', ['$resource',
        function ($resource) {

            return $resource('/', {}, {
                getTapes: {
                    method: 'GET',
                    url: '/get-tapes',
                    isArray: true
                },
                getRecords: {
                    method: 'GET',
                    url: '/get-records?tape=:tape&page=:page&size=:size'
                },
                addTape: {
                    method: 'POST',
                    url: '/add-tape',
                    isArray: true
                },
                reloadTape: {
                    method: 'GET',
                    url: '/reload-tape?tape=:tape'
                }
            });
        }]);