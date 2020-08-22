# Controlling a cluster of LIS2DH accelerometers over SPI
# Avoiding Adafruit libraries if possible, for speed reasons
# https://github.com/owainm713/LIS3DH-Python-Module/blob/master/LIS3DH.py

import time
import spidev
import RPi.GPIO as GPIO
import datetime
import lis2dh

GPIO.setmode(GPIO.BCM)
g = 9.806
def twos_complement(lsbmsb):
  lsb = lsbmsb[0]
  msb = lsbmsb[1]
  signBit = (msb & 0b10000000) >> 7
  msb &= 0x7F  # Strip off sign bit
  if signBit:
    x = (msb << 8) + lsb
    x ^= 0x7FFF
    x = -1 - x
  else:
    x = (msb << 8) + lsb
  x = x>>6  # Remove left justification of data
  return x


# Open SPI #1 with CS0_1 as chip select, and keep it open indefinitely, I guess
spi = spidev.SpiDev()
spi.open(1,0)

# Configure SPI speed
spi.max_speed_hz = 4000000 # 10 MHz fastest specified in LIS2DH datasheet

# Create instances of the accelerometer class for each chip select pin
chips = [16]
accels = []
for chip in chips:
  accels += [lis2dh.Accelerometer(spi, chip)]

# Read each chip's acceleration into a log file, to be decoded later
with open('raw.csv', 'a') as file:
  while True:
    file.write('\n' + str(datetime.datetime.now().timestamp()))
    for accel in accels:
      blah = accel.sequential_register_read(0x28, 6)  # This will be a six-element array, e.g. [244, 192, 0, 64, 79, 128]
      file.write(',' + str(accel.cs) + ',' + str(blah))