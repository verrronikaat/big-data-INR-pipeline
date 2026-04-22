import requests
from loguru import logger

logger.add("logs/collect_inr.log", rotation="1 MB")

CURRENCY = "INR"
url_today = "https://www.cbr-xml-daily.ru/daily_json.js"

try:
    response = requests.get(url_today)
    data = response.json()
    rate = data["Valute"][CURRENCY]["Value"]
    logger.success(f"Курс {CURRENCY}: {rate} руб.")
    print(f"✅ Курс {CURRENCY} на сегодня: {rate} руб.")
except Exception as e:
    logger.error(f"Ошибка: {e}")
    print(f"❌ Ошибка: {e}")