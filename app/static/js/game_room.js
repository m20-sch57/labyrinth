function xhrOpen(eventType) {
	var xhr = new XMLHttpRequest();

	xhr.open('POST', document.getElementById('info').getAttribute('post'), false);
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

var socket = io.connect('http://' + document.domain + ':' + location.port + '/grws');
socket.on('update', function(msg) {
	switch (msg.event) {
		case 'player_make_turn':
			var xhr = xhrOpen('update');
			xhr.send();

			var log = document.getElementById('log');
			log.innerHTML += ('<p>'+xhr.responseText.substr(1)+'</p>');

			var turnState = document.getElementById('turn_state');
			if (xhr.responseText.substr(0, 1) == 'y') {
				turnState.innerHTML = 'Твой ход';
			} else {
				turnState.innerHTML = 'Подожди';
			};
			break;
	};
});
socket.on('connect', function() {
	socket.emit('player join', {'room_id': document.getElementById('info').getAttribute('room_id')});
});

var turnInput = document.getElementById('input');
turnInput.onkeydown = makeTurn;