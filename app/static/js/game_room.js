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
	console.log(xhr.responseText);
	responseData = JSON.parse(xhr.responseText);
	console.log(responseData);

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
	// 1 - my turn
	// 2 - not my turn
	// 0 - game ended

	if (responseData.game_state == 1) {
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

	} else if (responseData.game_state == 2) {
		removeAllButtons();
		turnState.innerHTML = 'Подожди';
	} else if (responseData.game_state == 0) {
		removeAllButtons();	 
		turnState.innerHTML = 'Игра окончена';
	}
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

 // Bars
  
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

// When the document is loaded 
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
turnInput.onkeydown = makeTurnFromInput;

document.addEventListener("DOMContentLoaded", ready);