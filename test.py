import serial

# 連接到 UWB 模組的串口（請確認你的設備名稱）
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

def get_uwb_info():
    ser.write(b'si\r')  # 發送 'si' 命令查詢設備資訊
    response = ser.readlines()
    for line in response:
        print(line.decode().strip())

get_uwb_info()
ser.close()
