
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
- TAPO P125M smartplug


## Qualcomm AI and camera prerequisites

### 1. Install a supported Ubuntu image on the Rubik Pi and enable SSH.
Then update the system and install basic tools
```bash
sudo apt update
sudo apt upgrade -y

sudo apt install -y \
  git \
  python3 \
  python3-pip \
  python3-venv \
  python3-dev \
  build-essential \
  pkg-config \
  cmake \
  v4l-utils \
  gstreamer1.0-tools
```
### 3. Install the Qualcomm AI Runtime SDK.
### 4. Verify the libraries the program references
```bash
QAIRT=/opt/qcom/aistack/qairt/2.45.41.260507

ls "$QAIRT/lib/aarch64-oe-linux-gcc11.2/libQnnTFLiteDelegate.so"
ls "$QAIRT/lib/aarch64-oe-linux-gcc11.2/libQnnHtp.so"
```

### 5. Connect and verify the CSI camera

DO NOT disconnect/connect the csi camera while the rubik pi is powered on

Verify:
```bash
gst-launch-1.0 \
  qtiqmmfsrc name=camsrc camera=0 \
  ! video/x-raw,width=640,height=480 \
  ! fakesink
```
Successful test should look like:
```Setting pipeline to PLAYING```


Ctrl+C to stop


The commands in this repository assume:

```text
QAIRT path: /opt/qcom/aistack/qairt/2.45.41.260507
Hexagon version: v68
Camera source: qtiqmmfsrc name=camsrc camera=0

```

## Installation

- Clone the repository
```bash
cd ~
git clone https://github.com/YOUR_GITHUB_USERNAME/rubik-pi-gesture-projects.git
cd rubik-pi-gesture-projects
```
Each project should have its own python virtual environment


- Set up the onboard LED project
```bash
cd ~/rubik-pi-gesture-projects/hand_gesture_led_ubuntu_py

python3 -m venv .venv-host
source .venv-host/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
- OR set up the smartplug project
```bash
cd ~/rubik-pi-gesture-projects/hand_gesture_lamp_ubuntu_py

python3 -m venv .venv-host
source .venv-host/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Check the required `.tflite` models in the `models/` directory of either the LED or Lamp project.
The projects expect these files:
```
models/palm_detector.tflite
models/hand_landmark_detector.tflite
models/canned_gesture_classifier.tflite
```
Verify them:
```bash
cd ~/rubik-pi-gesture-projects/hand_gesture_lamp_ubuntu_py
ls -lh models/
```
```bash
cd ~/rubik-pi-gesture-projects/hand_gesture_led_ubuntu_py
ls -lh models/
```

## Onboard LED project

| Gesture      | Action        |
| ------------ | ------------- |
| Open palm    | Green LED on  |
| Closed fist  | Green LED off |
| Thumb up     | Red LED on    |
| Thumb down   | Red LED off   |
| Victory sign | Blue LED on   |
| Pointing up  | Blue LED off  |

The program requires root permission because it writes to Rubik Pi LED control files under /sys/class/leds
Run it with: 
```bash
cd ~/rubik-pi-gesture-projects/hand_gesture_led_ubuntu_py

GST_DEBUG=2 sudo -E \
  /home/ubuntu/rubik-pi-gesture-projects/hand_gesture_led_ubuntu_py/.venv-host/bin/python \
  main.py \
  --qairt-path /opt/qcom/aistack/qairt/2.45.41.260507 \
  --hexagon-version v68 \
  --video-gstreamer-source "qtiqmmfsrc name=camsrc camera=0" \
  --video-source-width 1280 \
  --video-source-height 720 \
  2>&1 | tee gesture.log
```
Press Ctrl+C to stop the program

## Tapo Smartplug Project

### Install ChipTool - Prebuild Matter Controller
```bash
sudo apt update
sudo apt install -y snapd avahi-daemon bluez
sudo systemctl enable --now avahi-daemon
sudo snap install chip-tool
```
Test the installation:
```bash
chip-tool
```
Create the storage directory:
```bash
mkdir -p /home/ubuntu/snap/chip-tool/common/storage
```
With a new Tapo P125M, pair it using its Matter setup code:
```bash
chip-tool pairing code-wifi \
  1 \
  "YOUR_WIFI_NAME" \
  "YOUR_WIFI_PASSWORD" \
  YOUR_MATTER_SETUP_CODE \
  --bypass-attestation-verifier true \
  --storage-directory /home/ubuntu/snap/chip-tool/common/storage
```
DO NOT place the Wi-Fi password or Matter code in this git repository

### Test the plug before starting gesture detection:
```bash
chip-tool onoff on 1 1 \
  --storage-directory /home/ubuntu/snap/chip-tool/common/storage
```
```bash
chip-tool onoff on 1 1 \
  --storage-directory /home/ubuntu/snap/chip-tool/common/storage
```
The first 1 is the Matter node ID. The second 1 is the plug endpoint.

## Run the lamp project

This project should run under normal ubuntu user rather than sudo so it can access Matter controller credientials
```bash
cd ~/rubik-pi-gesture-projects/hand_gesture_lamp_ubuntu_py
source .venv-host/bin/activate

GST_DEBUG=2 python main.py \
  --qairt-path /opt/qcom/aistack/qairt/2.45.41.260507 \
  --hexagon-version v68 \
  --video-gstreamer-source "qtiqmmfsrc name=camsrc camera=0" \
  --video-source-width 1280 \
  --video-source-height 720 \
  2>&1 | tee gesture.log
```
Default lamp controls are:
| Gesture     | Action   |
| ----------- | -------- |
| Open palm   | Lamp on  |
| Closed fist | Lamp off |

## Configuration

Gesture assignments can be changed in main.py

For example:
```bash
PLUG_ON_GESTURES = {"Open_Palm"}
PLUG_OFF_GESTURES = {"Closed_Fist"}
```
The matter configuration is located in main.py with:
```bash
matter_plug = MatterPlug(
    node_id=1,
    endpoint_id=1,
    storage_directory="/home/ubuntu/snap/chip-tool/common/storage",
)
```
Change the node and endpoint ids if the plug was commissioned with a different node or endpoint id

# Troubleshooting

### If python points to an old project folder
Delete and recreate the virtual environment
```bash
rm -rf .venv-host
python3 -m venv .venv-host
source .venv-host/bin/activate
python -m pip install -r requirements.txt
```

### If Tapo terminal command works but the program fails
Check that:
- The lamp project is not running with sudo
- matter_plug.py uses /snap/bin/chip-tool
- The same Matter storage directory is used for pairing and control
- The Rubik Pi and P125M are connected to the same local network

### Camera does not start
Check:
- CSI cable is connected correctly
- No other application is using the camera
- GStreamer and Qualcomm camera setup has been completed
- ```qtiqmmfsrc name=camsrc camera=0``` command works independently

## Files not stored in this original directory
The following must be installed or created locally:

Python virtual environments
- QAIRT SDK
- Matter controller credentials and storage
- Matter setup codes
- Wi-Fi credentials
- Runtime logs
- Generated cache files
- Any model files excluded by .gitignore

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
