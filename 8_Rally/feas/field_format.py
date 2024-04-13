from pyral import Rally
import os
from dotenv import load_dotenv

load_dotenv()

# Rally 계정 및 프로젝트 정보
RALLY_API_KEY=os.getenv('RALLY_API_KEY')
RALLY_SERVER='rally1.rallydev.com'
RALLY_USER=os.getenv('RALLY_USER')
RALLY_PASSWORD=os.getenv('ALMPASSWORD')
RALLY_WORKSPACE = 'GEHC DevSpark'
RALLY_PROJECT = 'GI - GEUK S/W team Project'

# os.environ["http_proxy"] = "http://PITC-Zscaler-Global-ZEN.proxy.corporate.ge.com:80" #give proxy if required
# os.environ["https_proxy"] = "http://PITC-Zscaler-Global-ZEN.proxy.corporate.ge.com:80" 

# Rally에 연결
rally = Rally(RALLY_SERVER, apikey=RALLY_API_KEY, user=RALLY_USER, password=RALLY_PASSWORD,
              workspace=RALLY_WORKSPACE, project=RALLY_PROJECT)


# User Story 가져오기
response = rally.get('UserStory', fetch=True, limit=1)

# 가져온 데이터 출력
for story in response:
    print("User Story Fields and Formats:")
    for field_name in story.attributes():  # 객체의 속성을 통해 필드에 접근
        field_value = getattr(story, field_name)
        field_type = type(field_value).__name__
        print(f"Field: {field_name}, Type: {field_type}")