import json
from datetime import datetime, timedelta
import random

# 오늘, 내일, 모레 날짜 계산
now = datetime.now()
dates = [
    {"label": "오늘", "date_str": now.strftime("%m/%d")},
    {"label": "내일", "date_str": (now + timedelta(days=1)).strftime("%m/%d")},
    {"label": "모레", "date_str": (now + timedelta(days=2)).strftime("%m/%d")}
]

# 날씨 상태 프리셋
weather_presets = [
    {"cond": "맑음", "icon": "fa-sun", "color": "#ecc94b"},
    {"cond": "구름많음", "icon": "fa-cloud-sun", "color": "#a0aec0"},
    {"cond": "흐림", "icon": "fa-cloud", "color": "#718096"},
    {"cond": "비", "icon": "fa-cloud-rain", "color": "#4299e1"}
]

# ---------------------------------------------------------
# [향후 크롤링 및 API 연동 위치]
# 1. KBO 일정 크롤링: BeautifulSoup을 이용해 3일치 매치업 수집
# 2. 날씨 API 연동: OpenWeatherMap 등에서 구장 좌표(lat, lng) 기반 3일 예보 수집
# ---------------------------------------------------------

kbo_data = []
stadiums = [
    {"id": "sajik", "name": "사직야구장", "team": "롯데", "lat": 35.1944, "lng": 129.0610, "opp": "KIA"},
    {"id": "jamsil", "name": "잠실야구장", "team": "LG/두산", "lat": 37.5122, "lng": 127.0719, "opp": "SSG"},
    {"id": "changwon", "name": "창원 NC 파크", "team": "NC", "lat": 35.2232, "lng": 128.5830, "opp": "삼성"},
    {"id": "gocheok", "name": "고척 스카이돔", "team": "키움", "lat": 37.4982, "lng": 126.8671, "opp": "한화", "dome": True},
    {"id": "gwangju", "name": "광주 챔피언스필드", "team": "KIA", "lat": 35.1682, "lng": 126.8891, "opp": "롯데"}
]

# 가상의 3일치 데이터 생성
for stadium in stadiums:
    forecast_3days = []
    for d in dates:
        # 고척돔은 항상 실내 날씨로 고정
        if stadium.get("dome"):
            w = {"cond": "실내(돔)", "icon": "fa-building", "color": "#3182ce"}
        else:
            w = random.choice(weather_presets)
        
        # 임의로 모레는 경기가 없는 것으로 설정해보기
        has_game = False if d["label"] == "모레" else True
        
        forecast_3days.append({
            "label": d["label"],
            "date": d["date_str"],
            "weather": w,
            "hasGame": has_game,
            "gameInfo": f"vs {stadium['opp']}<br>18:30" if has_game else "경기 없음"
        })
        
    kbo_data.append({
        "id": stadium["id"],
        "name": stadium["name"],
        "homeTeam": stadium["team"],
        "lat": stadium["lat"],
        "lng": stadium["lng"],
        "forecast": forecast_3days
    })

file_path = 'kbo_data.json'
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(kbo_data, f, ensure_ascii=False, indent=2)

print(f"[{now.strftime('%H:%M:%S')}] 3일치 날씨 및 일정 데이터 업데이트 완료!")
