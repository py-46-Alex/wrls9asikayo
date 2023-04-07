# This is a sample Python script.
import atexit
import json
import os

from sqlalchemy import create_engine, func, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
import pydantic
from typing import Optional
from typing import Type
import sys
import asyncio
from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select


os.environ["SQLALCHEMY_SILENCE_UBER_WARNING"]="1"
#

if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#
PG_DSN = 'postgresql+asyncpg://appadmin:1234@127.0.0.1:5431/appdb'
engine = create_async_engine(PG_DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
#
Base = declarative_base()
#
app = web.Application()
#
async def init_orm(app):
    print("app STARTED")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("app is CLOSING NOW")
#
@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request['session'] = session
        response = await handler(request)
        return response
#
app.middlewares.append(session_middleware)
app.cleanup_ctx.append(init_orm)
#
async def get_adve(adver_id: int, session: Session):
    adver = await session.get(Useradven, adver_id)
    if adver is None:
        raise web.HTTPNotFound(text=json.dumps({"status": "eror", "message": "not found this"}),
                               content_type='application/json')
    return adver
#
class Useradven(Base):
    __tablename__ = 'app_adv'

    id = Column(Integer, primary_key=True, autoincrement=True)
    head_adv = Column(String, nullable=False)
    text_of_adv = Column(String, nullable=False)
#     time_create = Column(DateTime, server_default=func.now())
#     autor = Column(String, index=True, unique=False)
#
#
class UserView(web.View):
    async def get(self):
        adversi = await get_adve(int(self.request.match_info['adv_id']), self.request['session'])
        return web.json_response({
            "ID": adversi.id,
            "head": adversi.head_adv})
            #"get_time": int(adversi.time_create.timestamp()) стандарт отображения ввремени в секундах принятый.})
    #
    async def post(self):
        user_data = await self.request.json()
        app_adv = Useradven(head_adv=user_data['head_adv'], text_of_adv=user_data['text_of_adv'])
        self.request['session'].add(app_adv)
        try:
            await self.request['session'].commit()
        except:
            raise web.HTTPConflict(
                text=json.dumps({"eror": "little erorrr"}),
                content_type='application/json')
        return web.json_response({"id": app_adv.id})
    #
    async def patch(self):
        adversi = await get_adve(int(self.request.match_info['adv_id']), self.request['session'])
        json_data = await self.request.json()
        for field, value in json_data.items():
            setattr(adversi, field, value)
            self.request['session'].add(adversi)
            await self.request['session'].commit()
        return web.json_response({"status": 'success updated'})
    #
    async def delete(self):
        adversi = await get_adve(int(self.request.match_info['adv_id']), self.request['session'])
        await self.request['session'].delete(adversi)
        await self.request['session'].commit()
        return web.json_response({"status": 'success DELETED'})
#
async def foku(request: web.Request):
    return web.json_response({
        "hiWORLD": "worrld HELLO!"})

if __name__ == '__main__':
    app.add_routes([
        web.get("/", foku),
        web.post("/post", UserView),
        web.get("/get/{adv_id:\d+}", UserView),
        web.patch("/patch/{adv_id:\d+}", UserView),
        web.delete("/delete/{adv_id:\d+}", UserView)
    ])
    #
    web.run_app(app=app, host='127.0.0.3', port=5001)


