import aiohttp
import requests
import asyncio
from aiohttp import ClientSession
import json


# -------------------------------------------------------------
# print("создать обьявлние")
#
async def f1rst_adve():
    async with ClientSession() as session:
        respons = await session.post('http://127.0.0.3:5001/post', json={
            "head_adv": "me want  to sell  u something",
            "text_of_adv": "aima seller, aima selling chair"})
        print(respons.status)
        print(await respons.json())
#
async def second_adve():
    async with ClientSession() as session:
        respons = await session.post('http://127.0.0.3:5001/post', json={
            "head_adv": "aima sella",
            "text_of_adv": "aima selling chairnoir"})
        print(respons.status)
        print(await respons.json())


async def give_me_adv():
    async with ClientSession() as session:
        respons = await session.get('http://127.0.0.3:5001/get/1', json={})
        print(respons.status)
        print(await respons.json())

async def change_adv():
    async with ClientSession() as session:
        respons = await session.patch('http://127.0.0.3:5001/patch/2', json={"head_adv": "selling my soul"})
        print(respons.status)
        print(await respons.json())
#
async def give_me_adv2():
    async with ClientSession() as session:
        respons = await session.get('http://127.0.0.3:5001/get/2', json={})
        print(respons.status)
        print(await respons.json())
#
async def c3rd_adve():
    async with ClientSession() as session:
        respons = await session.post('http://127.0.0.3:5001/post', json={
            "head_adv": "joker3",
            "text_of_adv": "joker is the seller"})
        print(respons.status)
        print(await respons.json())
#
async def c3rd_adve_will_delete():
    async with ClientSession() as session:
        respons = await session.delete('http://127.0.0.3:5001/delete/3')
        print(respons.status)
        print(await respons.json())

#
async def main():
    await f1rst_adve() ###  создать 1 объявление.
        #
    await second_adve() ### создать второе объявление

    await c3rd_adve()  ### создать  третее объявление

    await give_me_adv() ### поиск  первого объявления

    await change_adv() ### изменить в обьявлении2 чтото

    await give_me_adv2()  ###  посмотреть второе с изменениями.

    await c3rd_adve_will_delete() ###  удалить третее объявление

if __name__ == '__main__':
    asyncio.run(main())
