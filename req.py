import asyncio
from datetime import datetime, timedelta
import logging

from aiohttp import ClientSession, ClientConnectorError
from sys import argv


URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
URL_NBU = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'





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

def pb_handler(result):
    exc,  = list(filter(lambda el: el["ccy"] == "USD", result))
    return f"Date: {datetime.now().date()}, USD: buy: {exc['buy']}, sale: {exc['sale']} "




def nbu_handler(result):
    return result[0]


async def get_exchange(url, handler):
    result = await request(url)

    if result:
        return handler(result)
    return "Failed to retrieve data"

def main_req():
    result = asyncio.run(get_exchange(URL, pb_handler))
    return (result)


if __name__ == '__main__':
    print(main_req())




        # print(URL_ARHIV)
        #tasks.append(asyncio.create_task(get_exchange(URL_ARHIV, pba_handler)))
        # await task

    #result=[]
    # for task in tasks:
    #     result.append(await task)
    # return result

