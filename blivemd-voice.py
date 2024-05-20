# -*- coding: utf-8 -*-
import asyncio
import http.cookies
import random
import threading
from queue import Queue
from typing import *
import aiohttp
import time

import blivedm
import blivedm.models.web as web_models
from readConfig import read_json_config
from speech_pyttsx3 import text_to_speech
from speech_azure import azure_tts_speech, init_azure_config
from speech_alibaba import alibaba_tts_speech, init_alibaba_config
from speech_sovits import sovits_tts_speech, init_sovits_config

# 直播间ID的取值看直播间URL
session: Optional[aiohttp.ClientSession] = None

PLATFORM: str = 'win'
MODE: str = 'local'
ROOM_IDS: [] = []
SESSDATA: str = ''
HEART_PRINT: int = 10
GIFT_INTERVAL: int = 1
VOICE_TEXT: {} = {}
LIKE_NUMS: [] = [100, 500, 666, 1000]
LIKE_NEXT_INTERVAL: int = 100
WELCOME_LEVEL: int = 0


async def main():
    init_config()
    init_session()
    text = f'语音机器人启动成功，监控直播间：{ROOM_IDS}，语音模式：{MODE}，心跳间隔：{HEART_PRINT}，连续礼物间隔：{GIFT_INTERVAL}'
    print(text)
    speech(text)
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
    global GIFT_INTERVAL
    global VOICE_TEXT
    global LIKE_NUMS
    global LIKE_NEXT_INTERVAL
    global WELCOME_LEVEL
    config = read_json_config("config.json")
    PLATFORM = config['platform']
    MODE = config['mode']
    ROOM_IDS = config['room_ids']
    SESSDATA = config['bilibili_SESSION']
    HEART_PRINT = config['bilibili_heart_print']
    GIFT_INTERVAL = config['continuous_gift_interval']
    VOICE_TEXT = config['voice_text']
    LIKE_NUMS = config['like_nums']
    LIKE_NEXT_INTERVAL = config['max_next_interval']
    WELCOME_LEVEL = config['welcome_level']
    if MODE == 'azure':
        init_azure_config()
    if MODE == 'alibaba':
        init_alibaba_config()
    if MODE == 'sovits':
        init_sovits_config()


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
        self.gift_interval = GIFT_INTERVAL
        self.gift_queue = Queue()  # 创建一个队列用于存储礼物信息
        self.last_queue_size = 0  # 用于记录上一次队列的大小
        self.gift_thread = threading.Thread(target=self.gift_listen)  # 创建一个线程用于处理礼物信息
        self.gift_thread.start()  # 启动处理礼物信息的线程
        self.last_click_like_num = 0  # 点赞总数
        self.last_click_like_index = 0  # 最后点赞语音提示的数量索引

    def _on_heartbeat(self, client: blivedm.BLiveClient, message: web_models.HeartbeatMessage):
        if self.heart == HEART_PRINT:
            self.heart = 0
            print(f'[{client.room_id}] 自动心跳检测')
        else:
            self.heart += 1

    # 进入直播间
    def _on_enter(self, client: blivedm.BLiveClient, data: web_models.UserInData):
        if data.medal_level >= WELCOME_LEVEL:
            print(f' {data.uname} 进入直播间了')
            voice_text = VOICE_TEXT["enter"].format(uname=data.uname)
            speech(voice_text)

    # 弹幕消息
    def _on_danmaku(self, client: blivedm.BLiveClient, message: web_models.DanmakuMessage):
        print(f' {message.uname}：{message.msg}')
        msg = message.msg
        try:
            msg = split_and_reassemble(int(message.msg))
        except (ValueError, TypeError):
            msg = msg
        finally:
            voice_text = VOICE_TEXT["danmaku"].format(uname=message.uname, msg=msg)
            speech(voice_text)

    # 特殊弹幕通知
    def _on_spacial_danmaku(self, client: blivedm.BLiveClient, message: web_models.SpacialDanMaku):
        # 使用 for 循环输出 content_segments 中的 text 属性
        for content in message.content_segments:
            print(f'[{content.text}')
            speech(f'{content.text}')

    # 红包礼物信息
    def _on_red_pocket(self, client: blivedm.BLiveClient, message: web_models.GiftMessage):
        # 执行相应的逻辑
        print(f' {message.uname} 赠送 {message.gift_name}x{message.num}'
              f' （价值x{message.price}）')

        voice_text = VOICE_TEXT["gift"].format(uname=message.uname, num=message.num,
                                               gift_name=message.gift_name)
        speech(voice_text)

    # 礼物信息
    def _on_gift(self, client: blivedm.BLiveClient, message: web_models.GiftMessage):
        self.gift_queue.put(message)

    def gift_listen(self):
        while True:
            current_queue_size = self.gift_queue.qsize()
            if current_queue_size > 0 and current_queue_size != self.last_queue_size:
                # 如果队列有变动，则等待2秒
                time.sleep(self.gift_interval)
            else:
                # 如果队列没有变动，则执行逻辑
                messages = []
                while not self.gift_queue.empty():
                    messages.append(self.gift_queue.get())
                if messages:
                    total = {}
                    for message in messages:
                        # 汇总请求参数
                        if message.uname in total and total[message.uname].gift_name == message.gift_name:
                            total[message.uname].num += message.num
                            total[message.uname].total_coin += message.total_coin
                        else:
                            total[message.uname] = message
                    for uname, message in total.items():
                        # print(f'用户名: {uname}, 礼物名称: {message.gift_name}, 数量: {message.num}')

                        # 执行相应的逻辑
                        print(f' {uname} 赠送 {message.gift_name}x{message.num}'
                              f' （{message.coin_type}瓜子x{message.total_coin}）')

                        voice_text = VOICE_TEXT["gift"].format(uname=uname, num=message.num,
                                                               gift_name=message.gift_name)
                        speech(voice_text)
                # 清空队列
                self.gift_queue.queue.clear()
            # 更新上一次队列的大小
            self.last_queue_size = current_queue_size

    # 舰长？
    def _on_buy_guard(self, client: blivedm.BLiveClient, message: web_models.GuardBuyMessage):
        print(f' {message.username} 购买 {message.gift_name}')

    # 点赞消息处理：PS：可能存在并发问题
    def _click_like(self, client: blivedm.BLiveClient, data: web_models.ClickData):
        if len(data.uname) != 0:
            print(f' {data.uname} {data.like_text}')
            voice_text = VOICE_TEXT["like"].format(uname=data.uname, like_text=data.like_text)
            speech(voice_text)
        else:
            if LIKE_NUMS[0] > data.click_count:
                return

            index = len(LIKE_NUMS) - 1

            # 先判断是否超过最大值，避免无效循环
            if data.click_count > LIKE_NUMS[index] and data.click_count - self.last_click_like_num > 100:
                if self.last_click_like_num < LIKE_NUMS[index - 1]:
                    # 首次超过设置的最大值。特殊播报
                    self.last_click_like_num = data.click_count
                    text = f' 太棒了！本次直播点赞数量超过设定最大值 {LIKE_NUMS[len(LIKE_NUMS) - 1]} 次，达到 {data.click_count} 次'
                    print(text)
                    speech(text)
                else:
                    # 后续超过最大值后，按照上次播报后的数量100递增提示，每超过100次播报一次。
                    # 如：上一次播报的是1909次，则下次将会在超过2009次时播报，否则不播报
                    self.last_click_like_num = data.click_count + LIKE_NEXT_INTERVAL
                    # 点赞数量更新，本场直播的总点赞数量
                    text = f' 点赞数量达到 {data.click_count} 次'
                    print(text)
                    speech(text)
                return

            while True:
                if index > 0 and LIKE_NUMS[index] > data.click_count > LIKE_NUMS[index - 1]:
                    if self.last_click_like_index == index - 1:
                        return
                    self.last_click_like_num = LIKE_NUMS[index - 1]
                    self.last_click_like_index = index - 1
                    # 点赞数量更新，本场直播的总点赞数量
                    print(f' 本次直播点赞数量超过 {LIKE_NUMS[index - 1]} 次，达到 {data.click_count} 次')
                    voice_text = VOICE_TEXT["like_total"].format(limit_num=LIKE_NUMS[index - 1],
                                                                 click_count=data.click_count)
                    speech(voice_text)
                    return
                elif index <= 0:
                    break
                index -= 1

    def _on_super_chat(self, client: blivedm.BLiveClient, message: web_models.SuperChatMessage):
        print(f' 醒目留言 ¥{message.price} {message.uname}：{message.message}')


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
    if MODE == 'alibaba':
        alibaba_tts_speech(text)
    if MODE == 'sovits':
        sovits_tts_speech(text)


if __name__ == '__main__':
    asyncio.run(main())
