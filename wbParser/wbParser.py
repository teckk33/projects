import requests, pandas as pd, os

query = 'игровая клавиатура'
limit = 1000                # сколько нужно
all_products = []           # общий склад
page = 1                    # WB страницы начинаются с 1

while len(all_products) < limit:
    url = (
        'https://search.wb.ru/exactmatch/ru/common/v18/search'
        '?ab_testing=false&appType=1&curr=rub&dest=-5892277'
        f'&inheritFilters=false&lang=ru&page={page}'
        f'&query={query}&resultset=catalog&sort=popular&spp=30'
        '&suppressSpellcheck=false'
    )
    batch = requests.get(url, timeout=10).json().get('products', [])
    if not batch:          # WB больше не отдаёт
        break
    all_products.extend(batch)
    page += 1

# формируем DataFrame из нужного количества
data = [{'Бренд': p['brand'],
         'Название': p['name'],
         'Цена (₽)': int(p['sizes'][0]['price']['product'] / 100)}
        for p in all_products[:limit]]

df = pd.DataFrame(data)
df.to_excel(r'Z:/pythonProjects/wbParser/wb_products.xlsx', index=False)
print("📁 Файл сохранён в:", os.path.abspath(r'Z:/pythonProjects/wbParser/wb_products.xlsx'))