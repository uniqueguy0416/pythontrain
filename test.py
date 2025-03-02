import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)  # SPI 0, Chip Select 0
spi.max_speed_hz = 1000000  # 設定 SPI 速度為 1MHz

def read_register(address):
    response = spi.xfer2([address, 0x00, 0x00, 0x00, 0x00])
    return response[1:]

WHO_AM_I = 0x00  # DW1000 註冊位址
device_id = read_register(WHO_AM_I)
print(f"DW1000 Device ID: {device_id}")
