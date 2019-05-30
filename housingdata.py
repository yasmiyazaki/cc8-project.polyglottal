from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series, DataFrame
import time

url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&ta=13&bs=040&ekInput=41560&tj=10&nk=-1&ct=15.0&cb=10.0&kz=1&kz=2&et=15&mt=9999999&mb=35&cn=25&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&pc=30"

result = requests.get(url)
contents = result.content

soup = BeautifulSoup(contents, "html.parser")

summary = soup.find("div", {'id': 'js-bukkenList'})

# ページ数を取得
body = soup.find("body")
pages = body.find_all("div", {'class': 'pagination pagination_set-nav'})
pages_text = str(pages)
pages_split = pages_text.split('</a></li>')
num_pages = int(pages_split[0].split('>')[-1])

# URLを入れるリスト
urls = []

# 1ページ目を格納
urls.append(url)

# 2ページ目から最後のページまでを格納
for i in range(num_pages-1):
    pg = str(i+2)
    url_page = url + '&pn=' + pg
    urls.append(url_page)

name = []  # マンション名
address = []  # 住所
locations0 = []  # 立地1つ目（最寄駅/徒歩~分）
locations1 = []  # 立地2つ目（最寄駅/徒歩~分）
locations2 = []  # 立地3つ目（最寄駅/徒歩~分）
age = []  # 築年数
height = []  # 建物高さ
floor = []  # 階
rent = []  # 賃料
admin = []  # 管理費
others = []  # 敷/礼/保証/敷引,償却
floor_plan = []  # 間取り
area = []  # 専有面積
details = []  # URL

# 各ページで以下の動作をループ
for url in urls:
    # 物件リストを切り出し
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c, "html.parser")
    summary = soup.find("div", {'id': 'js-bukkenList'})

    # マンション名、住所、立地（最寄駅/徒歩~分）、築年数、建物高さが入っているcassetteitemを全て抜き出し
    cassetteitems = summary.find_all("div", {'class': 'cassetteitem'})

    # 各cassetteitemsに対し、以下の動作をループ
    for i in range(len(cassetteitems)):
        # 各建物から売りに出ている部屋数を取得
        tbodies = cassetteitems[i].find_all('tbody')

        # マンション名取得
        subtitle = cassetteitems[i].find_all("div", {
            'class': 'cassetteitem_content-title'})
        subtitle = str(subtitle)
        subtitle_rep = subtitle.replace(
            '[<div class="cassetteitem_content-title">', '')
        subtitle_rep2 = subtitle_rep.replace(
            '</div>]', '')

        # 住所取得
        subaddress = cassetteitems[i].find_all("li", {
            'class': 'cassetteitem_detail-col1'})
        subaddress = str(subaddress)
        subaddress_rep = subaddress.replace(
            '[<li class="cassetteitem_detail-col1">', '')
        subaddress_rep2 = subaddress_rep.replace(
            '</li>]', '')

        # 部屋数だけ、マンション名と住所を繰り返しリストに格納（部屋情報と数を合致させるため）
        for y in range(len(tbodies)):
            name.append(subtitle_rep2)
            address.append(subaddress_rep2)

        # 立地を取得
        sublocations = cassetteitems[i].find_all("li", {
            'class': 'cassetteitem_detail-col2'})

        # 立地は、1つ目から3つ目までを取得（4つ目以降は無視）
        for x in sublocations:
            cols = x.find_all('div')
            for j in range(len(cols)):
                text = cols[j].find(text=True)
                for y in range(len(tbodies)):
                    if j == 0:
                        locations0.append(text)
                    elif j == 1:
                        locations1.append(text)
                    elif j == 2:
                        locations2.append(text)

        # 築年数と建物高さを取得
        tbodies = cassetteitems[i].find_all('tbody')
        col3 = cassetteitems[i].find_all("li", {
            'class': 'cassetteitem_detail-col3'})
        for x in col3:
            for z in range(len(tbodies)):
                age.append(x.find_all('div')[0].string)
                height.append(x.find_all('div')[1].string)

    # 階、賃料、管理費、敷/礼/保証/敷引,償却、間取り、専有面積が入っているtable
    tables = summary.find_all('table')

    # 各建物（table）に対して、売りに出ている部屋（row）を取得
    rows = []
    for i in range(len(tables)):
        rows.append(tables[i].find_all('tr'))

    # 各部屋に対して、tableに入っているtext情報を取得し、dataリストに格納
    data = []
    for row in rows:
        for tr in row:
            cols = tr.find_all('td')
            for i in range(len(cols)):
                if i == 2:
                    getfloor = cols[i].find(text=True)
                    floor.append(getfloor.strip())
                elif i == 3:
                    getrent = cols[i].find("span", {
                        'class': 'cassetteitem_price cassetteitem_price--rent'})
                    rent.append(float(getrent.text.replace("万円", "")) * 10000)
                    getadmin = cols[i].find("span", {
                        'class': 'cassetteitem_price cassetteitem_price--administration'})
                    admin.append(getadmin.text.replace(
                        "-", "0").replace("円", ""))

                elif i == 4:
                    getdeposit = cols[i].find("span", {
                        'class': 'cassetteitem_price cassetteitem_price--deposit'})
                    getgratuity = cols[i].find("span", {
                        'class': 'cassetteitem_price cassetteitem_price--gratuity'})
                    others.append((float(getdeposit.text.replace(
                        "-", "0").replace("万円", "")) * 10000) + (float(getgratuity.text.replace(
                            "-", "0").replace("万円", "")) * 10000))
                elif i == 5:
                    getmadori = cols[i].find("span", {
                        'class': 'cassetteitem_madori'})
                    floor_plan.append(getmadori.text)
                    getmenseki = cols[i].find("span", {
                        'class': 'cassetteitem_menseki'})
                    area.append(getmenseki.text)

                elif i == 8:
                    detailurl = cols[i].find("a")
                    details.append("https://suumo.jp" + detailurl.get("href"))

    time.sleep(10)

# 各リストをシリーズ化
name = Series(name)
address = Series(address)
locations0 = Series(locations0)
locations1 = Series(locations1)
locations2 = Series(locations2)
age = Series(age)
height = Series(height)
floor = Series(floor)
rent = Series(rent)
admin = Series(admin)
others = Series(others)
floor_plan = Series(floor_plan)
area = Series(area)
area = Series(details)

# 各シリーズをデータフレーム化
suumo_df = pd.concat([name, address, locations0, locations1, locations2,
                      age, height, floor, rent, admin, others, floor_plan, area, details], axis=1)

# カラム名
suumo_df.columns = ['Name', 'Address', 'Station1', 'Station2', 'Station3', 'age',
                    'Total Floor', 'Floor', 'Rent', 'Admin', 'Other Cost', 'Plan', 'm2', "url"]

# csvファイルとして保存
suumo_df.to_csv('sumo.csv', sep='\t', encoding='utf-16')
