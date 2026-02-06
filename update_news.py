import requests
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

# News API 키
API_KEY = os.getenv("NEWS_API_KEY")
QUERY = "AI OR 인공지능"
URL = "https://newsapi.org/v2/everything"

README_PATH = "README.md"

def get_news():
    params = {
        "q": QUERY,
        "language": "ko",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": API_KEY
    }

    response = requests.get(URL, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])

        if not articles:
            return "뉴스를 찾을 수 없습니다."

        lines = []
        for i, a in enumerate(articles, 1):
            title = a["title"]
            source = a["source"]["name"]
            published = a["publishedAt"]
            lines.append(f"{i}. [{source}] {title} ({published})")

        return "\n".join(lines)
    else:
        return "뉴스 정보를 가져오는 데 실패했습니다."

def update_readme():
    news_info = get_news()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    readme_content = f"""
# 📰 News API Status

이 리포지토리는 News API를 사용하여 최신 뉴스 헤드라인을 자동으로 업데이트합니다.

## 🔥 최신 뉴스 (키워드: {QUERY})

{news_info}

⏳ 업데이트 시간: {now} (UTC)

---
자동 업데이트 봇에 의해 관리됩니다.
"""

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme_content)

if __name__ == "__main__":
    update_readme()
