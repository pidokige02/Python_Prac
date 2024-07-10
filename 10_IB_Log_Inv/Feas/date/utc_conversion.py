import pandas as pd

# 샘플 데이터
data = [
    "2024-03-21 23:59:35.0650000 +09:00\tTRK\t0x200\t1193\t603\t1\t0\t0\t3164\t36",
    "2024-03-21 23:59:35.2070000 +09:00\tFPS\tSET_KEY_4\t0\t\t0\t0\t0\t3165\t36",
    "2024-03-21 23:59:35.2070000 +09:00\tTRK\t0x202\t1193\t603\t0\t0\t0\t3166\t36",
    "2024-03-21 11:59:35.2290000 -03:00\tTRK\t0x200\t1193\t603\t1\t0\t0\t3167\t36",
    "2024-03-21 11:59:35.2330000 -03:00\tTRK\t0x200\t882\t648\t1\t0\t0\t3168\t36",
    "2024-03-21 11:59:35.8150000 -03:00\tTRK\t0x200\t881\t648\t1\t0\t0\t3169\t36"
]

# 데이터프레임 생성
df = pd.DataFrame([x.split('\t') for x in data], columns=['Timestamp', 'Type', 'Code', 'Value1', 'Value2', 'Value3', 'Value4', 'Value5', 'ID', 'Unknown'])

# 타임스탬프를 datetime으로 변환하고 UTC로 변환
df['Timestamp'] = pd.to_datetime(df['Timestamp'], utc=True)

# 결과 출력
print(df)
