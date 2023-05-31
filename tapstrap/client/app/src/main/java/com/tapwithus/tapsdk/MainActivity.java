package com.tapwithus.tapsdk;

import android.content.DialogInterface;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.tapwithus.sdk.TapListener;
import com.tapwithus.sdk.TapSdk;
import com.tapwithus.sdk.TapSdkFactory;
import com.tapwithus.sdk.airmouse.AirMousePacket;
import com.tapwithus.sdk.mode.Point3;
import com.tapwithus.sdk.mode.RawSensorData;
import com.tapwithus.sdk.mode.TapInputMode;
import com.tapwithus.sdk.mouse.MousePacket;
import com.tapwithus.sdk.tap.Tap;

import java.io.OutputStream;
import java.net.Socket;
import java.nio.channels.AsynchronousSocketChannel;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Objects;
import java.util.Queue;
import java.util.Set;

public class MainActivity extends AppCompatActivity {

    private TapSdk sdk;
    private RecyclerViewAdapter adapter;
    private boolean startWithControllerMode = false;
    private String lastConnectedTapAddress = "";

    private int imuCounter;
    private int devCounter;

    private Socket sock;
    private OutputStream outStream;
    private Queue<String> msgQueue = new LinkedList<>();
    private Queue<String> logQueue = new LinkedList<>();
    private AsynchronousSocketChannel client;
    private Thread socketThread;

    public double lastX = 0;
    public double lastY = 0;
    public double lastZ = 0;
    public Point3[] lastPoints;
    public String lastGyro = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        imuCounter = 0;
        devCounter = 0;
        log("onCreate");

        sdk = TapSdkFactory.getDefault(this);
        sdk.enableDebug();
        if (!startWithControllerMode) {
            sdk.setDefaultMode(TapInputMode.text(), true);
        }
        sdk.registerTapListener(tapListener);
        if (sdk.isConnectionInProgress()) {
            log("A Tap is connecting");
        }
        socketThread = new Thread(new Runnable() {
            public void run() {
                while (true) {
                    if (Objects.isNull(sock)) {
                        try {
                            sock = new Socket("192.168.0.6", 8888);
                            outStream = sock.getOutputStream();
                            logQueue.offer("Created socket successfully");
                        } catch (Exception ex) {
                            logQueue.offer("Issue with socket init");
                            log("Issue with socket init");
                            throw new RuntimeException(ex.fillInStackTrace());
                        }
                    } else if (sock.isConnected()) {
                        while (sock.isConnected()) {
                            String nextMsg = msgQueue.poll();
                            if (!Objects.isNull(nextMsg)) {
                                try {
                                    outStream.write(nextMsg.getBytes(StandardCharsets.UTF_8));
//                                    logQueue.offer("sent: " + nextMsg);
//                                log("sent: " + nextMsg);
                                } catch (Exception ex) {
                                    logQueue.offer("Issue with sending msg");
                                    log("Issue with sending msg");
                                    throw new RuntimeException(ex.fillInStackTrace());
                                }
                            }
                        }
                    } else {
                        logQueue.offer("Something's up..?");
                    }
                }
            }
        });
        socketThread.start();


        initRecyclerView();

        Button button = findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
//                sdk.setMouseNotification("D7:A9:E0:8C:17:6E");
//                String tapIdentifier = "D7:A9:E0:8C:17:6E";
//                sdk.writeName(tapIdentifier, "YanivWithCase");

//                sdk.restartBluetooth();
//                sdk.refreshBond(lastConnectedTapAddress);

