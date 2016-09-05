"""
Motion sensor data logger for BBC micro:bits.

This is sample code from Stephen Simmons' PyCon UK 2016 talk
"Where am? What am I doing? Motion Sensor Data Fusion with Python".

With one micro:bit:
  - stream sensor data as csv strings to host computer via USB [mode='log']
    Format is: "Time,AccX,AccY,AccZ,MagX,MagY,MagZ,Heading,Gesture\n"

With two micro:bits:
  - #1 streams sensor data as csv strings using microbit.radio.send()
    [mode='tx']
  - #2 relays data from microbit.radio.receive() to host computer
    via USB [mode='relay']

This code runs all three modes, switching between them by pressing Button A.
The accompanying script usb-receiver.py can be used on the host computer to
receive USB data.

Stephen Simmons - 5 Sep 2016
https://github.com/stevesimmons/pyconuk-motion-sensor-data-fusion
"""

from microbit import *
import radio

# =================================================================
# Read sensors as csv strings

CSV_HEADER = "Time,AccX,AccY,AccZ,MagX,MagY,MagZ,Heading,Gesture\n"

def read_sensors():
    "Sensor data as a comma-separated string with a newline"
    t = running_time()
    (ax, ay, az) = accelerometer.get_values()
    cx = compass.get_x()
    cy = compass.get_y()
    cz = compass.get_z()
    g = accelerometer.current_gesture()
    h = compass.heading()
    msg = '%d,%d,%d,%d,%d,%d,%d,%d,%s\n' % (t, ax, ay, az, cx, cy, cz, h, g)
    return msg

# =================================================================
# Define operating modes

MODE_ORDER = ['idle', 'relay', 'log', 'tx']     # Modes in order
MODE_CONFIG = {
    # mode:   image            get_func        send_func          delay
    'idle':  (None,            lambda: None,   lambda data: None, 50),
    'relay': (Image.HEART,     radio.receive,  uart.write,         5),
    'log':   (Image.ARROW_S,   read_sensors,   uart.write,        10),
    'tx':    (Image.ARROW_E,   read_sensors,   radio.send,        30),
    }

def event_loop():
    "Start in 'idle' mode then run event loop"
    mode = None
    while True:
        # Initialize or switch to next mode
        if mode is None or button_a.is_pressed():
            mode, image, get_func, send_func, delay = switch_modes(mode)
            ctr = 0
            sleep(1000)  # In case the button is held down

        # Get data from sensors or radio, then send via USB or radio
        data = get_func()
        if data:
            if ctr == 0:
                send_func(CSV_HEADER)
            send_func(data)
            ctr += 1
            pulse_image(image, ctr)
        sleep(delay)


def switch_modes(mode):
    """Switch hardware to next mode idle/log/tx/rx, returning
    tuple (new_mode, image, get_data_func, send_data_func, delay)
    """
    # Get the new mode and its hardware settings
    if mode is None:
        new_mode = 'idle'
    else:
        new_mode = MODE_ORDER[(MODE_ORDER.index(mode) + 1) % len(MODE_ORDER)]
    image, get_func, send_func, delay = MODE_CONFIG[new_mode]

    # Reconfigure the hardware for the new mode
    # See API docs for setting radio address, power, channel, etc.
    if get_func == radio.receive or send_func == radio.send:
        radio.config(length=100)    # Max 100 chars.
        radio.on()
    else:
        radio.off()
    if send_func == uart.write:
        uart.init(115200)
    if image:
        display.on()
        display.show(image)
    else:
        display.off()
    return new_mode, image, get_func, send_func, delay


def pulse_image(image, ctr, steps=10):
    "Display image pulsing brightness as ctr increments"
    if image is None:
        display.clear()
    else:
        brightness = float(ctr % steps)/float(steps-1)
        display.show(image * brightness)

# =================================================================
# Run the event loop forever
event_loop()
