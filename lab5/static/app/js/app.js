/**
 * Created by ivan on 30.10.16.
 */
'use strict';

// Declare app level module which depends on views, and components
var lab5App = angular.module('lab5App', [
    'ngRoute',
    'ngSanitize',
    'ngResource',
    'guessWho'
]);

/* Config */
lab5App.config(
    ['$routeProvider', function($routeProvider){
        $routeProvider
            .when('/index', {
                templateUrl: 'index.html',
                controller: 'index'
            })
            .otherwise({redirectTo: '/'});
    }]);

angular.module('guessWho', [])

    .controller('GuessWhoCtrl', [
        '$scope',
        'GuessWhoService',
        function($scope, GuessWhoService) {

            function init() {
                $scope.state = 'step-1';

                $scope.toState1 = function () {
                    $scope.state = 'step-1';
                    $scope.level = 'middle';
                };

                $scope.toState2 = function () {
                    $scope.state = 'step-2';
                };

                $scope.toGame = function () {
                    GuessWhoService.setLevel({value: $scope.level}, function (data) {
                        $scope.images = data.images;
                        $scope.var = data.var;
                        $scope.correctAnswer = data['correct_answer'];
                        $scope.state = 'game'
                    }, function () {
                        $scope.state = 'step-1';
                    });
                }

                $scope.sendResult = function () {

                    if($scope.correctAnswer == $scope.name) {
                        alert('Правильный ответ!');
                        $scope.state = 'step-1';
                    } else {
                        alert('Неправильный ответ!');
                    }
                }
            }

            init();

        }])
    .factory('GuessWhoService', ['$resource',
        function ($resource) {

            return $resource('/', {}, {
                setLevel: {
                    method: 'GET',
                    url: '/set-level?value=:value'
                }
            });
        }]);