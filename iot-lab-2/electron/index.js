//used to get env variable
require('dotenv').config();
document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65432;
var server_addr = process.env.IP_ADDRESS;   // the IP address of your Raspberry PI

//added for logging purposes
var nodeConsole = require('console');
var myConsole = new nodeConsole.Console(process.stdout, process.stderr);

function client(input){
    const net = require('net');
    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        myConsole.log('connected to server!');
        // send the message
        client.write(`${input}\r\n`);

    });
    myConsole.log(input)
    // get the data from the server
    client.on('data', (data) => {

        if(input == 'update'){
            info = data.toString().split(',');
            document.getElementById('distance').innerHTML = info[0];
            document.getElementById('power').innerHTML = info[1];
            document.getElementById('temperature').innerHTML = info[2];
        }
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });


}

// for detecting which key is been pressed w,a,s,d
function updateKey(e) {

    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        client("up");
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        client("down");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        client("left");
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        client("right");
    }else if (e.keyCode == '69'){
        client('stop');
    }
}

// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
}




setInterval(function(){
    // get image from python server
    client('update');
}, 300);
