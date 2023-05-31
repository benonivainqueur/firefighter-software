import { me as companion } from "companion";
import * as messaging from "messaging";



const wsUri = "ws://192.168.0.28:8008";
const websocket = new WebSocket(wsUri);



messaging.peerSocket.addEventListener("message", (evt) => {
    console.log("recevied from app : " + evt.data);
    websocket.send(evt.data);
});

function onOpen(evt) {
   console.log("CONNECTED");
   websocket.send("hello");
   websocket.send("hello2")
   websocket.send('hello3')
}

function onClose(evt) {
   console.log("DISCONNECTED");
}

function onMessage(evt) {
   console.log(`MESSAGE: ${evt.data}`);
}

function onError(evt) {
   console.error(`ERROR: ${evt.data}`);
   console.error(`ERROR: ${evt}`);
}

websocket.addEventListener("open", onOpen);
websocket.addEventListener("close", onClose);
websocket.addEventListener("message", onMessage);
websocket.addEventListener("error", onError);

if (!companion.permissions.granted("run_background")) {
  console.warn("We're not allowed to access to run in the background!");
}

const MILLISECONDS_PER_MINUTE = 1000 * 60;

// Tell the Companion to wake after 30 minutes
companion.wakeInterval = 30 * MILLISECONDS_PER_MINUTE;

// Listen for the event
companion.addEventListener("wakeinterval", doThis);

// Event happens if the companion is launched and has been asleep
if (companion.launchReasons.wokenUp) {
  doThis();
}

function doThis() {
  console.log("Wake interval happened!");
}
function sendThis(data) {
    websocket.send(data);
}


