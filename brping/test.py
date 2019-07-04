import serial
import time

s = serial.Serial("/dev/ttyUSB0", 115200)

while True:
    s.write(bytearray(b'BR\x0e\x00)\n\x00\x00\x01\x00\x01\x00\x05\x00P\x00\xe8\x03\xc8\x00\x01\x00\xe0\x02'))
    s.reset_input_buffer()

    while s.in_waiting < 214:
        pass
