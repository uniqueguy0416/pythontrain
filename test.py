import spidev
import RPi.GPIO as GPIO
import time

# 初始化 SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI 0, Chip Select 0
spi.max_speed_hz = 1000000  # 設置 SPI 速度

# 讀取 DW1000 註冊的 WHO_AM_I
def read_register(address):
    response = spi.xfer2([address, 0x00])
    return response[1]

WHO_AM_I = 0x00  # DW1000 WHO_AM_I 註冊位址
device_id = read_register(WHO_AM_I)
print(f"DW1000 Device ID: {hex(device_id)}")