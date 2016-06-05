#!/usr/bin/python

import time, sys
import zmq
import smbus

port_lcd = sys.argv[1]
port_hub = sys.argv[2]

# ===========================================================================
# BME280 Class
# ===========================================================================

class BME280 :
  bus = None

  # Operating Modes
  __BME280_SLEEP           = 0
  __BME280_FORCED          = 1
  __BME280_NORMAL          = 3

  __BME280_CONTROL           = 0xF4  # Control measurement
  __BME280_CONTROL_HUM       = 0xF2  # Control humidity
  __BME280_TEMPDATA          = 0xFA  # Temperature
  __BME280_PRESSURE_DATA     = 0xF7  # Pressure
  __BME280_HUMIDITY_DATA     = 0xFD  # Humidity
  __BME280_STATUS            = 0xF3  # Status
  __BME280_DATA_REG          = 0xF7  # Start of data registers (support shadowing)


  # Private Fields
  _t_fine = 0
  _calibration_t = []
  _calibration_p = []
  _calibration_h = []

  # Constructor
  def __init__(self, address=0x77, mode=1, debug=False):
    self.i2c_device = smbus.SMBus(1)
    self.addr = address

    if self.i2c_device == None or self.addr == None:
        print('Error initializing device.')
        return -1

    self.debug = debug
    # Make sure the specified mode is in the appropriate range
    if (mode not in [0, 1, 3]):
      if (self.debug):
        print("Invalid Mode: Using FORCED by default")
      self.mode = self.__BME280_FORCED
    else:
      self.mode = mode
    # Read the calibration data
    self.readCalibrationData()

  def readCalibrationData(self):
    "Reads the calibration data from the IC"
    cal_data_a = self._read_bytes(0x88, 24)
    cal_data_b = self._read_bytes(0xA1, 1)
    cal_data_c = self._read_bytes(0xE1, 7)
    raw_data = cal_data_a + cal_data_b + cal_data_c
    self._calibration_t = []
    self._calibration_p = []
    self._calibration_h = []
    self._calibration_t.append((raw_data[1] << 8) | raw_data[0])
    self._calibration_t.append((raw_data[3] << 8) | raw_data[2])
    self._calibration_t.append((raw_data[5] << 8) | raw_data[4])
    self._calibration_p.append((raw_data[7] << 8) | raw_data[6])
    self._calibration_p.append((raw_data[9] << 8) | raw_data[8])
    self._calibration_p.append((raw_data[11] << 8) | raw_data[10])
    self._calibration_p.append((raw_data[13] << 8) | raw_data[12])
    self._calibration_p.append((raw_data[15] << 8) | raw_data[14])
    self._calibration_p.append((raw_data[17] << 8) | raw_data[16])
    self._calibration_p.append((raw_data[19] << 8) | raw_data[18])
    self._calibration_p.append((raw_data[21] << 8) | raw_data[20])
    self._calibration_p.append((raw_data[23] << 8) | raw_data[22])
    self._calibration_h.append(raw_data[24])
    self._calibration_h.append((raw_data[26] << 8) | raw_data[25])
    self._calibration_h.append(raw_data[27])
    self._calibration_h.append((raw_data[28] << 4) | (0x0F & raw_data[29]))
    self._calibration_h.append((raw_data[30] << 4) | ((raw_data[29] >> 4) & 0x0F))
    self._calibration_h.append(raw_data[31])



    for i in range(1, 2):
        if self._calibration_t[i] & 0x8000:
            self._calibration_t[i] = (-self._calibration_t[i] ^ 0xFFFF) + 1

    for i in range(1, 8):
        if self._calibration_p[i] & 0x8000:
            self._calibration_p[i] = (-self._calibration_p[i] ^ 0xFFFF) + 1

    for i in range(0, 6):
        if self._calibration_h[i] & 0x8000:
            self._calibration_h[i] = (-self._calibration_h[i] ^ 0xFFFF) + 1



  def _oversampling(self):
      return 1 << 7 | 1 << 4

  def compensate_temperature(self, adc_t):
    v1 = (adc_t / 16384.0 - self._calibration_t[0] / 1024.0) * self._calibration_t[1]
    v2 = (adc_t / 131072.0 - self._calibration_t[0] / 8192.0) * (adc_t / 131072.0 - self._calibration_t[0] / 8192.0) * self._calibration_t[2]
    self.t_fine = v1 + v2
    temperature = self.t_fine / 5120.0
    return temperature

  def compensate_pressure(self, adc_p):
    v1 = (self.t_fine / 2.0) - 64000.0
    v2 = (((v1 / 4.0) * (v1 / 4.0)) / 2048) * self._calibration_p[5]
    v2 += ((v1 * self._calibration_p[4]) * 2.0)
    v2 = (v2 / 4.0) + (self._calibration_p[3] * 65536.0)
    v1 = (((self._calibration_p[2] * (((v1 / 4.0) * (v1 / 4.0)) / 8192)) / 8) + ((self._calibration_p[1] * v1) / 2.0)) / 262144
    v1 = ((32768 + v1) * self._calibration_p[0]) / 32768

    if v1 == 0:
        return 0

    pressure = ((1048576 - adc_p) - (v2 / 4096)) * 3125
    if pressure < 0x80000000:
        pressure = (pressure * 2.0) / v1
    else:
        pressure = (pressure / v1) * 2

    v1 = (self._calibration_p[8] * (((pressure / 8.0) * (pressure / 8.0)) / 8192.0)) / 4096
    v2 = ((pressure / 4.0) * self._calibration_p[7]) / 8192.0
    pressure += ((v1 + v2 + self._calibration_p[6]) / 16.0)

    return pressure / 100

  def compensate_humidity(self, adc_h):
    var_h = self._t_fine - 76800.0
    if var_h == 0:
        return 0

    var_h = (adc_h - (self._calibration_h[3] * 64.0 + self._calibration_h[4] / 16384.0 * var_h)) * (
        self._calibration_h[1] / 65536.0 * (1.0 + self._calibration_h[5] / 67108864.0 * var_h * (
            1.0 + self._calibration_h[2] / 67108864.0 * var_h)))
    var_h *= (1.0 - self._calibration_h[0] * var_h / 524288.0)

    if var_h > 100.0:
        var_h = 100.0
    elif var_h < 0.0:
        var_h = 0.0

    return var_h


  def readAll(self):
    "Reads the raw (uncompensated) temperature from the sensor"
    self._write_byte(self.__BME280_CONTROL_HUM, 4)
    self._write_byte(self.__BME280_CONTROL, self.mode | self._oversampling())
    time.sleep(0.1)
    raw = self._read_bytes(self.__BME280_DATA_REG, 8)
    raw_press = raw[0:3]
    raw_temp = raw[3:6]
    raw_hum = raw[6:8]
    raw_press = (raw_press[0] << 12) | (raw_press[1] << 4) | (raw_press[2] >> 4)
    raw_temp = (raw_temp[0] << 12) | (raw_temp[1] << 4) | (raw_temp[2] >> 4)
    raw_hum = (raw_hum[0] << 8) | raw_hum[1]

    self.temperature = self.compensate_temperature(raw_temp)
    self.pressure = self.compensate_pressure(raw_press)
    self.humidity = self.compensate_humidity(raw_hum)

    return self.temperature, self.pressure, self.humidity

  def readStatus(self):
    "Reads the raw (uncompensated) temperature from the sensor"
    self._write_byte(self.__BME280_CONTROL, self.mode)
    #time.sleep(0.005)  # Wait 5ms
    time.sleep(1)
    raw = self._read_bytes(self.__BME280_STATUS, 1)
    print(raw)
    return raw


  def readAltitude(self, seaLevelPressure=101325):
    "Calculates the altitude in meters"
    altitude = 0.0
    pressure = float(self.pressure * 100)
    altitude = 44330.0 * (1.0 - pow(pressure / seaLevelPressure, 0.1903))
    if (self.debug):
      print( "DBG: Altitude = %d" % (altitude))
    return altitude


  def _read_bytes(self, register, n):
     bytes_ = self.i2c_device.read_i2c_block_data(self.addr, register, n)
     return bytearray(bytes_)

  def _write_byte(self, register, byte_):
    self.i2c_device.write_byte_data(self.addr, register, byte_)
    return None

  def _read_byte(self, register):
    return self.i2c_device.read_byte_data(self.addr, register)

  def _write_bytes(self, register, *bytes_):
    bytes_ = self.i2c_device.write_i2c_block_data(self.addr, register, bytes_[0])
    return bytearray(bytes_)

bmp = BME280(mode=1, address=0x76)
#print(bmp.readPressure())
bmp.readAll()

print('Temperature: %f' % bmp.temperature)
print('Humidity: %f' % bmp.humidity)
print('Pressure: %f' % bmp.pressure)
print('Alt: %f' % bmp.readAltitude())

t = bmp.temperature
h = bmp.humidity
p = bmp.pressure

if t and h and p:
    print(t, h, p)
    out = "{0:.1f}:{1:d}:{2:.1f}".format(t, int(h), p)    
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.linger = 1000
    socket.connect ("tcp://localhost:%s" % port_lcd)
    socket.send(bytes("BME28"+out, 'ascii'), zmq.NOBLOCK)

    socket = context.socket(zmq.REQ)
    socket.linger = 1000
    socket.connect ("tcp://localhost:%s" % port_hub)
    socket.send(bytes("BME28"+out, 'ascii'), zmq.NOBLOCK)
