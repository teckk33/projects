import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import openpyxl
from openpyxl.drawing.image import Image

# 1. читаем данные
df = pd.read_csv(r'C:/Users/user/Desktop/csvReport/sales.csv', parse_dates=['date'])
df['revenue'] = df['quantity'] * df['price']

# 2. сводная таблица
pivot = pd.pivot_table(df,
                       index='product',
                       columns='region',
                       values='revenue',
                       aggfunc='sum',
                       fill_value=0)

# 3. строим график
daily = df.groupby('date')['revenue'].sum()
plt.figure(figsize=(8, 4))
plt.plot(daily.index, daily.values, marker='o')
plt.title('Выручка по дням')
plt.ylabel('Руб.')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('C:/Users/user/Desktop/csvReport/screenshots/chart.png', dpi=150)
plt.close()

# 4. заканчиваем работу с файлом и сохраняем результат в хлсх
with pd.ExcelWriter('C:/Users/user/Desktop/csvReport/output/sales_report.xlsx', engine='openpyxl') as writer:
    pivot.to_excel(writer, sheet_name='Сводная')
    wb = writer.book
    ws = wb.create_sheet('График')
    ws.add_image(Image('chart.png'), 'B2')

print('Готово: sales_report.xlsx')