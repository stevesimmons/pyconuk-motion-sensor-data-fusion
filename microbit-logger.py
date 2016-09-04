"""
Motion sensor data logger for BBC micro:bits.

This is sample code from Stephen Simmons' PyCon UK 2016 talk 
"Where am? What am I doing? Motion Sensor Data Fusion with Python".

With one micro:bit: 
  - stream sensor data as csv strings to host computer via USB [mode='log']
    Format is: "Time,AccX,AccY,AccZ,MagX,MagY,MagZ,Heading,Gesture\n"

With two micro:bits:
  - #1 streams sensor data as csv strings using microbit.radio.send() [mode='tx']
  - #2 relays data from microbit.radio.receive() to host computer via USB [mode='rx']

This code runs all three modes, switching between them by pressing Button A.
The accompanying script usb-receiver.py can be used on the host computer to receive USB data.

Stephen Simmons    https://github.com/stevesimmons/pyconuk-motion-sensor-data-fusion
"""

from microbit import *
import radio

header = "Time,AccX,AccY,AccZ,MagX,MagY,MagZ,Heading,Gesture\n"

def read_sensors():
    "Sensor data as a comma-separated string with a newline" 
    t = running_time()    
    (ax, ay, az) = accelerometer.get_values()
    cx = compass.get_x()
    cy = compass.get_y()
    cz = compass.get_z()
    g = accelerometer.current_gesture()
    h = compass.heading()
    msg = '%d,%d,%d,%d,%d,%d,%d,%d,%s\n' % (t,ax,ay,az,cx,cy,cz,h,g)
    return msg

MODES = ['idle', 'log', 'tx', 'rx']     # Modes in order. 
    
CONFIGS = {  
    # mode:   image            src_func        dest_func    delay
    'idle': ( None,            lambda: None,   None,        50 ),
    'log' : ( Image.ARROW_S,   read_sensors,   uart.write,  30 ),
    'tx'  : ( Image.ARROW_E,   read_sensors,   radio.send,  30),
    'rx'  : ( Image.HEART,     radio.receive,  uart.write,  10 ),
}

def switch_modes(mode):
    """Switch hardware to next mode idle/log/tx/rx, 
    returning tuple (new_mode, image, src_func, dest_func, delay)"""
    # Get the new mode and its hardware settings
    if mode is None:
        new_mode = 'idle'
    else:
        new_mode = MODES[(MODES.index(mode) + 1) % len(MODES)]
    image, src_func, dest_func, delay = CONFIGS[new_mode]
    
    # Reconfigure the hardware for the new mode
    if src_func == radio.receive or dest_func == radio.send:
        radio.config(length=100)    # Max 100 chars. See API docs for setting address, power, channel, etc.
        radio.on()
    else:
        radio.off()
    if dest_func == uart.write:
        uart.init(115200)
    if image:
        display.on()
        display.show(image)
    else:
        display.off()

    return new_mode, image, src_func, dest_func, delay

def pulse_image(image, ctr, steps=10):
    "Display image pulsing brightness as ctr increments"
    if image is None:
        display.clear()
    else:
        brightness = float(ctr % steps)/float(steps-1)
        display.show(image * brightness)

def event_loop():
    "Start in 'idle' mode then run event loop"
    mode = None
    while True:
        # Initialize or switch to next mode
        if mode is None or button_a.is_pressed():
            mode, image, get_data, send_data, delay = switch_modes(mode)
            ctr = 0
            sleep(1000)  # In case the button is held down
        
        # Get data from sensors or radio, then sent to USB or via radio to another micro:bit
        data = get_data()
        if data:
            if ctr == 0:
                send_data(header)
            send_data(data)
            ctr += 1
            pulse_image(image, ctr)
        sleep(delay)

event_loop()