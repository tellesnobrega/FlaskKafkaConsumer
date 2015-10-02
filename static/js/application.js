
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var messages_received = [];

    //receive details from server
    socket.on('newmessage', function(msg) {
        console.log("Received message" + msg.message);
        //maintain a list of ten numbers
        if (messages_received.length >= 10){
            messages_received.shift()
        }            
        messages_received.push(msg.message);
        messages_string = '';
        for (var i = 0; i < messages_received.length; i++){
            messages_string = messages_string + '<p>' + messages_received[i].toString() + '</p>';
        }
        $('#log').html(messages_string);
    });

});
