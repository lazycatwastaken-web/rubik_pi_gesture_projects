
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