                if (sdk.isTapIgnored(lastConnectedTapAddress)) {
                    sdk.unignoreTap(lastConnectedTapAddress);
                } else {
                    sdk.ignoreTap(lastConnectedTapAddress);
                }
            }
        });
    }

    private TapListItemOnClickListener itemOnClickListener = new TapListItemOnClickListener() {
        @Override
        public void onClick(TapListItem item) {
            final String tapIdentifier = item.tapIdentifier;
//            askModeDialog(new DialogInterface.OnClickListener() {
//                @Override
//                public void onClick(DialogInterface dialog, int which) {
//                    // do something like...
//                    log("Switching to TEXT mode");
//                    sdk.startMode(tapIdentifier, TapSdk.MODE_TEXT);
//                }
//            },
//                    new DialogInterface.OnClickListener() {
//                        @Override
//                        public void onClick(DialogInterface dialog, int which) {
//                            // do something like...
//                            log("Switching to CONTROLLER mode with MOUSEHID");
//                            sdk.setMouseHIDEnabledInRawMode(tapIdentifier, true);
//                            sdk.startMode(tapIdentifier, TapSdk.MODE_CONTROLLER);
//                        }
//                    },
//
//                    new DialogInterface.OnClickListener() {
//                        @Override
//                        public void onClick(DialogInterface dialog, int which) {
//                            // do something like...
//                            log("Switching to CONTROLLER mode without MOUSEHID");
//                            sdk.setMouseHIDEnabledInRawMode(tapIdentifier, false);
//                            sdk.startMode(tapIdentifier, TapSdk.MODE_CONTROLLER);
//                        }
//                    }
//            );
//


            sdk.vibrate(item.tapIdentifier, new int[]{500, 100, 500});
            askModeDialog(item.tapIdentifier);


//            if (item.isInControllerMode) {
//                log("Switching to TEXT mode");
//                sdk.startMode(item.tapIdentifier, TapSdk.MODE_TEXT);
//            } else {
//                log("Switching to CONTROLLER mode");
//                sdk.setMouseHIDEnabledInRawMode(item.tapIdentifier, true);
//                sdk.startMode(item.tapIdentifier, TapSdk.MODE_CONTROLLER);
//            }
        }
    };

    private void askModeDialog(final String tapIdentifier) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Change TAP Mode");

        String[] options = {"Text Mode", "Controller", "Controller with Mouse HID", "Raw Sensor", "Controller with Full HID"};
        builder.setItems(options, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                switch (which) {
                    // Commented out all the switches bc it would sometimes switch by accident
                    case 0: // TextMode
                        log("Attempted switching to TEXT mode");
//                        sdk.startTextMode(tapIdentifier);
//                        sdk.startMode(tapIdentifier, TapSdk.MODE_TEXT);
                        break;

                    case 1: // Controller Mode With Mouse HID
                        log("Attempted switching to CONTROLLER mode without MOUSEHID");
//                        sdk.setMouseHIDEnabledInRawMode(tapIdentifier, true);
//                        sdk.startMode(tapIdentifier, TapSdk.MODE_CONTROLLER_WITH_MOUSEHID);
//                        sdk.startControllerMode(tapIdentifier);
                        break;
                    case 2: // Controller Mode Without Mouse HID
                        log("Attempted switching to CONTROLLER mode with MOUSEHID");
//                        sdk.setMouseHIDEnabledInRawMode(tapIdentifier, false);
//                        sdk.startMode(tapIdentifier, TapSdk.MODE_CONTROLLER);

//                        sdk.startControllerWithMouseHIDMode(tapIdentifier);
                        break;
                    case 3:
                        log("Switching to RAW SENSOR MODE");
                        sdk.startRawSensorMode(tapIdentifier, (byte) 0, (byte) 0, (byte) 0);
                        break;
                    case 4:
                        log("Attempted switch to CONTROLLER mode with FULLHID");
//                        sdk.startControllerWithFullHIDMode(tapIdentifier);
                }
            }
        });

        builder.setNegativeButton("Cancel", null);
        AlertDialog dialog = builder.create();
        dialog.show();

    }

    private void askModeDialog(DialogInterface.OnClickListener textModeListener, DialogInterface.OnClickListener controllerWithMouseHIDListener, DialogInterface.OnClickListener controllerWithoutMouseHIDListener) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Change TAP Mode");
