import pandas as pd
import numpy as np

# ==========================
# 1. อ่านไฟล์ข้อมูล
# ==========================
df = pd.read_csv("iot_sensor_raw_data_extended.csv")

print("="*60)
print("รายงานการตรวจสอบคุณภาพข้อมูล")
print("="*60)

print(f"\nจำนวนข้อมูลทั้งหมด : {len(df)} แถว")

# ==========================
# 2. ตรวจสอบปัญหาก่อนทำความสะอาด
# ==========================

# Duplicate
duplicate_count = df.duplicated(subset=["device_id", "timestamp"]).sum()

# Missing Value
missing_device = df["device_id"].isna().sum() + (df["device_id"] == "").sum()
missing_temp = df["temp_c"].isna().sum()
missing_battery = df["battery"].isna().sum()

# Outlier / Error
temp_error = ((df["temp_c"] < 0) | (df["temp_c"] > 50)).sum()
battery_error = ((df["battery"] < 0) | (df["battery"] > 100)).sum()

print("\nปัญหาที่พบก่อนทำความสะอาด")
print("-"*60)
print(f"Duplicate                : {duplicate_count}")
print(f"Missing device_id        : {missing_device}")
print(f"Missing temp_c           : {missing_temp}")
print(f"Missing battery          : {missing_battery}")
print(f"Outlier temp_c           : {temp_error}")
print(f"Outlier battery          : {battery_error}")

# ==========================
# 3. ลบข้อมูลซ้ำ
# ==========================
before_duplicate = len(df)

df = df.drop_duplicates(subset=["device_id", "timestamp"])

after_duplicate = len(df)

print("\nลบข้อมูลซ้ำ")
print(f"ก่อนลบ : {before_duplicate} แถว")
print(f"หลังลบ : {after_duplicate} แถว")
print(f"ลบออก : {before_duplicate-after_duplicate} แถว")

# ==========================
# 4. แปลง Outlier เป็น NaN
# ==========================
df.loc[(df["temp_c"] < 0) | (df["temp_c"] > 50), "temp_c"] = np.nan
df.loc[(df["battery"] < 0) | (df["battery"] > 100), "battery"] = np.nan

# ==========================
# 5. จัดการ Missing Value
# ==========================

df["device_id"] = df["device_id"].fillna("UNKNOWN")
df["device_id"] = df["device_id"].replace("", "UNKNOWN")

df["temp_c"] = df["temp_c"].fillna(df["temp_c"].median())
df["battery"] = df["battery"].fillna(df["battery"].median())

# ==========================
# 6. เพิ่มสถานะข้อมูล
# ==========================
df["data_quality_status"] = "Clean"

# ==========================
# 7. ตรวจสอบหลังทำความสะอาด
# ==========================

duplicate_after = df.duplicated(subset=["device_id", "timestamp"]).sum()

missing_device_after = df["device_id"].isna().sum() + (df["device_id"] == "").sum()
missing_temp_after = df["temp_c"].isna().sum()
missing_battery_after = df["battery"].isna().sum()

temp_error_after = ((df["temp_c"] < 0) | (df["temp_c"] > 50)).sum()
battery_error_after = ((df["battery"] < 0) | (df["battery"] > 100)).sum()

print("\nผลหลังทำความสะอาด")
print("-"*60)
print(f"จำนวนข้อมูลทั้งหมด      : {len(df)} แถว")
print(f"Duplicate               : {duplicate_after}")
print(f"Missing device_id       : {missing_device_after}")
print(f"Missing temp_c          : {missing_temp_after}")
print(f"Missing battery         : {missing_battery_after}")
print(f"Outlier temp_c          : {temp_error_after}")
print(f"Outlier battery         : {battery_error_after}")

# ==========================
# 8. สรุปผล
# ==========================

summary = pd.DataFrame({
    "ประเภทปัญหา": [
        "Duplicate",
        "Missing device_id",
        "Missing temp_c",
        "Missing battery",
        "Outlier temp_c",
        "Outlier battery"
    ],
    "ก่อนทำความสะอาด": [
        duplicate_count,
        missing_device,
        missing_temp,
        missing_battery,
        temp_error,
        battery_error
    ],
    "หลังทำความสะอาด": [
        duplicate_after,
        missing_device_after,
        missing_temp_after,
        missing_battery_after,
        temp_error_after,
        battery_error_after
    ]
})

# บันทึกข้อมูลที่ทำความสะอาดแล้ว
df.to_csv("iot_sensor_cleaned_data.csv", index=False)

print("\nบันทึกไฟล์เรียบร้อย")
print("iot_sensor_cleaned_data.csv")