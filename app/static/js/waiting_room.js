var changeNameInput = document.getElementById('room_name');
function changeDescription(event) {
	if (event.keyCode == 13){
		var xhr = new XMLHttpRequest();
		var newDescription = document.getElementById('room_description');

		xhr.open('POST', document.getElementById('info').getAttribute('post'), false);
		xhr.setRequestHeader('Event-Type', 'change_description');
		xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		xhr.send("new_description=" + newDescription.value);	
	};
};
function changeName(event) {
	if (event.keyCode == 13){
		var xhr = new XMLHttpRequest();
		var newName = document.getElementById('room_name');

		xhr.open('POST', document.getElementById('info').getAttribute('post'), false);
		xhr.setRequestHeader('Event-Type', 'change_name');
		xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		xhr.send("new_name=" + newName.value);
	};
};

var socket = io.connect('http://' + document.domain + ':' + location.port + '/wrws');
socket.on('update', function(msg) {
	switch (msg.event) {
		case 'player_enter_or_leave' :
			var players = document.getElementById('players');
			players.innerHTML = ('Players: ' + msg.players);
			break;
		case 'change_name':
			var title = document.getElementById('title');
			title.innerHTML = ('Room ' + msg.name);
			break;
		case 'change_description':
			var description = document.getElementById('description');
			description.innerHTML = ('Description: ' + msg.description)
	};
});
socket.on('connect', function() {
	socket.emit('player join', {'room_id': document.getElementById('info').getAttribute('room_id')});
});

var changeNameInput = document.getElementById('room_name');
changeNameInput.onkeydown = changeName;

var changeDescriptionInput = document.getElementById('room_description');
changeDescriptionInput.onkeydown = changeDescription