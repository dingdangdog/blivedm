# -*- coding: utf-8 -*-
import asyncio
import http.cookies
import random
from typing import *
import aiohttp

import blivedm
import blivedm.models.web as web_models
from readConfig import read_json_config
from pyttsx3Speech import text_to_speech
from azure_tts import azure_tts_speech, init_azure_config

# 直播间ID的取值看直播间URL
session: Optional[aiohttp.ClientSession] = None

PLATFORM: str = 'win'
MODE: str = 'local'
ROOM_IDS: [] = []
SESSDATA: str = ''
HEART_PRINT: int = 10


async def main():
    init_config()
    init_session()
    try:
        await run_single_client()
        await run_multi_clients()
    finally:
        await session.close()


def init_config():
    global PLATFORM
    global MODE
    global ROOM_IDS
    global SESSDATA
    global HEART_PRINT
    config = read_json_config()
    PLATFORM = config['platform']
    MODE = config['mode']
    ROOM_IDS = config['room_ids']
    SESSDATA = config['bilibili_SESSION']
    HEART_PRINT = config['bilibili_heart_print']
    init_azure_config()


def init_session():
    cookies = http.cookies.SimpleCookie()
    cookies['SESSDATA'] = SESSDATA
    cookies['SESSDATA']['domain'] = 'bilibili.com'

    global session
    session = aiohttp.ClientSession()
    session.cookie_jar.update_cookies(cookies)


async def run_single_client():
    """
    监听一个直播间
    """
    room_id = random.choice(ROOM_IDS)
    client = blivedm.BLiveClient(room_id, session=session)
    handler = MyHandler()
    client.set_handler(handler)

    client.start()
    try:
        # 演示5秒后停止
        await asyncio.sleep(5)
        client.stop()

        await client.join()
    finally:
        await client.stop_and_close()


async def run_multi_clients():
    """
    同时监听多个直播间
    """
    clients = [blivedm.BLiveClient(room_id, session=session) for room_id in ROOM_IDS]
    handler = MyHandler()
    for client in clients:
        client.set_handler(handler)
        client.start()

    try:
        await asyncio.gather(*(
            client.join() for client in clients
        ))
    finally:
        await asyncio.gather(*(
            client.stop_and_close() for client in clients
        ))


class MyHandler(blivedm.BaseHandler):  # 类变量，将被所有类的实例共享

    # 心跳监听
    def __init__(self):
        self.heart = HEART_PRINT

    def _on_heartbeat(self, client: blivedm.BLiveClient, message: web_models.HeartbeatMessage):
        if self.heart == HEART_PRINT:
            print(f'[{client.room_id}] 自动心跳检测')
            self.heart = 0
        else:
            self.heart += 1

    # 进入直播间
    def _on_inter(self, client: blivedm.BLiveClient, data: web_models.UserInData):
        print(f'[{client.room_id}] {data.uname} 进入直播间了')
        speech(f'欢迎 {data.uname} 进入直播间，老板常来玩啊！')

    # 弹幕消息
    def _on_danmaku(self, client: blivedm.BLiveClient, message: web_models.DanmakuMessage):
        print(f'[{client.room_id}] {message.uname}：{message.msg}')
        msg = message.msg
        try:
            msg = split_and_reassemble(int(message.msg))
        except (ValueError, TypeError):
            msg = msg
        finally:
            speech(f'{message.uname} 说：{msg}')

    # 特殊弹幕通知
    def _on_spacial_danmaku(self, client: blivedm.BLiveClient, message: web_models.SpacialDanMaku):
        # 使用 for 循环输出 content_segments 中的 text 属性
        for content in message.content_segments:
            print(f'[{content.text}')
            speech(f'{content.text}')

    # 礼物信息
    def _on_gift(self, client: blivedm.BLiveClient, message: web_models.GiftMessage):
        print(f'[{client.room_id}] {message.uname} 赠送{message.gift_name}x{message.num}'
              f' （{message.coin_type}瓜子x{message.total_coin}）')
        speech(f'感谢 {message.uname} 赠送的 {message.num}个 {message.gift_name}，谢谢老板，老板大气！')

    # 舰长？
    def _on_buy_guard(self, client: blivedm.BLiveClient, message: web_models.GuardBuyMessage):
        print(f'[{client.room_id}] {message.username} 购买{message.gift_name}')

    # 点赞消息处理：PS：可能存在并发问题
    def _click_like(self, client: blivedm.BLiveClient, data: web_models.ClickData):
        if len(data.uname) != 0:
            print(f'[{client.room_id}] {data.uname} {data.like_text}')
            speech(f'感谢 {data.uname} {data.like_text}')
        else:
            # 点赞数量更新，本场直播的总点赞数量
            print(f'[{client.room_id}] 本次直播点赞数量达到 {data.click_count} 次')
            speech(f'本次直播点赞数量达到 {data.click_count} 次')

    def _on_super_chat(self, client: blivedm.BLiveClient, message: web_models.SuperChatMessage):
        print(f'[{client.room_id}] 醒目留言 ¥{message.price} {message.uname}：{message.message}')


def split_and_reassemble(number):
    # 将数字转换为字符串
    num_str = str(number)
    # 将每个字符转换为字符串列表
    digits = [char for char in num_str]
    # 重新组装成带逗号的字符串
    result_str = ",".join(digits)
    return result_str


def speech(text):
    if MODE == 'local':
        text_to_speech(text)
    if MODE == 'azure':
        azure_tts_speech(text)


if __name__ == '__main__':
    asyncio.run(main())
