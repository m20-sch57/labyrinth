function xhrOpen(eventType) {
	var xhr = new XMLHttpRequest();

	xhr.open('POST', document.getElementById('data').dataset.post, false);
	xhr.setRequestHeader('Event-Type', eventType);
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	return xhr;
};

function makeTurn(turn) {
	var xhr = xhrOpen('turn');
	xhr.send('turn=' + turn);
};

function getUpdate() {
	var xhr = xhrOpen('update');
	xhr.send();
	responseData = JSON.parse(xhr.responseText);

	var log = document.getElementById('log');
	log.innerHTML += ('<p>'+ responseData.msg +'</p>');

	var turnState = document.getElementById('turn_state');
	if (responseData.your_turn == 'yes') {
		turnState.innerHTML = 'Твой ход (' + responseData.ats + ')';
		removeAllButtons();
		responseData.buttons.forEach(function(entry) {
			switch(entry.type) {
				case 'button':
					addButton(entry.turn, entry.image)
					break;
			};
		});

	} else {
		removeAllButtons();
		turnState.innerHTML = 'Подожди';
	};
};

// Interface

// Buttons
function addButton(turn, image) {
	var buttonsBar = document.getElementById('buttons_bar');
	var button = document.createElement('button');
	button.innerHTML = '<img src="' + image + '">';
	function mt() {
		makeTurn(turn);
	};
	button.onclick = mt;
	
	buttonsBar.appendChild(button);
};

function removeAllButtons() {
	var buttonsBar = document.getElementById('buttons_bar');
	while (buttonsBar.firstChild) {
	    buttonsBar.removeChild(buttonsBar.firstChild);
	};
};

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

document.addEventListener("DOMContentLoaded", ready);