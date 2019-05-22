<script type='text/javascript'>
    function xhrOpen(eventType) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', "{{ url_for('waiting_room', room_id=room.id) }}");
        xhr.setRequestHeader('Event-Type', eventType);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        return xhr;
    };

    function xhrGetTemplate(templateName) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', "{{ url_for('get_template', template_name='') }}" + templateName);
        return xhr;
    }

    function saveSettings() {
        var xhr = xhrOpen('change_settings');
        var description = document.getElementById('room_description').value;
        var name = document.getElementById('room_name').value;
        var mapId = document.getElementById('room_map').value;
        xhr.send('description='+description+'&name='+name+'&map_id='+mapId)
    }  

    $(document).ready(function () {
        userBlockTemplateLoader = xhrGetTemplate('_user_block-small.html');
        userBlockTemplateLoader.send();
        userBlockTemplateLoader.onload = function() {
            userBlockTemplate = userBlockTemplateLoader.responseText;
        };

        var socket = io.connect('http://' + document.domain + ':' + location.port + '/' + '{{ room.id }}');
        socket.on('update', function(msg) {
            switch (msg.event) {
                case 'change_settings':
                    $('#roomname').attr('data-saved-value', msg.name).html(msg.name).trigger('change');
                    // $('#roomname').trigger('change');
                    $('#description').html('Описание:<br>' + msg.description.replace(/\n/g, '<br>'));
                    if (msg.map) {
                        $('#map_name').html('Карта:' + msg.map.name);
                        $('#map_description').html('Описание карты:<br>' + msg.map.description.replace(/\n/g, '<br>'));
                    }
                    break;

                case 'player_enter_or_leave':
                    $('#players_list').html(msg.data);
                    break;

                case 'change_description':
                    $('#description').html('Description:<br>' + msg.description.replace(/\n/g, '<br>'));
                    break;

                case 'delete_room':
                    alert('Oups. Room was deleted');
                    document.location.href = "{{ url_for('room_list') }}";
                    break;

                case 'start_game':
                    document.location.href = "{{ url_for('game_room', room_id=room.id) }}";
                    break;
            };
        });
        window.onbeforeunload = function() {
            socket.emit('disconnect_request')
        };
    })

    $('#start_game').click(function(){
        var xhr = xhrOpen('start_game');
        xhr.send();
    })
    $('#exit_room').click(function(){
        window.location = "{{ url_for('room_list') }}"
    })
    $('#delete_aroom').click(function(){
        var xhr = xhrOpen('delete_room');
        xhr.send();
    })


    // var settingButton = document.getElementById('settings_button');
    // var roomInfo = document.getElementById('room_info');
    // var roomSettings = document.getElementById('room_settings');
    // if (settingButton) {
    //     settingButton.onclick = function() {
    //         toggle(roomInfo);
    //         toggle(roomSettings);
    //     };
    // };
</script>