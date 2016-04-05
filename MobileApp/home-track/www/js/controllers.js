angular.module('starter.controllers', ['pubnub.angular.service'])
.controller('EpCtrl', function($scope, PubNub, $stateParams, $state, $ionicViewSwitcher, $ionicNavBarDelegate, $ionicPlatform) {

$ionicNavBarDelegate.showBackButton(false);
console.log($stateParams.date);
var dateStart;
var dateEnd;
if($stateParams.date === undefined || $stateParams.date === ''){
  dateStart =  new Date();
  $scope.date = dateStart;

  dateStart.setHours(0,0,0,0);
  $scope.dayStart = dateStart;

  dateEnd = new Date();
  dateEnd.setHours(23,59,59,999);
  $scope.dayEnd = (dateEnd);
} else {
  dateStart = new Date($stateParams.date);
  $scope.date = dateStart;
  
  dateStart.setHours(0,0,0,0);
  $scope.dayStart = dateStart;

  dateEnd = new Date($stateParams.date);
  dateEnd.setHours(23,59,59,999);
  $scope.dayEnd = (dateEnd);
}

var getIcon = function(reason){
  switch(reason.toUpperCase()) {
    case 'MAN': return 'ion-person-stalker';
    case 'DOG': return 'ion-ios-paw';
    case 'CLATTER': return 'ion-volume-high';
    case 'LOWNOISE': return 'ion-volume-low';
    case 'BANG': return 'ion-alert';
  }
};

$scope.backDay = function(){
  $ionicViewSwitcher.nextDirection('back');
  var testdate = new Date($scope.date.setDate(($scope.date).getDate() + -1));
  $state.go('tab.episodes', {date : testdate});
  //$scope.date = "10/08/1994";
};
$scope.forwardDay = function(){
  $ionicViewSwitcher.nextDirection('forward');
  var testdate = new Date($scope.date.setDate(($scope.date).getDate() + 1));
  console.log(testdate.getTime()/1000.0);
  $state.go('tab.episodes', {date : testdate});
};

$scope.messages = [];
 PubNub.init({
    subscribe_key: 'sub-c-02de9d80-9a93-11e5-9a49-02ee2ddab7fe',
    publish_key: 'pub-c-92b5e647-0c49-49a1-ab2a-4753777f53b9',
});
PubNub.ngSubscribe({ channel: 'HomeTracker' });


 $scope.$on(PubNub.ngMsgEv('episodes'), function(event, payload) {
  $scope.$apply(function() {
    $scope.messages.push(JSON.parse(payload.message));
  });
});

 //7th and 21st of feb  
PubNub.ngHistoryQ({channel:'episodes', limit:500, start: ((($scope.dayStart).getTime()/1000.0)*10000000)-1, end: ((($scope.dayEnd).getTime()/1000.0)*10000000)-1, include_token:true}).then(function(payload) {
    var noiseCount = {};
    console.log(($scope.dayStart).getTime()/1000.0);
    console.log(($scope.dayEnd).getTime()/1000.0);
    console.log("pubstart: " + ((($scope.dayStart).getTime()/1000.0)*10000000));
    console.log("pubend: " + ((($scope.dayEnd).getTime()/1000.0)*10000000));
    payload[0].forEach(function(message) {
      var JsonMessage = JSON.parse(message.message);
      if(JsonMessage.count !== undefined)
      {
        console.log(new Date(JsonMessage.start * 1000));
        JsonMessage.count.forEach(function(noise) {
          noiseCount[noise] = (noiseCount[noise] || 0) + 1;
        });
        var arr = Object.keys(noiseCount).reduce(function(a, b){ return noiseCount[a] > noiseCount[b] ? a : b });
        JsonMessage.icon = getIcon(arr);
        $scope.messages.push(JsonMessage);
        console.log(JsonMessage);
        noiseCount = {};
      }
    });
  });

  PubNub.ngHistoryQ({channel:'snapshots', limit:500, start: ((($scope.dayStart).getTime()/1000.0)*10000000)-1, end: ((($scope.dayEnd).getTime()/1000.0)*10000000)-1, include_token:true}).then(function(payload) {
  //console.log(payload);
    if(payload[0].length > 0)
    {
        message = payload[0][0];
        console.log(message);
        if(message.message.epid !== undefined)
        {
            //console.log(message.message);
            var image = new Image();
            $scope.image = 'data:image/png;base64,' + message.message.picture;
        }
    } else {
      $scope.image = '../www/img/NO_DATA.jpg';
    }
  });
})