//        builder.setMessage("Would you like to continue learning how to use Android alerts?");
        // add the buttons
        if (textModeListener != null) {
            builder.setNeutralButton("Text", textModeListener);
        }
        if (controllerWithMouseHIDListener != null) {
            builder.setNeutralButton("Con w/", controllerWithMouseHIDListener);
        }
        if (controllerWithoutMouseHIDListener != null) {
            builder.setNeutralButton("Con w/o", controllerWithoutMouseHIDListener);
        }
        builder.setNegativeButton("Cancel", null);

        // create and show the alert dialog
        AlertDialog dialog = builder.create();
        dialog.show();

    }

    @Override
    protected void onResume() {
        super.onResume();

        log("onResume");

        Set<String> connectedTaps = sdk.getConnectedTaps();
        List<TapListItem> listItems = new ArrayList<>();
        for (String tapIdentifier : connectedTaps) {
            TapListItem tapListItem = new TapListItem(tapIdentifier, itemOnClickListener);
//            tapListItem.isInControllerMode = sdk.isInMode(tapIdentifier, TapSdk.MODE_CONTROLLER);
            listItems.add(tapListItem);
        }
        adapter.updateList(listItems);

        sdk.resume();
    }

    @Override
    protected void onPause() {
        super.onPause();

        log("onPause");
        sdk.pause();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        log("onDestroy");
        sdk.unregisterTapListener(tapListener);
    }


    @Override
    public void onBackPressed() {
        new AlertDialog.Builder(this)
                .setMessage("Are you sure you want to exit?")
                .setCancelable(false)
                .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        sdk.close();
                        int pid = android.os.Process.myPid();
                        android.os.Process.killProcess(pid);
                    }
                })
                .setNegativeButton("No", null)
                .show();
    }

    private void initRecyclerView() {
        RecyclerView recyclerView = findViewById(R.id.recyclerView);
        recyclerView.setHasFixedSize(true);

        RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(this);
        recyclerView.setLayoutManager(layoutManager);

        List<TapListItem> listItems = new ArrayList<>();

        adapter = new RecyclerViewAdapter(listItems);
        recyclerView.addItemDecoration(new DividerItemDecoration(this, LinearLayoutManager.VERTICAL));
        recyclerView.setAdapter(adapter);
    }

    private TapListener tapListener = new TapListener() {

        @Override
        public void onBluetoothTurnedOn() {
            log("Bluetooth turned ON");
        }

        @Override
        public void onBluetoothTurnedOff() {
            log("Bluetooth turned OFF");
        }

        @Override
        public void onTapStartConnecting(@NonNull String tapIdentifier) {
            log("Tap started connecting - " + tapIdentifier);
        }

        @Override
        public void onTapConnected(@NonNull String tapIdentifier) {
            log("TAP connected " + tapIdentifier);
            Tap tap = sdk.getCachedTap(tapIdentifier);
            if (tap == null) {
                log("Unable to get cached Tap");
                return;
            }

            lastConnectedTapAddress = tapIdentifier;
            log(tap.toString());

            adapter.removeItem(tapIdentifier);

            TapListItem newItem = new TapListItem(tapIdentifier, itemOnClickListener);
            newItem.tapName = tap.getName();
            newItem.tapFwVer = tap.getFwVer();
//            newItem.isInControllerMode = sdk.isInMode(tapIdentifier, TapSdk.MODE_CONTROLLER);
            adapter.addItem(newItem);
        }

        @Override
        public void onTapDisconnected(@NonNull String tapIdentifier) {
            log("TAP disconnected " + tapIdentifier);
            adapter.removeItem(tapIdentifier);
        }

        @Override
        public void onTapResumed(@NonNull String tapIdentifier) {
            log("TAP resumed " + tapIdentifier);
            Tap tap = sdk.getCachedTap(tapIdentifier);
            if (tap == null) {
                log("Unable to get cached Tap");
                return;
            }

            log(tap.toString());
            adapter.updateFwVer(tapIdentifier, tap.getFwVer());
        }

        @Override
        public void onTapChanged(@NonNull String tapIdentifier) {
            log("TAP changed " + tapIdentifier);
            Tap tap = sdk.getCachedTap(tapIdentifier);
            if (tap == null) {
                log("Unable to get cached Tap");
                return;
            }

            log("TAP changed " + tap);
            adapter.updateFwVer(tapIdentifier, tap.getFwVer());
        }

//        @Override
//        public void onControllerModeStarted(@NonNull String tapIdentifier) {
//            log("Controller mode started " + tapIdentifier);
//            adapter.onControllerModeStarted(tapIdentifier);
//        }
//
//        @Override
//        public void onTextModeStarted(@NonNull String tapIdentifier) {
//            log("Text mode started " + tapIdentifier);
//            adapter.onTextModeStarted(tapIdentifier);
//        }

        @Override
        public void onTapInputReceived(@NonNull String tapIdentifier, int data, int repeatData) {
            adapter.updateTapInput(tapIdentifier, data, repeatData);
            log("TapInputReceived - " + tapIdentifier + ", " + data + ", repeatData = " + repeatData);
        }

        @Override
        public void onTapShiftSwitchReceived(@NonNull String tapIdentifier, int data) {
            log("TapSwitchShiftReceived - " + tapIdentifier + ", " + data);
            adapter.updateTapSwitchShift(tapIdentifier, data);
        }

        @Override
        public void onMouseInputReceived(@NonNull String tapIdentifier, @NonNull MousePacket data) {
//            log(tapIdentifier + " mouse input received " + data.dx.getInt() + " " + data.dy.getInt() + " " + data.dt.getUnsignedLong() + " " + data.proximity.getInt());
        }

        @Override
        public void onAirMouseInputReceived(@NonNull String tapIdentifier, @NonNull AirMousePacket data) {
            log(tapIdentifier + " air mouse input received " + data.gesture.getInt());
        }

        @Override
        public void onRawSensorInputReceived(@NonNull String tapIdentifier, @NonNull RawSensorData rsData) {
            while (logQueue.size() > 0) {
                log("FROM SOCKETTHREAD: " + logQueue.poll());
            }
            //RawSensorData Object has a timestamp, dataType and an array points(x,y,z).
            if (rsData.dataType == RawSensorData.DataType.Device) {
//                if (lastPoints == null) {
//                    log("hand: " + rsData.getPoint(0).magnitude());
//                }
//                else {
//                    double magSum = 0;
//                    for (int i =0; i<5; i++) {
//                        Point3 lastFinger = lastPoints[i];
//                        Point3 currFinger = rsData.points[i];
//                        Point3 fingerDiff = new Point3(
//                                lastFinger.x - currFinger.x,
//                                lastFinger.y - currFinger.y,
//                                lastFinger.z - currFinger.z
//                        );
//                        magSum += fingerDiff.magnitude();
//                    }
//                    log(String.format("handD: %.3f", magSum));
//                }
//                lastPoints = rsData.points;

//                Point3 thumb = rsData.getPoint(RawSensorData.iDEV_THUMB);
//                if (thumb != null) {
//                    log("thumb: " + new Point3(
//                            lastX-thumb.x,
//                            lastY-thumb.y,
//                            lastZ-thumb.z
//                    ).magnitude());
//                    lastX = thumb.x;
//                    lastY = thumb.y;
//                    lastZ = thumb.z;
//                }

                // Fingers accelerometer.
                // Each point in array represents the accelerometer value of a finger (thumb, index, middle, ring, pinky).
                Point3 thumb = rsData.points[RawSensorData.iDEV_THUMB];
                Point3 index = rsData.points[RawSensorData.iDEV_INDEX];
                Point3 middle = rsData.points[RawSensorData.iDEV_MIDDLE];
                Point3 ring = rsData.points[RawSensorData.iDEV_RING];
                Point3 pinky = rsData.points[RawSensorData.iDEV_PINKY];
                if ((thumb != null) && (index != null) && (middle != null)
                        && (ring != null) && (pinky != null)) {
                    long messageTimestamp = System.currentTimeMillis();
                    String handData = messageTimestamp + "|("+thumb+","+index+","+middle+","+ring+","+pinky+","+lastGyro+")\n";
                    msgQueue.offer(handData);
//                    log("handMag: "+(thumb.magnitude() + index.magnitude() + middle.magnitude() + ring.magnitude() + pinky.magnitude()));

                }
                // Etc... use indexes: RawSensorData.iDEV_THUMB, RawSensorData.iDEV_INDEX, RawSensorData.iDEV_MIDDLE, RawSensorData.iDEV_RING, RawSensorData.iDEV_PINKY
            } else if (rsData.dataType == RawSensorData.DataType.IMU) {
                // Refers to an additional accelerometer on the Thumb sensor and a Gyro (placed on the thumb unit as well).
                Point3 gyro = rsData.getPoint(RawSensorData.iIMU_GYRO);
                if (gyro != null) {
                    double x = gyro.x;
                    double y = gyro.y;
                    double z = gyro.z;
                    String gyroSample = "("+x+","+y+","+z+")";
                    lastGyro = gyroSample;
                    String gyroLog = "hand gyro: " + gyroSample;
                    log(gyroLog);
                    log(String.valueOf(Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2) + Math.pow(z, 2))));
                    logQueue.offer(gyroLog);
                }
                // Etc... use indexes: RawSensorData.iIMU_GYRO, RawSensorData.iIMU_ACCELEROMETER
            }
            // -------------------------------------------------
            // -- Please refer readme.md for more information --
            // -------------------------------------------------
        }

        @Override
        public void onTapChangedState(@NonNull String tapIdentifier, int state) {
            log(tapIdentifier + " changed state: " + state);
        }

        @Override
        public void onError(@NonNull String tapIdentifier, int code, @NonNull String description) {
            log("Error - " + tapIdentifier + " - " + code + " - " + description);
        }
    };

    private void log(String message) {
        Log.e(this.getClass().getSimpleName(), message);
    }
}
