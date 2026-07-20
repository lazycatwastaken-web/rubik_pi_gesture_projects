
# Rubik Pi Gesture Projects

Gesture-control projects for the Rubik Pi using a CSI camera.


### hand_gesture_lamp_ubuntu_py

Uses hand gestures to control a Tapo P125M Matter smart plug.

- Open palm: lamp on
- Closed fist: lamp off
- Runs as the normal `ubuntu` user

### hand_gesture_led_ubuntu_py

Uses hand gestures to control the Rubik Pi onboard LEDs.

- Open palm / closed fist: green LED
- Thumb up / thumb down: red LED
- Victory / pointing up: blue LED
- Requires elevated LED-file permissions

#### Hardware Prerequisites

- Rubik Pi running Ubuntu
- Compatible CSI camera
- Heatsink or cooling
- TAPO P125M smartplug (specifically for outlet/lamp control)


### Qualcomm AI and camera prerequisites

1. Install a supported Ubuntu image on the Rubik Pi and enable SSH.
2. Install the Qualcomm AI Runtime SDK.
3. Verify the libraries the program references
```bash
QAIRT=/opt/qcom/aistack/qairt/2.45.41.260507

ls "$QAIRT/lib/aarch64-oe-linux-gcc11.2/libQnnTFLiteDelegate.so"
ls "$QAIRT/lib/aarch64-oe-linux-gcc11.2/libQnnHtp.so"
```
4. Confirm that the QAIRT TFLite Delegate and HTP libraries are available.
5. Install the Python packages from `requirements.txt`.
6. Place the required `.tflite` models in the `models/` directory.
7. Connect the CSI camera and verify that
   `qtiqmmfsrc name=camsrc camera=0` produces frames.
8. Run the application once and confirm that the Qualcomm NPU delegate loads
   without errors.

The commands in this repository assume:

```text
QAIRT path: /opt/qcom/aistack/qairt/2.45.41.260507
Hexagon version: v68
Camera source: qtiqmmfsrc name=camsrc camera=0

```

## Notes

Python virtual environments, credentials, logs, and Matter controller
storage are not included in the repository.


## Attribution

This project is derived from Qualcomm AI Hub Apps'
`mediapipe_hand_gesture_ubuntu_py` sample application.

Original source:
Qualcomm AI Hub Apps, licensed under the BSD 3-Clause License.

The original Qualcomm copyright notices and license have been retained.
This repository contains modifications for controlling the Rubik Pi onboard
LEDs and a Tapo P125M Matter smart plug.

This project is not affiliated with or endorsed by Qualcomm Technologies, Inc.

## Main modifications

- `main.py`: Added gesture-triggered LED and smart-plug control
- `matter_plug.py`: Added Tapo P125M control through Matter `chip-tool`
