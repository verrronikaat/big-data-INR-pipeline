# visualization/charts.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

# Создаём папку для результатов
os.makedirs('results', exist_ok=True)

# Устанавливаем стиль
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")

# ============= ДАННЫЕ ИЗ MAPREDUCE/HIVE =============
data = {
    'source': ['batch'],
    'count': [5],
    'min_rate': [10.8956],
    'max_rate': [11.0216],
    'avg_rate': [10.9778]
}
df = pd.DataFrame(data)

# ============= ГРАФИК 1: MIN, MAX, AVG =============
fig, ax = plt.subplots(figsize=(8, 5))
metrics = ['min_rate', 'max_rate', 'avg_rate']
labels = ['Минимум', 'Максимум', 'Среднее']
colors = ['#3498db', '#e74c3c', '#2ecc71']
values = [df['min_rate'].iloc[0], df['max_rate'].iloc[0], df['avg_rate'].iloc[0]]

bars = ax.bar(labels, values, color=colors, edgecolor='black', linewidth=1.5)
ax.set_title('📊 Статистика курса INR (batch данные)', fontsize=14, fontweight='bold')
ax.set_ylabel('Курс (руб.)', fontsize=12)
ax.set_xlabel('Показатель', fontsize=12)

# Добавляем значения на столбцы
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
            f'{val:.4f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('results/inr_stats.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ График 1 сохранён: results/inr_stats.png")

# ============= ГРАФИК 2: ВСЕ ЗНАЧЕНИЯ КУРСОВ =============
# Загружаем оригинальные данные из dataset.csv
df_raw = pd.read_csv('dataset/dataset.csv')
df_raw['date'] = pd.to_datetime(df_raw['date'])

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df_raw['date'], df_raw['rate'], marker='o', linewidth=2, markersize=6, 
        color='#3498db', label='Курс INR')
ax.set_title('📈 Динамика курса INR (март 2024)', fontsize=14, fontweight='bold')
ax.set_xlabel('Дата', fontsize=12)
ax.set_ylabel('Курс (руб.)', fontsize=12)
ax.legend()
ax.grid(True, alpha=0.3)

# Добавляем аннотации min/max
min_idx = df_raw['rate'].idxmin()
max_idx = df_raw['rate'].idxmax()
ax.annotate(f'Min: {df_raw["rate"].min():.4f}', 
            xy=(df_raw['date'].iloc[min_idx], df_raw['rate'].min()),
            xytext=(10, 20), textcoords='offset points', 
            arrowprops=dict(arrowstyle='->', color='red'))
ax.annotate(f'Max: {df_raw["rate"].max():.4f}', 
            xy=(df_raw['date'].iloc[max_idx], df_raw['rate'].max()),
            xytext=(10, -20), textcoords='offset points',
            arrowprops=dict(arrowstyle='->', color='green'))

plt.tight_layout()
plt.savefig('results/inr_timeseries.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ График 2 сохранён: results/inr_timeseries.png")

# ============= ГРАФИК 3: ГИСТОГРАММА РАСПРЕДЕЛЕНИЯ =============
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(df_raw['rate'], bins=5, kde=True, color='#9b59b6', edgecolor='black')
ax.set_title('📊 Распределение курсов INR', fontsize=14, fontweight='bold')
ax.set_xlabel('Курс (руб.)', fontsize=12)
ax.set_ylabel('Частота', fontsize=12)
plt.tight_layout()
plt.savefig('results/inr_distribution.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ График 3 сохранён: results/inr_distribution.png")

# ============= ГРАФИК 4: СРАВНЕНИЕ МИНИМУМ/МАКСИМУМ/СРЕДНЕЕ (ГОРИЗОНТАЛЬНЫЙ) =============
fig, ax = plt.subplots(figsize=(8, 5))
y_pos = range(len(labels))
ax.barh(y_pos, values, color=colors, edgecolor='black')
ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.set_xlabel('Курс (руб.)', fontsize=12)
ax.set_title('📊 Сравнение показателей курса INR', fontsize=14, fontweight='bold')
ax.invert_yaxis()

for i, v in enumerate(values):
    ax.text(v + 0.02, i, f'{v:.4f}', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('results/inr_horizontal_bar.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ График 4 сохранён: results/inr_horizontal_bar.png")

# ============= ГРАФИК 5: КРУГОВАЯ ДИАГРАММА =============
# Процент от min к max (диапазон)
range_val = df['max_rate'].iloc[0] - df['min_rate'].iloc[0]
min_pct = (df['min_rate'].iloc[0] - 10.8) / 0.3 * 100
max_pct = (df['max_rate'].iloc[0] - 10.8) / 0.3 * 100
avg_pct = (df['avg_rate'].iloc[0] - 10.8) / 0.3 * 100

fig, ax = plt.subplots(figsize=(8, 8))
sizes = [df['min_rate'].iloc[0], df['max_rate'].iloc[0], df['avg_rate'].iloc[0]]
labels_pie = ['Минимум', 'Максимум', 'Среднее']
colors_pie = ['#3498db', '#e74c3c', '#2ecc71']
explode = (0.05, 0.05, 0.05)

ax.pie(sizes, explode=explode, labels=labels_pie, colors=colors_pie,
       autopct='%1.1f%%', shadow=True, startangle=90)
ax.set_title('🥧 Соотношение показателей курса INR', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('results/inr_pie.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ График 5 сохранён: results/inr_pie.png")

# ============= ГРАФИК 6: ТЕПЛОВАЯ КАРТА (или BOXPLOT) =============
fig, ax = plt.subplots(figsize=(8, 5))

# Boxplot для наглядного распределения
box_data = [df_raw['rate'].values]
bp = ax.boxplot(box_data, patch_artist=True, labels=['Курс INR'])
bp['boxes'][0].set_facecolor('#3498db')
bp['boxes'][0].set_alpha(0.7)
ax.set_title('📦 Boxplot распределения курсов INR', fontsize=14, fontweight='bold')
ax.set_ylabel('Курс (руб.)', fontsize=12)
ax.grid(True, alpha=0.3)

# Добавляем значения
median = df_raw['rate'].median()
q1 = df_raw['rate'].quantile(0.25)
q3 = df_raw['rate'].quantile(0.75)
ax.text(1, median, f'Медиана: {median:.4f}', ha='center', va='bottom', fontweight='bold')
ax.text(1, q1, f'Q1: {q1:.4f}', ha='center', va='top', fontsize=9)
ax.text(1, q3, f'Q3: {q3:.4f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('results/inr_boxplot.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ График 6 сохранён: results/inr_boxplot.png")
print("\n" + "="*50)
print("🎉 ВСЕ ГРАФИКИ СОЗДАНЫ!")
print("📁 Папка: results/")
print("   - inr_stats.png")
print("   - inr_timeseries.png")
print("   - inr_distribution.png")
print("="*50)