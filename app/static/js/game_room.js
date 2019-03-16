function xhrOpen(eventType) {
	var xhr = new XMLHttpRequest();

	xhr.open('POST', document.getElementById('data').dataset.post, false);
	xhr.setRequestHeader('Event-Type', eventType);
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	return xhr;
};

function makeTurnFromInput(event) {
	if (event.keyCode == 13) {
		var xhr = xhrOpen('turn');
		var turn = document.getElementById('input').value;

		xhr.send('turn=' + turn);
	};
}

function makeTurn(turn) {
	var xhr = xhrOpen('turn');
	xhr.send('turn=' + turn);
};

function getUpdate() {
	var xhr = xhrOpen('update');
	xhr.send();
	responseData = JSON.parse(xhr.responseText);

	var log = document.getElementById('log');
	log.innerHTML += ('<p>'+ responseData.msg.join('<br>') +'</p>');

	var turnState = document.getElementById('turn_state');
	if (responseData.your_turn == 'yes') {
		turnState.innerHTML = 'Твой ход';
		removeAllButtons();
		responseData.buttons.forEach(function(entry) {
			switch(entry.type) {
				case 'button':
					addCommonButton(entry.turns[0], entry.image);
					break;
				case 'lbutton':
					addListButton(entry.turns, entry.image, entry.turn_images);
					break;
				case 'dbutton':
					addDirectionButton(entry.turns, entry.image, entry.turn_images);
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
function addCommonButton(turn, image) {
	var button = document.createElement('div');

	button.className = 'common-turn-button'
	button.innerHTML = '<img src="' + image + '">';
	function mt() {
		makeTurn(turn);
	};
	button.onclick = mt;

	var buttonsBar = document.getElementById('buttons_bar');	
	buttonsBar.appendChild(button);
};

function addListButton(turns, image, turn_images) {
	var buttonsBar = document.getElementById('buttons_bar');

	// var buttonContainer document.createElement('div');
	var button = document.createElement('div');
	var buttonImage = document.createElement('img');
	var turnsContainer = document.createElement('div');
	var buttonContainer = document.createElement('div');

	button.className = 'list-game-button';
	turnsContainer.className = 'list-turns-container';
	buttonContainer.className = 'list-button-container';

	buttonImage.setAttribute('src', image);
	button.appendChild(buttonImage);

	buttonContainer.appendChild(button);
	buttonContainer.appendChild(turnsContainer);

	for (var i = 0; i < turns.length; i++) {
		var buttonTurn = document.createElement('div');

		buttonTurn.className = 'list-turn-button';

		var buttonTurnImage = document.createElement('img');
		buttonTurnImage.setAttribute('src', turn_images[i]);

		function mtg(k) {
			function mt() {
				makeTurn(turns[k])
			}
			return mt
		};
		buttonTurn.onclick = mtg(i);

		buttonTurn.appendChild(buttonTurnImage);
		turnsContainer.appendChild(buttonTurn);
	}
	buttonsBar.appendChild(buttonContainer);
};

function addDirectionButton() {
	var buttonsBar = document.getElementById('buttonsBar')
}

function removeAllButtons() {
	var buttonsBar = document.getElementById('buttons_bar');
	while (buttonsBar.firstChild) {
	    buttonsBar.removeChild(buttonsBar.firstChild);
	};
};


// When the document is loaded 

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
turnInput.onkeydown = makeTurnFromInput;

document.addEventListener("DOMContentLoaded", ready);