.controller('EventsCtrl', function($scope, PubNub, $stateParams, $ionicNavBarDelegate) {
$ionicNavBarDelegate.showBackButton(true);
  $scope.getIcon = function(reason){
    switch(reason.toUpperCase()) {
      case 'MAN': return 'ion-person-stalker';
      case 'DOG': return 'ion-ios-paw';
      case 'CLATTER': return 'ion-volume-high';
      case 'LOWNOISE': return 'ion-volume-low';
      case 'BANG': return 'ion-alert';
    }
  };
  //console.log($routeParams.message);
  $scope.messages = [];
  PubNub.init({
      subscribe_key: 'sub-c-02de9d80-9a93-11e5-9a49-02ee2ddab7fe',
      publish_key: 'pub-c-92b5e647-0c49-49a1-ab2a-4753777f53b9',
  });
  //PubNub.ngSubscribe({ channel: 'HomeTracker' });
  var episode = JSON.parse($stateParams.message);
  var datime = new Date(episode.start*1000);
  datime.setHours(datime.getHours() - 2);
  //console.log(datime);
  datime = datime.getTime();

  $scope.start = episode.start;
  $scope.end = episode.end;
  //console.log((episode.start - (300*60)) * 10000000);
  //console.log(episode.end* 10000000);
  //console.log(new Date(((episode.start - (300*60)))*1000));
  //console.log(new Date(episode.end * 1000));
  
  PubNub.ngHistoryQ({channel:'events',limit:100, include_token:true}).then(function(payload) {
  var noiseCount = {};
  var sep = [];
  //console.log(payload);
    payload[0].forEach(function(eventmess) {
      //console.log(JSON.parse(eventmess.message));
      //console.log("episode" + JSON.parse($routeParams.message).epid)
      var mess = JSON.parse($stateParams.message);
      var jsonmess = JSON.parse(eventmess.message);
      if(jsonmess.epid !== undefined)
      {
        if(jsonmess.epid === JSON.parse($stateParams.message).epid)
        {
        mess.count.forEach(function(noise) {
          //noiseCount[noise] = (noiseCount[noise] || 0) + 1;
          console.log(eventmess);
        });

        //if(!sep[jsonmess.reason]) {
        //  sep[jsonmess.reason] = [];
        //}
        sep.push(jsonmess);
        $scope.sep = sep;
        $scope.noiseCount = noiseCount;
        $scope.messages.push(eventmess);
        noiseCount = {};
      }
    }
    });
  });
  
  PubNub.ngHistoryQ({channel:'snapshots', limit:500, start: ((episode.start - (60)) * 10000000), end: ((episode.end + 60) * 10000000), include_token:true}).then(function(payload) {
    payload[0].forEach(function(message) {
      console.log(message);
      if(message.message.epid !== undefined)
      {
        if(message.message.epid === JSON.parse($stateParams.message).epid)
        {
          //console.log(message.message);
          var image = new Image();
          $scope.image = 'data:image/png;base64,' + message.message.picture;
        }
      }
    });
  });




  $scope.toggleGroup = function(group) {
    if ($scope.isGroupShown(group)) {
      $scope.shownGroup = null;
    } else {
      $scope.shownGroup = group;
    }
  };
  $scope.isGroupShown = function(group) {
    return $scope.shownGroup === group;
  };
  
})

.controller('LiveCtrl', function($scope, $stateParams, Chats) {
  $scope.chat = Chats.get($stateParams.chatId);
})

.controller('AccountCtrl', function($scope) {
  $scope.OnOffToggle = true;
  $scope.toggleOnOff = function(){
    $scope.OnOffToggle = !$scope.OnOffToggle;
  };
  $scope.MotionToggle = true;
  $scope.toggleMotion = function(){
    $scope.MotionToggle = !$scope.MotionToggle;
  };
});
