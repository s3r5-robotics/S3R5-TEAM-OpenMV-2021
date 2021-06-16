import math

import pyb
import sensor
import time
from pyb import LED


def count_vertical_lines():
    global times
    black = False
    for x in range(blob.y(), blob.y() + blob.h()):
        if img.get_pixel(blob.cx(), x) < 110:
            if not black:
                times += 1

            black = True
        else:
            black = False


def count_horizontal_lines():
    global times
    times = 0
    black = False
    for x in range(blob.y(), blob.y() + blob.h()):
        if x > (((blob.y() + blob.h()) / 10) * 9):
            if img.get_pixel(blob.cx(), x) < 110:
                if not black:
                    times += 1

                black = True
            else:
                black = False


def calculate_distance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def turn_everything_off():
    blue_led.off();
    green_led.off();
    red_led.off();

    event_pin.low()
    pin1.low()
    pin2.low()
    pin3.low()


def s_detected():
    print("S")
    blue_led.on();
    green_led.off();
    red_led.off();

    event_pin.high()
    pin1.high()
    pin2.low()
    pin3.low()


def h_detected():
    print("H")
    blue_led.off();
    green_led.off();
    red_led.on();

    event_pin.high()
    pin1.high()
    pin2.high()
    pin3.low()


def u_detected():
    print("U")
    blue_led.off();
    green_led.on();
    red_led.off();

    event_pin.high()
    pin1.low()
    pin2.high()
    pin3.low()


def y_detected():
    print("Y")
    blue_led.off();
    green_led.off();
    red_led.off();

    event_pin.high()
    pin1.low()
    pin2.low()
    pin3.high()


def g_detected():
    print("G")
    blue_led.off();
    green_led.off();
    red_led.off();

    event_pin.high()
    pin1.high()
    pin2.low()
    pin3.high()


def r_detected():
    print("R")
    blue_led.off();
    green_led.off();
    red_led.off();

    event_pin.high()
    pin1.low()
    pin2.high()
    pin3.high()


sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(30)
sensor.set_vflip(True)
sensor.set_windowing([0, 90, 320, 150])
clock = time.clock()
threshold = (110, 255)
thresholds = [(30, 100, 15, 96, 15, 95),
              (35, 60, -80, -40, -30, 70),
              (50, 100, -10, 10, 40, 80)]

thresholdsGS = [(30, 100, 15, 127, 15, 127),
                (30, 100, -64, -8, -32, 32),
                (0, 15, 0, 40, -80, -20)]

black = False
blobDetected = False
colorMode = False
times = 0

s_times_detected = 0
u_times_detected = 0
h_times_detected = 0

red_led = LED(1)
green_led = LED(2)
blue_led = LED(3)
event_pin = pyb.Pin("P6", pyb.Pin.OUT_PP)
pin1 = pyb.Pin("P7", pyb.Pin.OUT_PP)
pin2 = pyb.Pin("P8", pyb.Pin.OUT_PP)
pin3 = pyb.Pin("P9", pyb.Pin.OUT_PP)

event_pin.low()
pin1.low()
pin2.low()
pin3.low()

sensor.set_windowing([0, 0, 240, 240])

while (True):
    if not colorMode:
        sensor.set_pixformat(sensor.GRAYSCALE)
        img = sensor.snapshot()
        img.lens_corr(2.7, 1.0)
        img.replace(vflip=True);
        img.binary([threshold])
        blobDetected = False
        for blob in img.find_blobs(thresholdsGS, pixels_threshold=430, area_threshold=500):
            blobDetected = True

            width_ = blob.w()
            height_ = blob.h()

            if blob.perimeter() > 750 or (height_ > (3 * width_)):
                break

            if width_ > 110:
                img.rotation_corr(0.0, 0.0, -90.0, 0.0, 0.1)

                for blob in img.find_blobs(thresholds, pixels_threshold=430, area_threshold=500):
                    blobDetected = True

                    count_vertical_lines()

                    if times == 3:

                        s_detected()

                    elif times == 1:

                        count_horizontal_lines()

                        if times == 1:
                            u_detected()
                        else:
                            h_detected()

                    else:
                        # Nothing detected
                        turn_everything_off()

                    times = 0
                    img.draw_rectangle(blob.rect(), color=0)
                    img.draw_cross(blob.cx(), blob.cy(), color=122)

            else:
                count_vertical_lines()

                if times == 3:

                    s_detected()

                elif times == 1:

                    count_horizontal_lines()

                    if times == 1:
                        u_detected()
                    else:
                        h_detected()

                else:
                    # Nothing detected - False alarm
                    turn_everything_off()

                times = 0
                img.draw_rectangle(blob.rect(), color=0)
                img.draw_cross(blob.cx(), blob.cy(), color=122)
    elif colorMode:
        sensor.set_pixformat(sensor.RGB565)
        img = sensor.snapshot()
        for blob in img.find_blobs([thresholds[0]], pixels_threshold=200, area_treshold=200, merge=True):
            r_detected()

        for blob in img.find_blobs([thresholds[1]], pixels_threshold=200, area_treshold=200, merge=True):
            g_detected()

        for blob in img.find_blobs([thresholds[2]], pixels_threshold=200, area_treshold=200, merge=True):
            y_detected()

    if not blobDetected:
        # Nothing detected
        turn_everything_off()

    colorMode = not colorMode
