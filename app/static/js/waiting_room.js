function xhrOpen(eventType) {
	var xhr = new XMLHttpRequest();

	xhr.open('POST', document.getElementById('info').getAttribute('post'), false);
	xhr.setRequestHeader('Event-Type', eventType);
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	return xhr;
};
function changeDescription(event) {
	if (event.keyCode == 13){
		var xhr = xhrOpen('change_description');
		var newDescription = document.getElementById('room_description').value;

		xhr.send("new_description=" + newDescription);	
	};
};
function changeName(event) {
	if (event.keyCode == 13){
		var xhr = xhrOpen('change_name');
		var newName = document.getElementById('room_name').value;

		xhr.send("new_name=" + newName);
	};
};
function startGame() {
	var xhr = xhrOpen('start_game');

	xhr.send();
};

var socket = io.connect('http://' + document.domain + ':' + location.port + '/wrws');
socket.on('update', function(msg) {
	switch (msg.event) {
		case 'change_name':
			var title = document.getElementById('title');
			title.innerHTML = ('Room ' + msg.name);
			break;
		case 'player_enter_or_leave' :
			var players = document.getElementById('players');
			players.innerHTML = ('Players: ' + msg.players);
			break;
		case 'change_description':
			var description = document.getElementById('description');
			description.innerHTML = ('Description: ' + msg.description);
			break;
		case 'start_game':
			document.location.href = document.getElementById('info').getAttribute('redirect');
			break;
	};
});
socket.on('connect', function() {
	socket.emit('player join', {'room_id': document.getElementById('info').getAttribute('room_id')});
});

var changeNameInput = document.getElementById('room_name');
changeNameInput.onkeydown = changeName;

var changeDescriptionInput = document.getElementById('room_description');
changeDescriptionInput.onkeydown = changeDescription;

var startButton = document.getElementById('start_button');
startButton.onclick = startGame;