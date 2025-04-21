import serial
import time
import csv
import re
import numpy as np

# ======= 使用者自定參數 =======
SERIAL_PORT = "/dev/ttyUSB0"          # 根據實際埠名修改
BAUD_RATE = 57600                     # 使用者指定
ANCHOR_ID = "0241000000000000"        # 目標 Anchor
MEASURE_TIMES = 20                    # 每個點測 N 次
OUTPUT_FILE = "uwb_precision_test.csv"
# =================================

def extract_distance_from_line(line):
    """
    從字串中抓取 Anchor ID 和對應距離 (單位：cm)
    支援格式如：SRC:TAG DEST:0241000000000000 DIST:123.4cm
    """
    if ANCHOR_ID in line and "DIST:" in line:
        match = re.search(r"DIST[:\s]*(\d+\.?\d*)", line)
        if match:
            return float(match.group(1))  # 預設單位為 cm
    return None

def record_measurements(actual_distance):
    """
    針對單一距離測試點進行多次量測，並統計數據
    """
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"\n📏 開始測試（目標距離：{actual_distance} cm）")

    distances = []

    while len(distances) < MEASURE_TIMES:
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        distance = extract_distance_from_line(line)
        if distance:
            distances.append(distance)
            print(f"第 {len(distances):>2} 次：{distance:.2f} cm")
        time.sleep(0.1)

    ser.close()

    avg = np.mean(distances)
    error = avg - actual_distance
    std = np.std(distances)

    return {
        "actual": actual_distance,
        "average": round(avg, 2),
        "error": round(error, 2),
        "std_dev": round(std, 2),
        "samples": distances,
    }

def save_to_csv(results):
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["實際距離(cm)", "平均距離(cm)", "誤差(cm)", "標準差", "測量樣本（cm）"])
        for res in results:
            writer.writerow([
                res["actual"],
                res["average"],
                res["error"],
                res["std_dev"],
                ", ".join(f"{d:.1f}" for d in res["samples"])
            ])
    print(f"\n✅ 測試完成，資料儲存於：{OUTPUT_FILE}")

def main():
    print("=== UWB 精度測試：指定 Anchor 模式 ===")
    print(f"🎯 測試 Anchor ID: {ANCHOR_ID}\n")

    test_points = []

    while True:
        try:
            actual = float(input("請輸入測試點實際距離 (cm)，輸入 0 結束測試："))
            if actual == 0:
                break
            result = record_measurements(actual)
            test_points.append(result)
        except ValueError:
            print("⚠️ 請輸入有效數字")

    if test_points:
        save_to_csv(test_points)
    else:
        print("❗ 沒有執行任何測試")

if __name__ == "__main__":
    main()
