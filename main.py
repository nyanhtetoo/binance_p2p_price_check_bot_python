from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import requests
import json
from datetime import datetime, timedelta
import sqlite3
from time import time, sleep
import numpy as np

url = "https://www.binance.com"
endPoint = "/bapi/c2c/v2/friendly/c2c/adv/search"

print("=======================================")
print("|            CHOOSE NUMBER            |")
print("=======================================")
print("1) See all pages and all rows prices")
print("2) See single row of first page price")
choose = int(input("Choose 1 or 2: "))

# All Prices Function
def all_prices():
    global count
    global asset
    global tradeType
    global fiat
    global pages
    global row

    # for buy_price and sell_price table
    for page in range(pages):
        page = page+1
        #tradeType = 'BUY' # 'BUY' or 'SELL'
        tradeType = tradeType_input

        options = {
            'asset': asset,
            'tradeType': tradeType,
            'fiat': fiat,
            'transAmount': 0,
            'order': '',
            'page': page,
            'rows': row,
            'filterType' : 'all'
        }

        r = requests.post(url+endPoint, json=options)
        r = r.json()
        data = r['data']
        code = r['code']
        message = r['message']
        messageDetail = r['messageDetail']
        data = r['data']
        #total = r['total']
        success = r['success']

        for d in data:

            tradeType = d['adv']['tradeType']
            asset = d['adv']['asset']
            fiatUnit = d['adv']['fiatUnit']
            price = d['adv']['price']
            tradableQuantity = d['adv']['tradableQuantity']
            minSingleTransAmount = int(float(d['adv']['minSingleTransAmount']))
            #maxSingleTransAmount = d['adv']['maxSingleTransAmount']
            tradeMethodName = d['adv']['tradeMethods'][0]['tradeMethodName']
            dynamicMaxSingleTransAmount = int(float(d['adv']['dynamicMaxSingleTransAmount']))

            nickName = d['advertiser']['nickName']
            monthOrderCount = d['advertiser']['monthOrderCount']
            monthFinishRate = d['advertiser']['monthFinishRate']
            userType = d['advertiser']['userType']
            userGrade = d['advertiser']['userGrade']

            date = datetime.now()

            data = np.array([
                    count,
                    date,
                    tradeType,
                    asset,
                    price,
                    fiatUnit,
                    tradableQuantity,
                    minSingleTransAmount,
                    dynamicMaxSingleTransAmount,
                    nickName,
                    tradeMethodName,
                    monthOrderCount,
                    monthFinishRate,
                    userType,
                    userGrade
                    ])

            if tradeType == "BUY":
                trade_side = "SELL SIDE: "
            elif tradeType == "SELL":
                trade_side = "BUY SIDE: "

            print(trade_side, data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],)
            count += 1

# Single Price Function
def single_price(tradeType):
    global count

    tradeType = tradeType
    asset = 'USDT'
    fiat = 'MMK'
    row = 1
    page = 1

    options = {
        'asset': asset,
        'tradeType': tradeType,
        'fiat': fiat,
        'transAmount': 0,
        'order': '',
        'page': page,
        'rows': row,
        'filterType' : 'all'
    }

    r = requests.post(url+endPoint, json=options)
    r = r.json()
    data = r['data']
    code = r['code']
    message = r['message']
    messageDetail = r['messageDetail']
    data = r['data']
    #total = r['total']
    success = r['success']

    for d in data:

        tradeType = d['adv']['tradeType']
        asset = d['adv']['asset']
        fiatUnit = d['adv']['fiatUnit']
        price = d['adv']['price']
        tradableQuantity = d['adv']['tradableQuantity']
        minSingleTransAmount = int(float(d['adv']['minSingleTransAmount']))
        #maxSingleTransAmount = d['adv']['maxSingleTransAmount']
        tradeMethodName = d['adv']['tradeMethods'][0]['tradeMethodName']
        dynamicMaxSingleTransAmount = int(float(d['adv']['dynamicMaxSingleTransAmount']))

        nickName = d['advertiser']['nickName']
        monthOrderCount = d['advertiser']['monthOrderCount']
        monthFinishRate = d['advertiser']['monthFinishRate']
        userType = d['advertiser']['userType']
        userGrade = d['advertiser']['userGrade']

        date = datetime.now()

        data = np.array([
                count,
                date,
                tradeType,
                asset,
                price,
                fiatUnit,
                tradableQuantity,
                minSingleTransAmount,
                dynamicMaxSingleTransAmount,
                nickName,
                tradeMethodName,
                monthOrderCount,
                monthFinishRate,
                userType,
                userGrade
                ])
        if tradeType == "BUY":
            trade_side = "SELL SIDE: "
        elif tradeType == "SELL":
            trade_side = "BUY SIDE: "
        print(f'{trade_side}', data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],)

