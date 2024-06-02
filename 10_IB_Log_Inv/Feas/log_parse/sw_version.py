import pandas as pd
import re

# 샘플 데이터프레임 생성
data = {
    'Text': [
        "Overall SW version R4.5.5 is released.",
        "Overall SW version R4.6.0 is released.",
        "Overall SW version R4.6.1 is released."
    ]
}
df = pd.DataFrame(data)

# 정규표현식 패턴
pattern = r'Overall SW version (\S+)'

# 각 행에 대해 정규표현식을 적용하여 값을 추출하여 새로운 열에 저장
df['Version'] = df['Text'].apply(lambda x: re.search(pattern, x).group(1) if re.search(pattern, x) else None)

# 결과 출력
print(df)
