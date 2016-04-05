// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
// 'starter.services' is found in services.js
// 'starter.controllers' is found in controllers.js
angular.module('starter', ['ionic','ionic.service.core', 'starter.controllers', 'starter.services', 'ionic.service.push'])

.run(function($ionicPlatform, $ionicPush) {
  $ionicPlatform.ready(function() {
    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if (window.cordova && window.cordova.plugins && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
      cordova.plugins.Keyboard.disableScroll(true);

    }
    if (window.StatusBar) {
      // org.apache.cordova.statusbar required
      StatusBar.styleDefault();
    }
  });

  $ionicPush.register({
      canShowAlert: false, //Can pushes show an alert on your screen?
      canSetBadge: true, //Can pushes update app icon badges?
      canPlaySound: true, //Can notifications play a sound?
      canRunActionsOnWake: true, //Can run actions outside the app,
      onNotification: function(notification) {
        // Handle new push notifications here
        console.log(notification);
        $state.go(payload.$state, {"message" : JSON.stringify(payload.$stateParams)});
        //$state.go('tab.live')
        return true;
      }
    });

})
.run(function($ionicPlatform, $location, $state, $ionicPush) {
  $ionicPlatform.ready(function() {
    $ionicPush.init({
      "debug": false,
      "onNotification": function(notification) {
        var payload = notification.payload;
        console.log(notification, payload);
        $state.go(payload.$state, {"message" : payload.$stateParams});
        //$state.go('tab.live')
      },
      "onRegister": function(data) {
        console.log(data.token);
      }
    });

    $ionicPush.register(function(token) {
      console.log("Device token:",token.token);
    });
  });
})

.config(function($stateProvider, $urlRouterProvider) {

  // Ionic uses AngularUI Router which uses the concept of states
  // Learn more here: https://github.com/angular-ui/ui-router
  // Set up the various states which the app can be in.
  // Each state's controller can be found in controllers.js
  $stateProvider

  // setup an abstract state for the tabs directive
    .state('tab', {
    url: '/tab',
    abstract: true,
    templateUrl: 'templates/tabs.html'
  })

  // Each tab has its own nav history stack:

  .state('tab.episodes', {
    url: '/episodes/:date',
    views: {
      'tab-episodes': {
        templateUrl: 'templates/tab-episodes.html',
        controller: 'EpCtrl'
      }
    }
  })

  .state('tab.events', {
      url: '/events/:message',
      views: {
        'tab-episodes': {
          templateUrl: 'templates/tab-events.html',
          controller: 'EventsCtrl'
        }
      }
    })
    .state('tab.live', {
    url: '/live',
    views: {
      'tab-live': {
        templateUrl: 'templates/tab-live.html',
        controller: 'LiveCtrl'
      }
    }
  })
  .state('tab.account', {
    url: '/account',
    views: {
      'tab-account': {
        templateUrl: 'templates/tab-account.html',
        controller: 'AccountCtrl'
      }
    }
  })

  // if none of the above states are matched, use this as the fallback
  $urlRouterProvider.otherwise('/tab/episodes/');

});
