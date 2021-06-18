# SERS TEAM OpenMV

Code for recognizing U, S, and H letters and detecting red, green, and yellow


# Hardware

1. OpenMV M7

## Software 

1. MicroPython


# Principle of working

There's a matrix that consists of 3 blocks of pixels on the x axis and 3 on the y axis. The image signal is, of course, in greyscale with a quite some contrast and if more than 55% of the pixel block is dark then the pixel block is considered dark and when a certain combination of pixel blocks is dark, the OpenMV module sends a combination of high and low signals to the Raspberry Pi, which then sends an interrupt to Arduino and starts ejecting a rescue packet.

