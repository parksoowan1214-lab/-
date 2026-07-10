import json
from datetime import datetime, timedelta
import random

now = datetime.now()

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

def get_weather_icon(hour, base_cond):
    is_night = hour >= 19 or hour < 6
    if base_cond == "맑음":
        return "fa-moon" if is_night else "fa-sun", "#6366f1" if is_night else "#ecc94b"
    if base_cond == "구름많음":
        return "fa-cloud-moon" if is_night else "fa-cloud-sun", "#94a3b8"
    if base_cond == "흐림":
        return "fa-cloud", "#718096"
    return "fa-cloud-rain", "#4299e1"

time_slots = []
current_day = "오늘"
for hour in range(14, 24, 1):
    time_slots.append({"day_label": current_day, "time": f"{hour:02d}:00", "hour": hour})
    if hour == 18:
        time_slots.append({"day_label": current_day, "time": "18:30", "hour": 18})

# ... 내일/모레 로직은 동일 ...
current_day = "내일"
for hour in range(0, 24, 1):
    time_slots.append({"day_label": current_day, "time": f"{hour:02d}:00", "hour": hour})

current_day = "모레"
for hour in range(0, 24, 1):
    time_slots.append({"day_label": current_day, "time": f"{hour:02d}:00", "hour": hour})
time_slots.append({"day_label": "", "time": "24:00", "hour": 24})

kbo_data = []
for stadium in stadiums:
    hourly_forecast = []
    base_cond = random.choice(["맑음", "구름많음", "흐림", "비"])
    
    for slot in time_slots:
        if stadium.get("dome"):
            w = {"cond": "실내", "icon": "fa-building", "color": "#3182ce"}
        else:
            if random.random() < 0.1: base_cond = random.choice(["맑음", "구름많음", "흐림", "비"])
            icon, color = get_weather_icon(slot["hour"], base_cond)
            w = {"cond": base_cond, "icon": icon, "color": color}
            
        hourly_forecast.append({"day_label": slot["day_label"], "time": slot["time"], "weather": w})
        
    kbo_data.append({"id": stadium["id"], "name": stadium["name"], "address": stadium["address"], "homeTeam": stadium["team"], "lat": stadium["lat"], "lng": stadium["lng"], "hourly_forecast": hourly_forecast})

with open('kbo_data.json', 'w', encoding='utf-8') as f:
    json.dump(kbo_data, f, ensure_ascii=False, indent=2)
