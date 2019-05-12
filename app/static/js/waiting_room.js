function xhrOpen(eventType) {
	var xhr = new XMLHttpRequest();

	xhr.open('POST', document.getElementById('data').dataset.post);
	xhr.setRequestHeader('Event-Type', eventType);
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	return xhr;
};

//settings
function saveSettings() {
	var xhr = xhrOpen('change_settings');

	var description = document.getElementById('room_description').value;
	var name = document.getElementById('room_name').value;
	var mapId = document.getElementById('room_map').value;

	console.log(description, name, mapId);

	xhr.send('description='+description+'&name='+name+'&map_id='+mapId)
}

function deleteRoom() {
	var xhr = xhrOpen('delete_room');
	xhr.send();
};

function startGame() {
	var xhr = xhrOpen('start_game');
	xhr.send();
};

var socket = io.connect('http://' + document.domain + ':' + location.port + '/' + document.getElementById('data').dataset.room_id);
socket.on('update', function(msg) {
	switch (msg.event) {
		case 'change_settings':
			var title = document.getElementById('title');
			var description = document.getElementById('description');
			var mapName = document.getElementById('map_name');
			var mapDescription = document.getElementById('map_description');

			title.innerHTML = (msg.name);
			description.innerHTML = ('Описание:<br>' + msg.description.replace(/\n/g, '<br>'));
			mapName.innerHTML = ('Карта:' + msg.map.name);
			mapDescription.innerHTML = ('Описание карты:<br>' + msg.map.description.replace(/\n/g, '<br>'));
			break;

		case 'player_enter_or_leave':
			var players_list = document.getElementById('players_list');
			var xhr = xhrOpen('get_players_list');
			xhr.send()
			xhr.onload = function () {
				players_list.innerHTML = xhr.responseText
			};
			break;

		case 'change_description':
			var description = document.getElementById('description');

			description.innerHTML = ('Description:<br>' + msg.description.replace(/\n/g, '<br>'));
			break;

		case 'delete_room':
			alert('Oups. Room was deleted');
			document.location.href = document.getElementById('data').dataset.delRedirect;
			break;

		case 'start_game':
			document.location.href = document.getElementById('data').dataset.startRedirect;
			break;
	};
});

// var changeNameInput = document.getElementById('room_name');
// changeNameInput.onkeydown = changeName;

// var changeDescriptionInput = document.getElementById('room_description');
// changeDescriptionInput.onkeydown = changeDescription;

// var saveSettingsButton = document.getElementById('save_settings_btn');
// saveSettingsButton.onclick = saveSettings;

var startButton = document.getElementById('start_button');
if (startButton) {
	startButton.onclick = startGame;
}

var deleteRoomButton = document.getElementById('delete_room_button');
if (deleteRoomButton) {
	deleteRoomButton.onclick = deleteRoom;
}

var settingButton = document.getElementById('settings_button');
var roomInfo = document.getElementById('room_info');
var roomSettings = document.getElementById('room_settings');
if (settingButton) {
	settingButton.onclick = function() {
		toggle(roomInfo);
		toggle(roomSettings);
	};
}