# For all_prices
if choose == 1:
    print("=======================")
    print("|  CHOOSE TRADE TYPE  |")
    print("=======================")
    print("1) BUY")
    print("2) SELL")
    choose_tradeType = int(input("Choose 1 or 2: "))

    if choose_tradeType == 1:
        tradeType_input = "BUY"
    elif choose_tradeType == 2:
        tradeType_input = "SELL"

    pages = int(input('Type page numbers: '))
    asset = 'USDT'
    fiat = 'MMK'
    row = 10
    count = 1

    while True:
        print('=============================================================================================================================================================')
        print("TradeSide","Count","Date","TradeType","Asset","Price","FiatUnit","TradableQuantity","MinAmount","MaxAmount","Trader","PaymentMethod","MonthlyOrder","MonthFinishRate","UserType","UserGrade")
        print('=============================================================================================================================================================')

        all_prices()

        sleep(60 - time() % 60)

# For single_price
elif choose == 2:
    count = 1
    #all_prices()
    while True:
        print('=============================================================================================================================================================')
        print("TradeSide","Count","Date","TradeType","Asset","Price","FiatUnit","TradableQuantity","MinAmount","MaxAmount","Trader","PaymentMethod","MonthlyOrder","MonthFinishRate","UserType","UserGrade")
        print('=============================================================================================================================================================')
        single_price("BUY")
        single_price("SELL")
        count += 1
        sleep(60 - time() % 60)

