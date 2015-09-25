var app = angular.module('trumpApp', []);
app.controller('trumpController',['$scope', '$http',function($scope,$http){
  $scope.getResponse = function() {
    var word = $('input[name=user_input]').val();
      //$http.get('http://whatwouldtrumpsay.elasticbeanstalk.com/api/v0/?q='+word)
      $http.get('http://localhost:5000/api/v0/?q='+word)
        .then( function(response) { $scope.response = response.data; });
        $scope.started = true;
   };
}]);


app.directive('trump', function($http) {
        return {
                restrict: 'AE',
                scope: {},
                templateUrl: 'static/app.html',
                link: function(scope, elem, attrs) {
                        /*scope.start = function() {
                                scope.id = 0;
                                scope.quizOver = false;
                                scope.inProgress = true;
                        };*/

                        scope.reset = function() {
                                scope.inProgress = false;
                                scope.trumpresponse = '';
                        }

                        scope.set = function(q) {
                              scope.trumpresponse = q.answer;
                        }

                        scope.getQuestion = function(word) {
                                //$http.get('http://whatwouldtrumpsay.elasticbeanstalk.com/v0/?q='+word)
                                $http.get('http://localhost:5000/v0/?q='+word)
                                     .then(
                                         function(response) {
                                                 scope.set(response.data);
                                     });

                                     scope.inProgress = true;
                        };

                        scope.reset();
                }
        }
});
