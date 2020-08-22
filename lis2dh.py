# Create a class "Accelerometer", create one instance per node in cluster
# Based on https://github.com/owainm713/LIS3DH-Python-Module/blob/master/LIS3DH.py

import time
import spidev
import RPi.GPIO as GPIO

class Accelerometer:
  def turnOn(self):
    GPIO.output(self.cs, GPIO.LOW)
  
  def turnOff(self):
    GPIO.output(self.cs, GPIO.HIGH)
  
  def single_register_read(self, register = 0x00):
    rwBit = 0b1  # Read/write bit set to "read"
    msBit = 0b0  # Multi-read bit set to "repeat"
    self.turnOn()
    dataTransfer = self.spi.xfer2([(rwBit << 7) + (msBit << 6) + register] + [0])
    self.turnOff()
    return dataTransfer[1]
  
  def sequential_register_read(self, register = 0x00, numBytes = 1):
    rwBit = 0b1  # Read/write bit set to "read"
    msBit = 0b1  # Multi-read bit set to "auto-increment"
    self.turnOn()
    dataTransfer = self.spi.xfer2([(rwBit<<7) + (msBit<<6) + register] + [0 for x in range(numBytes)])
    self.turnOff()
    return dataTransfer[1:]
  
  def single_register_write(self, register = 0x00, value = 0x0):
    rwBit = 0b0  # Read/write bit set to "write"
    msBit = 0b1  # Multi-read bit set to "auto-increment"
    self.turnOn()
    dataTransfer = self.spi.xfer2([(rwBit<<7) + (msBit<<6) + register, value])
    self.turnOff()
    return
  
  def __init__(self, spi, cs):
    self.cs = cs
    self.spi = spi
    self.cscsv = ',' + str(self.cs) + ','
    GPIO.setup(cs, GPIO.OUT)
    GPIO.output(cs, GPIO.HIGH)
    # Set ctrl_reg4 to +- 8g
    self.single_register_write(0x23, 0x20)
    # Set ctrl_reg1 to 400 Hz, normal power, enabled
    self.single_register_write(0x20, 0x77)