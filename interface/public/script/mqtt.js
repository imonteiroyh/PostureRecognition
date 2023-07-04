
    // Create a client instance
client = new Paho.MQTT.Client('localhost', Number(9001), "clientId");

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({onSuccess:onConnect});


// called when the client connects
function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    console.log("onConnect");
    client.subscribe("posture/classification");
        message = new Paho.MQTT.Message(JSON.stringify({
            name:"yago",
            id:1,
            class: "incorreta"
        }));
    message.destinationName = "posture/classification";
    client.send(message);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
    }
}

// called when a message arrives
function onMessageArrived(message) {
    var data = JSON.parse(message.payloadString);
    var posture = data.class;
    var img = data.image;

    const result = document.querySelector("#result");
    result.innerHTML = posture

    const imgresult = document.querySelector("#img-result");
    imgresult.src = `data:image/png;base64,${imgresult}`

       
}


