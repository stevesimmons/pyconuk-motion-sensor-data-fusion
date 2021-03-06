# Motion sensors and data fusion - in Python

Presentation slides and code from my PyCon UK 2016 talk on motion sensors and data fusion (3:30pm, 15 September 2016).


## Example 1 - BBC microbit data logger

`microbit-logger.py` is a MicroPython program that sets up the microbit to log accelerometer and compass data. 

The simplest mode of operation (called `'log'`) logs sensor data directly to a host computer connected to its USB port. The function `read_sensors()` reads the motion sensor data and formats it into a comma-separated strings. The microbit command `uart.write(data)` sends these csv strings via a serial interface over USB to the host computer. The host computer can capture this data stream (using the program `usb-receiver.py`) directly into a csv text file, ready for subsequent analysis in Excel or in Python using pandas.

The more fun mode (called `'tx'`) transmits sensor data wirelessly rather than via USB. Now the microbit is free to move around (especially if battery-powered) and capture a much wider range of movements. This mode require a second microbit to be the radio receiver (running in mode called `'rx'`) to  relay the sensor data messages to the host computer connected via USB. This radio mode uses MicroPython's very simple mesh radio protocol: the transmitter does `radio.send(data)` and the receiver `data = radio.receive()`.

Note the while the microbit hardware supports Bluetooth Low Energy (BLE), we unfortunately cannot use BLE to stream sensor data directly to the host computer. BLE is a complex protocol and the current BLE stack does not leave enough free memory to run MicroPython. Instead we use the simpler mesh radio protocol, with the second microbit relaying the sensor data to the host computer. 

To run this example:

1. Use the `mu` editor or `uflash` utility to flash the `microbit-logger.py` code onto the microbit(s).
  
  ```$ uflash microbit-logger.py```
  
  If you have multiple microbits connected, you will need to specify which one to flash:
  
  ```$ uflash microbit-logger.py /media/stephen/MICROBIT```
  
2. Start the microbit(s) and put them into the correct modes: `'log'` if you have one microbit, and `'tx'` and `'rx'` if you have two. 

  Button A cycles through the modes `'idle'`/`'log'`/`'tx'`/`'rx'` and back to `'idle'` again. 
  
  The LEDs show which mode is active: `Image.ARROW_S` for `'log'` (think saving results straight down), `Image.ARROW_E` for `'tx'` (sending data somewhere else), and `Image.HEART` for '`rx`' (a heart beat as data gets relayed). These pulsate in brightness as data is received, giving a clear indication that everything is working ok.
  
  The microbit may display a message that its compass needs to be calibrated, followed by a single dot on the LEDs. Rotate the microbit until all directions. Calibration is complete when the LEDs are lit in a full circle.
   
3. Run `usb-receiver.py` on the host computer to receive the sensor data via USB and print on the console. From here it can be redirected to a file.
  
  ```$ python usb-receiver.py``` 
  
  ```$ python usb-receiver.py > data.csv```

4. Analyse the data by loading it into a spreadsheet like Excel or a Python program. A Jupyter notebook plus pandas makes this easy.

    ```(TODO: Add example Jupyter notebook)```
    
  
## Example 2 - Mobile phone sensor data

(to be added)
