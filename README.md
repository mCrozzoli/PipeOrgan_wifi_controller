# PipeOrgan_wifi_controller
First version of a wifi pipe organ controller! try it out &lt;3

**Project: Pipe Organ WIFI Controller**

This project allows users to control the opening and closing of a solenoid valve which manages the airflow into a pipe organ. The system is comprised of a Python-based user interface (UI), an ESP32 connected via serial communication, and additional ESP32 devices that receive data through ESP-NOW (WiFi).

**System Overview**

The Python script provides a UI for the user to create a grid representing the solenoid valve states (open/close). Users can input the number of rows and columns for the grid, as well as a tempo value that affects the timing of solenoid valve actions.

Once the user has configured the grid and tempo, the Python script constructs an Open Sound Control (OSC) message containing the grid and tempo data. This message is sent over a serial connection to the first ESP32 device. The first ESP32 parses the incoming OSC message and forwards the parsed data to the other ESP32 devices using the ESP-NOW protocol.

Each receiving ESP32 device processes the incoming data and controls the solenoid valve's state based on the received data. The valve states are managed according to the user-defined grid and tempo values.

**Communication Flow**

Python UI receives user input (grid configuration and tempo).
Python script constructs an OSC message with grid and tempo data.
OSC message is sent over a serial connection to the first ESP32.
First ESP32 parses the OSC message and forwards data to other ESP32 devices using ESP-NOW.
Receiving ESP32 devices control the solenoid valve based on received data (grid configuration and tempo).
User Interaction
Through the UI, users can create a grid representing the solenoid valve states (open/close) and input a tempo value. The grid consists of black and white cells, where black represents an open state and white represents a closed state. Users can toggle cell states by clicking on them. Once the desired grid configuration and tempo are set, the user can click the "Save" button to send the data to the ESP32 devices and control the solenoid valve accordingly.


**Building the System**

To build the pipe organ controller system, you will need the following components:
1.Python installed (preferably version 3.6 or later)
2.Two or more ESP32 microcontrollers
3.Step-up converter
4.Relay Module
5.Solenoid valves for controlling airflow into the pipe organ
6.USB cable for connecting the sending ESP32 to the computer (for serial communication)
7.Jumper wires
8.A 5v for the ESP32 connected to the solenoid (check the valve's specifications)


**Steps to Build the System**

1.Set up the Python environment: Install the required Python libraries for the project. The script requires pyserial, python-osc, and tkinter. You can install these libraries using pip:
2.Flash the ESP32 devices: Upload the provided ESP32 code to each of your ESP32 microcontrollers using the Arduino IDE or a similar tool. Make sure to update the MAC addresses in the "ESP32 connected via Serial" code to match the addresses of your receiving ESP32 devices. Also, update the peerMacA, peerMacB, etc., in the "ESP32 receivers" code to match the addresses of your receiving ESP32 devices.
3.Connect the ESP32 devices: Connect the first ESP32 to your computer using a USB cable. This will allow serial communication between the Python script and the ESP32. Connect the receiving ESP32 devices to the solenoid valve(s) using jumper wires and a breadboard. Make sure to connect the appropriate GPIO pin (as specified in the "ESP32 receivers" code) to the control pin of the solenoid valve. Additionally, connect the power and ground pins of the solenoid valve to a suitable power source.
4.Run the Python script: Execute the provided Python script on your computer. This will open the user interface, allowing you to create a grid, set a tempo, and control the solenoid valve.
5.Configure and control the system: Use the UI to set the desired grid configuration and tempo. Click the "Save" button to send the data to the ESP32 devices and control the solenoid valve accordingly.

Check the txt or PDF for some **Dashed diagrams of how the system is built and communicates**

