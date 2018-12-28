var changeNameInput = document.getElementById('room_name');
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
			players.innerHTML = ('<p>' + msg.players + '</p>');
			break;
		case 'change_name':
			var title = document.getElementById('title');
			title.innerHTML = ('Room ' + msg.room_name);
			break;
	};
});
socket.on('connect', function() {
	socket.emit('player join', {'room_id': document.getElementById('info').getAttribute('room_id')});
});

var changeNameInput = document.getElementById('room_name');
changeNameInput.onkeydown = changeName;