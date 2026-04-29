# Big Data Pipeline: курс индийской рупии (INR)

## 📌 О проекте
Реализован полный конвейер обработки данных курса индийской рупии (INR):
- Сбор данных с сайта ЦБ РФ
- Потоковая передача через Apache Kafka
- Хранение в HDFS
- Пакетная аналитика: MapReduce, Hive
- Визуализация: 6 графиков

---

## 🛠 Технологический стек
| Компонент | Технология |
|-----------|------------|
| Сбор данных | Python (requests, pandas) |
| Потоковая передача | Apache Kafka (kafka-python) |
| Хранение | HDFS (Hadoop) |
| Аналитика | MapReduce, Hive |
| Визуализация | Matplotlib, Seaborn |

---

## 📁 Структура проекта
big-data-INR-pipeline/
├── .gitignore
├── README.md
├── requirements.txt
│
├── scraper/
│ └── collect_inr.py # сбор данных с cbr-xml-daily.ru
│
├── kafka/
│ ├── batch_producer.py # читает CSV → отправляет в Kafka
│ └── consumer_hdfs.py # читает Kafka → сохраняет в HDFS
│
├── visualization/
│ └── charts.py # генерация 6 графиков
│
├── dataset/
│ └── dataset.csv # исходные данные (5 записей)
│
└── results/
├── inr_stats.png
├── inr_timeseries.png
├── inr_distribution.png
├── inr_horizontal_bar.png
├── inr_pie.png
├── inr_boxplot.png
└── report.txt

text

---

## 🚀 Запуск проекта

### 1. Установка зависимостей (локально)
```bash
pip install -r requirements.txt
2. Сбор данных (режим "за последний год")
bash
python scraper/collect_inr.py
# Выбрать режим 3
3. Запуск Kafka producer (Windows)
bash
python kafka/batch_producer.py
4. Запуск Kafka consumer → HDFS (на Cloudera VM)
bash
python kafka/consumer_hdfs.py
5. MapReduce аналитика (на VM)
bash
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
  -input /user/cloudera/raw_data/source=batch/date=2026-04-29/*.json \
  -output /user/cloudera/analytics/mr_output \
  -mapper "python3 mapper.py" -reducer "python3 reducer.py" \
  -file mapper.py -file reducer.py
6. Hive (на VM или через Hue)
sql
CREATE EXTERNAL TABLE inr_rates_raw (line STRING)
LOCATION '/user/cloudera/raw_data/source=batch/date=2026-04-29/';

CREATE TABLE inr_rates AS
SELECT 
  get_json_object(line, '$.source') as source,
  get_json_object(line, '$.timestamp') as timestamp,
  CAST(get_json_object(line, '$.rate') AS DOUBLE) as rate,
  get_json_object(line, '$.currency') as currency
FROM inr_rates_raw;
7. Визуализация (локально)
bash
python visualization/charts.py
📊 Результаты аналитики
Показатель	Значение
Количество записей	5
Минимальный курс	10.8956 руб.
Максимальный курс	11.0216 руб.
Средний курс	10.9778 руб.
📈 Графики
№	Файл	Тип
1	inr_stats.png	Столбчатая диаграмма (min/max/avg)
2	inr_timeseries.png	Временной ряд
3	inr_distribution.png	Гистограмма
4	inr_horizontal_bar.png	Горизонтальный бар
5	inr_pie.png	Круговая диаграмма
6	inr_boxplot.png	Boxplot
📝 Выводы
Курс INR в марте 2024 был стабилен (разброс ~1.15%)

Максимум зафиксирован 5 марта (11.0216 руб.)

Минимум — 7 марта (10.8956 руб.)

Конвейер успешно обработал данные через Kafka → HDFS → MapReduce → Hive → визуализацию