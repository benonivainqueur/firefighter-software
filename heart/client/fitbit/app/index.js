import { Accelerometer } from "accelerometer";
import { HeartRateSensor } from "heart-rate";
import * as messaging from "messaging";
import { display } from "display";
import * as document from "document";
import { me } from "appbit";

console.log("Hello world!");
console.log("Timeout, before: " + me.appTimeoutEnabled);
me.appTimeoutEnabled = false; // Disable timeout
console.log("Timeout, after: " + me.appTimeoutEnabled);

const accelLabel = document.getElementById("accel-label");
const accelData = document.getElementById("accel-data");
const hrmLabel = document.getElementById("hrm-label");
const hrmData = document.getElementById("hrm-data");
const eventButtonState = false;
const eventButton = document.getElementById("event-button");
const eventButtonText = document.getElementById("event-button-text");
const sensors = [];

if (Accelerometer) {
  const accel = new Accelerometer({ frequency: 1 });
  accel.addEventListener("reading", () => {
    accelData.text = JSON.stringify({
      x: accel.x ? accel.x.toFixed(1) : 0,
      y: accel.y ? accel.y.toFixed(1) : 0,
      z: accel.z ? accel.z.toFixed(1) : 0,
    });
  });
  sensors.push(accel);
  accel.start();
} else {
  accelLabel.style.display = "none";
  accelData.style.display = "none";
}

if (HeartRateSensor) {
  const hrm = new HeartRateSensor({ frequency: 1 });
  hrm.addEventListener("reading", () => {
    hrmData.text = JSON.stringify({
      heartRate: hrm.heartRate ? hrm.heartRate : 0,
    });
    if (eventButtonState) {
      messaging.peerSocket.send(hrm.heartRate ? hrm.heartRate : 0);
    }
    //   console.log(hrmData.text);
  });
  sensors.push(hrm);
  hrm.start();
} else {
  hrmLabel.style.display = "none";
  hrmData.style.display = "none";
}

display.addEventListener("change", () => {
  // Automatically stop all sensors when the screen is off to conserve battery
  display.on
    ? sensors.map((sensor) => sensor.start())
    : sensors.map((sensor) => sensor.start());
});

eventButton.addEventListener("click", (evt) => {
  eventButtonState = !eventButtonState;
  if (eventButtonState) { // action is starting, switch to stop button
    eventButton.style.fill="red";
    eventButtonText.text="STOP";
  } else { // action is over, switch to start button
    eventButton.style.fill="green";
    eventButtonText.text="START";
  }
  messaging.peerSocket.send(eventButtonState?"START":"STOP");
});
