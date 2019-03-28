function xhrOpen(eventType) {
	var xhr = new XMLHttpRequest();

	xhr.open('POST', document.getElementById('data').dataset.post, false);
	xhr.setRequestHeader('Event-Type', eventType);
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	return xhr;
};

function makeTurn(event) {
	if (event.keyCode == 13) {
		var xhr = xhrOpen('turn');
		var turn = document.getElementById('input').value;

		xhr.send('turn=' + turn);
	};
};

function getUpdate() {
	var xhr = xhrOpen('update');
	xhr.send();
	responseData = JSON.parse(xhr.responseText);
	console.log(responseData);

	var log = document.getElementById('log');
	log.innerHTML += ('<p>'+ responseData.msg.join('<br>') +'</p>');

	var turnState = document.getElementById('turn_state');
	if (responseData.your_turn == 'yes') {
		turnState.innerHTML = 'Твой ход';
	} else {
		turnState.innerHTML = 'Подожди';
	};
};

function ready() {
	getUpdate();
	var socket = io.connect('http://' + document.domain + ':' + location.port + '/' + document.getElementById('data').dataset.room_id);
	socket.on('update', function(msg) {
		switch (msg.event) {
			case 'player_make_turn':
				getUpdate();
				break;
		};
	});
	socket.on('connect', function() {
		socket.emit('player join', {'room_id': document.getElementById('data').dataset.room_id});
	});
};
var turnInput = document.getElementById('input');
turnInput.onkeydown = makeTurn;

document.addEventListener("DOMContentLoaded", ready);