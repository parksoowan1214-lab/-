import json
from datetime import datetime, timedelta
import random

now = datetime.now()

# KBO 1군 전체 야구장 (address 데이터 추가, 북->남 정렬을 위해 lat 순)
stadiums = [
    {"id": "jamsil", "name": "잠실야구장", "address": "서울 송파구", "team": "LG 트윈스 / 두산 베어스", "lat": 37.5122, "lng": 127.0719},
    {"id": "gocheok", "name": "고척 스카이돔", "address": "서울 구로구", "team": "키움 히어로즈", "lat": 37.4982, "lng": 126.8671, "dome": True},
    {"id": "incheon", "name": "인천 SSG 랜더스필드", "address": "인천 미추홀구", "team": "SSG 랜더스", "lat": 37.4371, "lng": 126.6933},
    {"id": "suwon", "name": "수원 kt 위즈파크", "address": "경기 수원시", "team": "kt 위즈", "lat": 37.2998, "lng": 127.0101},
    {"id": "daejeon", "name": "대전 한화생명 이글스파크", "address": "대전 중구", "team": "한화 이글스", "lat": 36.3172, "lng": 127.4292},
    {"id": "daegu", "name": "대구 삼성 라이온즈 파크", "address": "대구 수성구", "team": "삼성 라이온즈", "lat": 35.8412, "lng": 128.6816},
    {"id": "gwangju", "name": "광주-기아 챔피언스 필드", "address": "광주 북구", "team": "KIA 타이거즈", "lat": 35.1682, "lng": 126.8891},
    {"id": "changwon", "name": "창원 NC 파크", "address": "경남 창원시", "team": "NC 다이노스", "lat": 35.2232, "lng": 128.5830},
    {"id": "sajik", "name": "사직야구장", "address": "부산 동래구", "team": "롯데 자이언츠", "lat": 35.1944, "lng": 129.0610}
]

weather_presets = [
    {"cond": "맑음", "icon": "fa-sun", "color": "#ecc94b"},
    {"cond": "구름많음", "icon": "fa-cloud-sun", "color": "#a0aec0"},
    {"cond": "흐림", "icon": "fa-cloud", "color": "#718096"},
    {"cond": "비", "icon": "fa-cloud-rain", "color": "#4299e1"}
]

# 시간표 생성 (1시간 간격 및 18:30 추가)
time_slots = []
current_day = "오늘"

# 1. 오늘 14:00 ~ 23:00 (중간에 18:30 껴넣기)
for hour in range(14, 24, 1):
    time_slots.append({"day_label": current_day, "time": f"{hour:02d}:00"})
    if hour == 18:
        time_slots.append({"day_label": current_day, "time": "18:30"})

# 2. 내일 00:00 ~ 23:00
current_day = "내일"
for hour in range(0, 24, 1):
    time_slots.append({"day_label": current_day, "time": f"{hour:02d}:00"})

# 3. 모레 00:00 ~ 24:00 (24시를 편의상 다음날 00시로 표기)
current_day = "모레"
for hour in range(0, 24, 1):
    time_slots.append({"day_label": current_day, "time": f"{hour:02d}:00"})
time_slots.append({"day_label": "", "time": "24:00"})

kbo_data = []

for stadium in stadiums:
    hourly_forecast = []
    base_weather = random.choice(weather_presets)
    
    for slot in time_slots:
        if stadium.get("dome"):
            w = {"cond": "실내(돔)", "icon": "fa-building", "color": "#3182ce"}
        else:
            if random.random() < 0.2:
                base_weather = random.choice(weather_presets)
            w = base_weather
            
        hourly_forecast.append({
            "day_label": slot["day_label"],
            "time": slot["time"],
            "weather": w
        })
        
    kbo_data.append({
        "id": stadium["id"],
        "name": stadium["name"],
        "address": stadium["address"], # 새로 추가된 주소 데이터
        "homeTeam": stadium["team"],
        "lat": stadium["lat"],
        "lng": stadium["lng"],
        "hourly_forecast": hourly_forecast
    })

file_path = 'kbo_data.json'
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(kbo_data, f, ensure_ascii=False, indent=2)

print(f"[{now.strftime('%H:%M:%S')}] 시간대별 기상 데이터 업데이트 완료!")
