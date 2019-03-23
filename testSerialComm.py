import math
import serial
import time

ser = serial.Serial()
ser.port = '/dev/cu.usbserial-00000000'
ser.timeout = 0.1  # Reading Timeout is 10 ms
ser.baudrate = 115200
sendFrequency = 100
maxTrials = 5
counter = 0
ser.open()

# Generate dummy sine wave 
while True:
    time.sleep(1 / sendFrequency)
    counter += 1 / sendFrequency
    # if counter >= 2 * math.pi:
    #    counter = 0
    voltage = math.sin(counter) * 12 + 12
    sample = math.cos(counter)
    # capVolt,time,sample
    string = 'capVolt,%.2f,time,%.2f,sample,%.2f\r\n' % (voltage, counter, sample)
    print(string)
    ser.write(string.encode())