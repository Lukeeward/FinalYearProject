"use strict"
var trackControllers = angular.module('HomeTrackControllers', ['pubnub.angular.service','ngRoute' ]);
trackControllers.controller('EpListCtrl', function($scope, PubNub, $http){
	console.log("test");
$scope.messages = [];
 PubNub.init({
		subscribe_key: 'sub-c-02de9d80-9a93-11e5-9a49-02ee2ddab7fe',
		publish_key: 'pub-c-92b5e647-0c49-49a1-ab2a-4753777f53b9',
});
PubNub.ngSubscribe({ channel: 'HomeTracker' });


 $scope.$on(PubNub.ngMsgEv('episodes'), function(event, payload) {
	$scope.$apply(function() {
		$scope.messages.push(JSON.parse(payload.message))
	});
});
PubNub.ngHistoryQ({channel:'episodes',limit:500}).then(function(payload) {
	  var noiseCount = {};
	  payload[0].forEach(function(message) {
	  	if(message.count != undefined)
	  	{
			message.count.forEach(function(noise) {
				noiseCount[noise] = (noiseCount[noise] || 0) + 1;
			});
		    $scope.messages.push(message);
			noiseCount = {};
		}
	  });
	});
});

trackControllers.controller('EpisodeCtrl',function($scope, PubNub, $http, $routeParams){
	//console.log($routeParams.message);
	$scope.messages = [];
	PubNub.init({
			subscribe_key: 'sub-c-02de9d80-9a93-11e5-9a49-02ee2ddab7fe',
			publish_key: 'pub-c-92b5e647-0c49-49a1-ab2a-4753777f53b9',
	});
	//PubNub.ngSubscribe({ channel: 'HomeTracker' });
	var episode = JSON.parse($routeParams.message);
	var datime = new Date(episode.start*1000);
	datime.setHours(datime.getHours() - 2);
	//console.log(datime);
	datime = datime.getTime();
	//console.log((episode.start - (300*60)) * 10000000);
	//console.log(episode.end* 10000000);
	//console.log(new Date(((episode.start - (300*60)))*1000));
	//console.log(new Date(episode.end * 1000));
	
	PubNub.ngHistoryQ({channel:'events',limit:500, include_token:true}).then(function(payload) {
	var noiseCount = {};
	var sep = {};
	//console.log(payload);
	  payload[0].forEach(function(eventmess) {
	  	//console.log(JSON.parse(eventmess.message));
	  	//console.log("episode" + JSON.parse($routeParams.message).epid)
	  	var mess = JSON.parse($routeParams.message);
	  	var jsonmess = JSON.parse(eventmess.message);
	  	if(jsonmess.epid != undefined)
	  	{
	  		if(jsonmess.epid == JSON.parse($routeParams.message).epid)
	  		{
				mess.count.forEach(function(noise) {
					noiseCount[noise] = (noiseCount[noise] || 0) + 1;
					console.log(eventmess);
				});

				if(!sep[jsonmess.reason]) sep[jsonmess.reason] = [];
				sep[jsonmess.reason].push(jsonmess);
				$scope.sep = sep;
				$scope.noiseCount = noiseCount;
				$scope.messages.push(eventmess);
				noiseCount = {};
			}
		}
	  });
	});
	
	PubNub.ngHistoryQ({channel:'snapshots',limit:500, start: ((episode.start - (60)) * 10000000), end: ((episode.end + 60) * 10000000), include_token:true}).then(function(payload) {
	var noiseCount = {};
	//console.log(payload);
		payload[0].forEach(function(message) {
			console.log(message);
			if(message.message.epid != undefined)
			{
				if(message.message.epid == JSON.parse($routeParams.message).epid)
				{
					//console.log(message.message);
					var image = new Image();
					$scope.image = 'data:image/png;base64,' + message.message.picture;
					document.body.appendChild(image);
					noiseCount = {};
				}
			}
	  });
	});
	
	
});