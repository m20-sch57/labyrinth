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

	var log = document.getElementById('log');
	msg = document.createElement('p');
	msg.innerHTML = responseData.msg.join('<br>');
	log.appendChild(msg);

	clearBars();
	responseData.bars.forEach(function(entry) {
		switch(entry.type) {
			case 'common':
				addCommonBar(entry.name, entry.value);
		};
	});

	var turnState = document.getElementById('your-turn');
	if (responseData.your_turn == 'yes') {
		turnState.innerHTML = 'Твой ход';
	} else {
		turnState.innerHTML = 'Подожди';
	};
};

function addCommonBar(name, value) {
	// <span class="resource-name">Бомбы: </span><span class="resource-value">3</span><br>
	resourceName = document.createElement('span');
	resourceName.classsName = 'resource-name';
	resourceName.innerHTML = name + ': ';

	resourceValue = document.createElement('span');
	resourceValue.className = 'resource-value';
	resourceValue.innerHTML = value;
	
	br = document.createElement('br');

	var turnState = document.getElementById('turn-state');
	turnState.appendChild(resourceName);
	turnState.appendChild(resourceValue);
	turnState.appendChild(br);
}

function clearBars() {
	var turnState = document.getElementById('turn-state');
	turnState.innerHTML = '';
}

function ready() {
	getUpdate();
	var socket = io.connect('http://' + document.domain + ':' + location.port + '/grws');
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