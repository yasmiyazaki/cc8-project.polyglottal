from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series, DataFrame
import time


def getapartments(thisurl):
    url = thisurl
    # url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&ta=13&bs=040&ekInput=41560&tj=10&nk=-1&ct=15.0&cb=10.0&co=1&et=7&mt=9999999&mb=0&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&pc=30"

    result = requests.get(url)
    contents = result.content

    soup = BeautifulSoup(contents, "html.parser")

    summary = soup.find("div", {'id': 'js-bukkenList'})

    # get page number
    body = soup.find("body")
    pages = body.find_all("div", {'class': 'pagination pagination_set-nav'})
    pages_text = str(pages)
    pages_split = pages_text.split('</a></li>')
    num_pages = int(pages_split[-2].split('>')[-1])

    # store all urls
    urls = []

    # store first parge
    urls.append(url)

    # store rest of the pages (from two to the end)
    for i in range(num_pages-1):
        pg = str(i+2)
        url_page = url + '&pn=' + pg
        urls.append(url_page)

    name = []  # name of apartment
    address = []
    locations0 = []  # closest station and how long it takes to get there
    locations1 = []  # closest station and how long it takes to get there
    locations2 = []  # closest station and how long it takes to get there
    age = []  # how many years ago the building was built
    height = []  # how many floors it has
    floor = []  # the floor of the rent
    rent = []  # how much per month
    admin = []  # administration fee
    others = []  # other costs
    floor_plan = []
    area = []  # size of the room
    details = []  # URL

    # Loop all the pages
    for url in urls:
        # get all lists of apartmemt
        result = requests.get(url)
        c = result.content
        soup = BeautifulSoup(c, "html.parser")
        summary = soup.find("div", {'id': 'js-bukkenList'})

        # get DOM of all general info
        cassetteitems = summary.find_all("div", {'class': 'cassetteitem'})

        # loop the DOM
        for i in range(len(cassetteitems)):
            # get how many rooms are available in the apartment
            tbodies = cassetteitems[i].find_all('tbody')

            # get name of the apartment
            subtitle = cassetteitems[i].find_all("div", {
                'class': 'cassetteitem_content-title'})
            subtitle = str(subtitle)
            subtitle_rep = subtitle.replace(
                '[<div class="cassetteitem_content-title">', '')
            subtitle_rep2 = subtitle_rep.replace(
                '</div>]', '')

            # get address
            subaddress = cassetteitems[i].find_all("li", {
                'class': 'cassetteitem_detail-col1'})
            subaddress = str(subaddress)
            subaddress_rep = subaddress.replace(
                '[<li class="cassetteitem_detail-col1">', '')
            subaddress_rep2 = subaddress_rep.replace(
                '</li>]', '')

            # loop the above data by number of rooms available
            for y in range(len(tbodies)):
                name.append(subtitle_rep2)
                address.append(subaddress_rep2)

            # get closest station info
            sublocations = cassetteitems[i].find_all("li", {
                'class': 'cassetteitem_detail-col2'})

            # get three of them
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

            # get year and highest floor of the apartment
            tbodies = cassetteitems[i].find_all('tbody')
            col3 = cassetteitems[i].find_all("li", {
                'class': 'cassetteitem_detail-col3'})
            for x in col3:
                for z in range(len(tbodies)):
                    age.append(x.find_all('div')[0].string)
                    height.append(x.find_all('div')[1].string)

        # get detail info
        tables = summary.find_all('table')

        # get each info in detail
        rows = []
        for i in range(len(tables)):
            rows.append(tables[i].find_all('tr'))

        # get all detail info and store them to each variables
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
                        rent.append(
                            float(getrent.text.replace("万円", "")) * 10000)
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
                        details.append("https://suumo.jp" +
                                       detailurl.get("href"))

    time.sleep(1)

    # make list
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
    details = Series(details)

    # make the list into dataframe
    suumo_df = pd.concat([name, address, locations0, locations1, locations2, age,
                          height, floor, rent, admin, others, floor_plan, area, details], axis=1)

    # male columns
    suumo_df.columns = ['Name', 'Address', 'Station1', 'Station2', 'Station3', 'age',
                        'Total Floor', 'Floor', 'Rent', 'Admin', 'Other Cost', 'Plan', 'm2', "url"]
    # save as csv
    # suumo_df.to_csv('../sumo.csv', sep='\t', encoding='utf-16')

    return suumo_df.to_json()