'''
asset = str(input("Type Asset Name (USDT, BTC, ..): "))
tradeType = str(input('Input Trade Type(BUY or SELL): '))
fiat = str(input('Fiat currency(MMK,USD...): '))
page = int(input('Input Page Number(1 or 2 ...): '))
row = int(input('Input Row Number(1 or 2 ...): '))


# Timer for 1 minute
while True:
    print('-------------------')

    # for buy_price and sell_price table
    for page in range(pages):
        page = page+1
        #tradeType = 'BUY' # 'BUY' or 'SELL'
        tradeType = tradeType_input

        options = {
            'asset': asset,
            'tradeType': tradeType,
            'fiat': fiat,
            'transAmount': 0,
            'order': '',
            'page': page,
            'rows': row,
            'filterType' : 'all'
        }

        r = requests.post(url+endPoint, json=options)
        r = r.json()
        data = r['data']
        code = r['code']
        message = r['message']
        messageDetail = r['messageDetail']
        data = r['data']
        #total = r['total']
        success = r['success']

        for d in data:

            tradeType = d['adv']['tradeType']
            asset = d['adv']['asset']
            fiatUnit = d['adv']['fiatUnit']
            price = d['adv']['price']
            tradableQuantity = d['adv']['tradableQuantity']
            minSingleTransAmount = int(float(d['adv']['minSingleTransAmount']))
            #maxSingleTransAmount = d['adv']['maxSingleTransAmount']
            tradeMethodName = d['adv']['tradeMethods'][0]['tradeMethodName']
            dynamicMaxSingleTransAmount = int(float(d['adv']['dynamicMaxSingleTransAmount']))

            nickName = d['advertiser']['nickName']
            monthOrderCount = d['advertiser']['monthOrderCount']
            monthFinishRate = d['advertiser']['monthFinishRate']
            userType = d['advertiser']['userType']
            userGrade = d['advertiser']['userGrade']

            date = datetime.now()

            datass = [
                    count,
                    date,
                    tradeType,
                    asset,
                    price,
                    fiatUnit,
                    tradableQuantity,
                    minSingleTransAmount,
                    dynamicMaxSingleTransAmount,
                    nickName,
                    tradeMethodName,
                    monthOrderCount,
                    monthFinishRate,
                    userType,
                    userGrade
                    ]

            #data = (datass[0],datass[1],datass[2],datass[3],datass[4],datass[5],datass[6],datass[7],datass[8],datass[9],datass[10],datass[11],datass[12],datass[13])
            count += 1
            #print(datass)

            if tradeType_input == 'BUY' or tradeType_input == 'buy':

                # Create sqlite3 database
                conn = sqlite3.connect('data/data.db')

                c = conn.cursor()

                c.execute("""CREATE TABLE IF NOT EXISTS sell_price(
                            date text,
                            tradeType text,
                            asset text,
                            price int,
                            fiatUnit text,
                            tradableQuantity float,
                            minSingleTransAmount int,
                            dynamicMaxSingleTransAmount int,
                            nickName text,
                            tradeMethodName text,
                            monthOrderCount int,
                            monthFinishRate float,
                            userType text,
                            userGrade int
                    )""")

                c.execute("INSERT INTO sell_price VALUES(:date, :tradeType, :asset, :price, :fiatUnit, :tradableQuantity, :minSingleTransAmount, :dynamicMaxSingleTransAmount, :nickName, :tradeMethodName, :monthOrderCount, :monthFinishRate, :userType, :userGrade)",
                        {
                            'date' : date,
                            'tradeType' : tradeType,
                            'asset' : asset,
                            'price' : price,
                            'fiatUnit' : fiatUnit,
                            'tradableQuantity' : tradableQuantity,
                            'minSingleTransAmount' : minSingleTransAmount,
                            'dynamicMaxSingleTransAmount' : dynamicMaxSingleTransAmount,
                            'nickName' : nickName,
                            'tradeMethodName' : tradeMethodName,
                            'monthOrderCount' : monthOrderCount,
                            'monthFinishRate' : monthFinishRate,
                            'userType' : userType,
                            'userGrade' : userGrade
                        }
                    )

                conn.commit()

                conn.close()

            elif tradeType_input == 'SELL' or tradeType_input == 'sell':

                # Create sqlite3 database
                conn = sqlite3.connect('data/data.db')

                c = conn.cursor()

                c.execute("""CREATE TABLE IF NOT EXISTS buy_price(
                            date text,
                            tradeType text,
                            asset text,
                            price int,
                            fiatUnit text,
                            tradableQuantity float,
                            minSingleTransAmount int,
                            dynamicMaxSingleTransAmount int,
                            nickName text,
                            tradeMethodName text,
                            monthOrderCount int,
                            monthFinishRate float,
                            userType text,
                            userGrade int
                    )""")

                c.execute("INSERT INTO buy_price VALUES(:date, :tradeType, :asset, :price, :fiatUnit, :tradableQuantity, :minSingleTransAmount, :dynamicMaxSingleTransAmount, :nickName, :tradeMethodName, :monthOrderCount, :monthFinishRate, :userType, :userGrade)",
                        {
                            'date' : date,
                            'tradeType' : tradeType,
                            'asset' : asset,
                            'price' : price,
                            'fiatUnit' : fiatUnit,
                            'tradableQuantity' : tradableQuantity,
                            'minSingleTransAmount' : minSingleTransAmount,
                            'dynamicMaxSingleTransAmount' : dynamicMaxSingleTransAmount,
                            'nickName' : nickName,
                            'tradeMethodName' : tradeMethodName,
                            'monthOrderCount' : monthOrderCount,
                            'monthFinishRate' : monthFinishRate,
                            'userType' : userType,
                            'userGrade' : userGrade
                        }
                    )

                conn.commit()

                conn.close()

    # for buy_price_chart and sell_price_chart table

    tradeType = tradeType_input
    options = {
        'asset': asset,
        'tradeType': tradeType,
        'fiat': fiat,
        'transAmount': 0,
        'order': '',
        'page': 1,
        'rows': 1,
        'filterType' : 'all'
    }

    r = requests.post(url+endPoint, json=options)
    r = r.json()
    data = r['data']
    code = r['code']
    message = r['message']
    messageDetail = r['messageDetail']
    data = r['data']
    #total = r['total']
    success = r['success']

    for d in data:

        tradeType = d['adv']['tradeType']
        asset = d['adv']['asset']
        fiatUnit = d['adv']['fiatUnit']
        price = d['adv']['price']
        tradableQuantity = d['adv']['tradableQuantity']
        minSingleTransAmount = int(float(d['adv']['minSingleTransAmount']))
        #maxSingleTransAmount = d['adv']['maxSingleTransAmount']
        tradeMethodName = d['adv']['tradeMethods'][0]['tradeMethodName']
        dynamicMaxSingleTransAmount = int(float(d['adv']['dynamicMaxSingleTransAmount']))

        nickName = d['advertiser']['nickName']
        monthOrderCount = d['advertiser']['monthOrderCount']
        monthFinishRate = d['advertiser']['monthFinishRate']
        userType = d['advertiser']['userType']
        userGrade = d['advertiser']['userGrade']

        date = datetime.now()

        datass = [
                count,
                date,
                tradeType,
                asset,
                price,
                fiatUnit,
                tradableQuantity,
                minSingleTransAmount,
                dynamicMaxSingleTransAmount,
                nickName,
                tradeMethodName,
                monthOrderCount,
                monthFinishRate,
                userType,
                userGrade
                ]

        #data = (datass[0],datass[1],datass[2],datass[3],datass[4],datass[5],datass[6],datass[7],datass[8],datass[9],datass[10],datass[11],datass[12],datass[13])
        count += 1

        if tradeType_input == 'BUY' or tradeType_input == 'buy':

            # Create sqlite3 database
            conn = sqlite3.connect('data/data.db')

            c = conn.cursor()

            c.execute("""CREATE TABLE IF NOT EXISTS sell_price_chart(
                        date text,
                        tradeType text,
                        asset text,
                        price int,
                        fiatUnit text,
                        tradableQuantity float,
                        minSingleTransAmount int,
                        dynamicMaxSingleTransAmount int,
                        nickName text,
                        tradeMethodName text,
                        monthOrderCount int,
                        monthFinishRate float,
                        userType text,
                        userGrade int
                )""")

            c.execute("INSERT INTO sell_price_chart VALUES(:date, :tradeType, :asset, :price, :fiatUnit, :tradableQuantity, :minSingleTransAmount, :dynamicMaxSingleTransAmount, :nickName, :tradeMethodName, :monthOrderCount, :monthFinishRate, :userType, :userGrade)",
                    {
                        'date' : date,
                        'tradeType' : tradeType,
                        'asset' : asset,
                        'price' : price,
                        'fiatUnit' : fiatUnit,
                        'tradableQuantity' : tradableQuantity,
                        'minSingleTransAmount' : minSingleTransAmount,
                        'dynamicMaxSingleTransAmount' : dynamicMaxSingleTransAmount,
                        'nickName' : nickName,
                        'tradeMethodName' : tradeMethodName,
                        'monthOrderCount' : monthOrderCount,
                        'monthFinishRate' : monthFinishRate,
                        'userType' : userType,
                        'userGrade' : userGrade
                    }
                )

            conn.commit()

            conn.close()

        elif tradeType_input == 'SELL' or tradeType_input == 'sell':

            # Create sqlite3 database
            conn = sqlite3.connect('data/data.db')

            c = conn.cursor()

            c.execute("""CREATE TABLE IF NOT EXISTS buy_price_chart(
                        date text,
                        tradeType text,
                        asset text,
                        price int,
                        fiatUnit text,
                        tradableQuantity float,
                        minSingleTransAmount int,
                        dynamicMaxSingleTransAmount int,
                        nickName text,
                        tradeMethodName text,
                        monthOrderCount int,
                        monthFinishRate float,
                        userType text,
                        userGrade int
                )""")

            c.execute("INSERT INTO buy_price_chart VALUES(:date, :tradeType, :asset, :price, :fiatUnit, :tradableQuantity, :minSingleTransAmount, :dynamicMaxSingleTransAmount, :nickName, :tradeMethodName, :monthOrderCount, :monthFinishRate, :userType, :userGrade)",
                    {
                        'date' : date,
                        'tradeType' : tradeType,
                        'asset' : asset,
                        'price' : price,
                        'fiatUnit' : fiatUnit,
                        'tradableQuantity' : tradableQuantity,
                        'minSingleTransAmount' : minSingleTransAmount,
                        'dynamicMaxSingleTransAmount' : dynamicMaxSingleTransAmount,
                        'nickName' : nickName,
                        'tradeMethodName' : tradeMethodName,
                        'monthOrderCount' : monthOrderCount,
                        'monthFinishRate' : monthFinishRate,
                        'userType' : userType,
                        'userGrade' : userGrade
                    }
                )

            conn.commit()

            conn.close()

    # Create sqlite3 database
    conn = sqlite3.connect('data/data.db')

    c = conn.cursor()

    if tradeType_input == 'BUY' or tradeType_input == 'buy':

        c.execute("SELECT oid,* FROM sell_price_chart ORDER BY date DESC LIMIT 1")
        min_prices = c.fetchall()
        for min_price in min_prices:
            #min_price = min_price[4]
            df = pd.DataFrame(min_price)
            print(df)


        c.execute("SELECT MIN(price),oid,* FROM sell_price")
        min_prices = c.fetchall()
        for min_price in min_prices:
            print(min_price)

        c.execute("SELECT oid,* FROM sell_price")
        records = c.fetchall()
        for record in records:
            print(record)

        c.execute("SELECT MAX(price),oid,* FROM sell_price")
        max_prices = c.fetchall()
        for max_price in max_prices:
            print(max_price)

        c.execute("SELECT * FROM sell_price ORDER BY date DESC LIMIT 1")
        records = c.fetchall()
        for record in records:
            print(record)


    elif tradeType_input == 'SELL' or tradeType_input == 'sell':

        c.execute("SELECT oid,* FROM buy_price_chart ORDER BY date DESC LIMIT 1")
        max_prices = c.fetchall()
        for max_price in max_prices:
            #max_price = max_price[4]
            print(max_price)


        c.execute("SELECT MAX(price),oid,* FROM buy_price")
        max_prices = c.fetchall()
        for max_price in max_prices:
            print(max_price)

        c.execute("SELECT oid,* FROM buy_price")
        records = c.fetchall()
        for record in records:
            print(record)

        c.execute("SELECT MIN(price),oid,* FROM buy_price")
        min_prices = c.fetchall()
        for min_price in min_prices:
            print(min_price)

        c.execute("SELECT * FROM buy_price ORDER BY date DESC LIMIT 1")
        records = c.fetchall()
        for record in records:
            print(record)

    conn.commit()

    conn.close()

    sleep(60 - time() % 60)


# Create pandas dataframe
datas = {
    'datetime' : [datetime.now()],
    'tradeType': [tradeType],
    'asset' : [asset],
    'price' : [price],
    'fiatUnit' : [fiatUnit],
    'tradableQuantity' : [tradableQuantity],
    'minAmount' : [minSingleTransAmount],
    'maxAmount' : [dynamicMaxSingleTransAmount],
    'trader' : [nickName],
    'paymentMethod' : [tradeMethodName],
    'monthOrderCount' : [monthOrderCount],
    'monthFinishRate' : [monthFinishRate],
    'userType' : [userType],
    'userGrade' : [userGrade]
    }

datass = [
        count,
        datetime.now(),
        tradeType,
        asset,
        price,
        fiatUnit,
        tradableQuantity,
        minSingleTransAmount,
        dynamicMaxSingleTransAmount,
        nickName,
        tradeMethodName,
        monthOrderCount,
        monthFinishRate,
        userType,
        userGrade
        ]

df = pd.DataFrame.from_dict(datas, orient='columns')
#df = pd.DataFrame(datas)
#df = pd.DataFrame.from_dict(datas, orient='columns')  #orient='index',orient='columns', orient='tight'

#df.to_csv('data/name.csv')
print(df)

print('----------------------------------------***----------------------------------------')
print(f'{tradeType}')
print(f'Price is                                {price} {fiatUnit}')
#print(f'Asset is {asset}')
#print(fiatUnit)
print(f'Available {tradeType.lower()} amount is                {tradableQuantity} {asset}')
print(f'{tradeType.capitalize()} limit is                           {minSingleTransAmount} {fiatUnit} ~ {dynamicMaxSingleTransAmount} {fiatUnit}')
#print(dynamicMaxSingleTransAmount)
print(f'Trader is                               {nickName}')
print(f'Payment method is                       {tradeMethodName}')
print(f'Trader monthly order is                 {monthOrderCount}')
print(f'Trader monthly order completion is      {monthFinishRate*100} %')
print(f'Trader type is                          {userType}')
print(f'Trader grade is                         {userGrade}')

print('----------------------------------------***----------------------------------------')
'''
