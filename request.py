'''
запускається зі строки : python request [назва валюти] [кількість днів]
по замовчуванню USD 1
gsckz 12ї ночі сьогоднішній день дає помилку (можна перевірити на час  і range(n - 1, -1, -1) в main замінити на range(n - 1, 0, -1)
помилки не буде і сьогоднішній день не буде викликатись)
'''
import asyncio
from datetime import datetime, timedelta
import logging

from aiohttp import ClientSession, ClientConnectorError
from sys import argv


async def request(url: str):
    async with ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.ok:
                    r = await resp.json()
                    return r
                logging.error(f"Error status: {resp.status} for {url}")
                return None
        except ClientConnectorError as err:
            logging.error(f"Connection error: {str(err)}")
            return None


def pba_handler(result,n,curr):

    exc,  = list(filter(lambda el: el["currency"] == curr, result["exchangeRate"]))

    return f"Date: {result["date"]}, {curr}: buy: {exc['purchaseRate']}, sale: {exc['saleRate']} "


async def get_exchange(url, handler):
    result = await request(url)

    if result:
        return handler(result,0, curr)
    return "Failed to retrieve data"


def main(curr,n):
    for i in range(n - 1, -1, -1):
        dat = (datetime.now().date() - timedelta(i)).strftime("%d.%m.%Y")
        URL_ARHIV = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={dat}"
        result = asyncio.run(get_exchange(URL_ARHIV, pba_handler))
        print(result)

if __name__ == '__main__':

    currs = ['USD', 'CHF', 'EUR']
    if len(argv)>1 and argv[1] in currs:
        curr =argv[1]
    else:
        curr = "USD"

    if len(argv)>2 and argv[2].isdigit() and int(argv[2])<10:
        n=int(argv[2])
    else:
        n=1

    main(curr,n)

