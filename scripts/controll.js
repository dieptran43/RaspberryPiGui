window.onload = function(){

    /*Variables*/
    let brightness = document.getElementById('brightness');
    let brightness_text = document.getElementById("brightness_number");
    let bvalue = brightness.value;
    let modal = document.getElementById('alerts');
    let error = document.getElementById('error');
    let message = document.getElementById('message');
    let error_msg = document.getElementById('error_message');
    let message_msg = document.getElementById('message_message');
    let dismiss = document.getElementById('Dismiss');
    let ok = document.getElementById('Ok');
    let cancle = document.getElementById('Cancle');
    let picker = document.getElementById('color');
    let cabinet = document.getElementById("cabinet");
    let bath_tub = document.getElementById("bath_tub");
    let room = document.getElementById("room");

    /*Functions*/
    show_error = function(msg) {
        error_msg.innerHTML = msg;
        error.style.display = 'block';
        modal.style.display = 'block';
    }

    show_message = function(msg) {
        message_msg.innerHTML = msg;
        message.style.display = 'block';
        modal.style.display = 'block';
    }

    /* Connection */
    let connection = new this.WebSocket("ws://127.0.0.1:6969");
    let todo;

    console.log("Connecting to server...")

    connection.onopen = function() {
        console.log("Connection established");
    }

    connection.onclose = function() {
        console.log("Connection closed!");
        show_error('Megszakadt a kapcsolat a szerverrel!');
    }

    connection.onmessage = function(event){
        todo = event.data;
        console.log(todo);
        switch (todo) {
            case 'room':
                show_message('Az ajtó nyitva, a fények égnek 2 percig.<br>Maradjanak égve?');
                break;
        }
    }

    if (bvalue < 10) {
        bvalue = "0" + bvalue;
    }

    brightness_text.innerHTML = bvalue;

    /* Event handlers */
    brightness.addEventListener("input", function() {
        
        let bvalue = brightness.value;
        console.log("EventListener called with value of "+bvalue)
        if (bvalue < 10) {
            bvalue = "0" + bvalue;
        }

        brightness_text.innerHTML = bvalue;
        let data = 'brightness,'+bvalue;
        connection.send(data);
    }, false);

    room.addEventListener('change', function() {
        let room_on = room.checked;
        console.log("EventListener called for '"+lights.id+"' with value '"+room_on+"'");
        let data = 'room,'+room_on;
        connection.send(data);
    }, false);

    bath_tub.addEventListener('change', function() {
        let bath_tub_on = bath_tub.checked;
        console.log("EventListener called for '"+bath_tub.id+"' with value '"+bath_tub_on+"'");
        let data = 'bath_tub,'+bath_tub_on;
        connection.send(data);
    }, false);

    cabinet.addEventListener('change', function() {
        let cabinet_on = cabinet.checked;
        console.log("EventListener called for '"+cabinet.id+"' with value '"+cabinet_on+"'");
        let data = 'cabinet,'+cabinet_on;
        connection.send(data);
    }, false);

    work = function(ansver) {
        console.log('Todo: '+todo+'\tAnsver: '+ansver);
        switch (todo) {
            case 'room':
                room.checked = ansver;
                event = document.createEvent('Event');
                event.initEvent('change', true, true);
                room.dispatchEvent(event);
                break;
            case 'kill':
                connection.send('kill');
                break;
        }
    }

    dismiss.addEventListener('click', function() {
        error_msg.innerHTML = '';
        error.style.display = 'none';
        modal.style.display = 'none';
    }, false);
    
    ok.addEventListener('click', function() {
        message_msg.innerHTML = '';
        message.style.display = 'none';
        modal.style.display = 'none';
        work(true);
    }, false);

    cancle.addEventListener('click', function() {
        message_msg.innerHTML = '';
        message.style.display = 'none';
        modal.style.display = 'none';
        work(false);
    }, false);

    picker.addEventListener('change', function(event){
        picker.value = event.target.value;
        picker.style.backgroundColor = event.target.value;
        console.log('Selected color: '+picker.value);
        connection.send('color,'+event.target.value);
    }, false);

}