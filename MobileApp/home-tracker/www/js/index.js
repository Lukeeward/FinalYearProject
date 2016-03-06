var hometracker = angular.module('HomeTracker', [
  'ngRoute',
  'HomeTrackControllers'
]);
hometracker.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/episodes', {
        templateUrl: 'episodes.html',
        controller: 'EpListCtrl'
      }).
      when('/events/:message', {
        templateUrl: 'events.html',
        controller: 'EpisodeCtrl'
      }).
      otherwise({
        redirectTo: '/episodes'
      });
  }]);