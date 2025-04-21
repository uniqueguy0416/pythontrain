import serial
import time

# 請根據你的環境修改這兩個參數
SERIAL_PORT = "/dev/ttyUSB0"  # Windows 改成 COM3、COM4...
BAUD_RATE = 57600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"✅ 已連接至 {SERIAL_PORT}，正在接收資料...\n")

    while True:
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        if line:
            print(f"📡 收到資料：{line}")
        time.sleep(0.1)

except serial.SerialException as e:
    print(f"❌ 串列埠錯誤：{e}")
except KeyboardInterrupt:
    print("🛑 使用者中斷程式")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
