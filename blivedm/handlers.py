# -*- coding: utf-8 -*-
import logging
from typing import *

from .clients import ws_base
from .models import web as web_models, open_live as open_models

__all__ = (
    'HandlerInterface',
    'BaseHandler',
)

logger = logging.getLogger('blivedm')

logged_unknown_cmds = {
    'PLAYTOGETHER_ICON_CHANGE', # 图标变更？ command={'cmd': 'PLAYTOGETHER_ICON_CHANGE', 'data': {'area_id': 236, 'has_perm': 0, 'show_count': 0}}
    'AREA_RANK_CHANGED', # command={'cmd': 'AREA_RANK_CHANGED', 'data': {'conf_id': 21, 'rank_name': '单机航海', 'uid': 412847209, 'rank': 0, 'icon_url_blue': 'https://i0.hdslb.com/bfs/live/18e2990a546d33368200f9058f3d9dbc4038eb5c.png', 'icon_url_pink': 'https://i0.hdslb.com/bfs/live/a6c490c36e88c7b191a04883a5ec15aed187a8f7.png', 'icon_url_grey': 'https://i0.hdslb.com/bfs/live/cb7444b1faf1d785df6265bfdc1fcfc993419b76.png', 'action_type': 1, 'timestamp': 1706182633, 'msg_id': 'f639198e-80f1-4bf1-bc43-866efcfb711a', 'jump_url_link': 'https://live.bilibili.com/p/html/live-app-hotrank/index.html?clientType=3&ruid=412847209&conf_id=21&is_live_half_webview=1&hybrid_rotate_d=1&is_cling_player=1&hybrid_half_ui=1,3,100p,70p,f4eefa,0,30,100,0,0;2,2,375,100p,f4eefa,0,30,100,0,0;3,3,100p,70p,f4eefa,0,30,100,0,0;4,2,375,100p,f4eefa,0,30,100,0,0;5,3,100p,70p,f4eefa,0,30,100,0,0;6,3,100p,70p,f4eefa,0,30,100,0,0;7,3,100p,70p,f4eefa,0,30,100,0,0;8,3,100p,70p,f4eefa,0,30,100,0,0#/area-rank', 'jump_url_pc': 'https://live.bilibili.com/p/html/live-app-hotrank/index.html?clientType=4&ruid=412847209&conf_id=21&pc_ui=338,465,f4eefa,0#/area-rank', 'jump_url_pink': 'https://live.bilibili.com/p/html/live-app-hotrank/index.html?clientType=1&ruid=412847209&conf_id=21&is_live_half_webview=1&hybrid_rotate_d=1&hybrid_half_ui=1,3,100p,70p,ffffff,0,30,100,12,0;2,2,375,100p,ffffff,0,30,100,0,0;3,3,100p,70p,ffffff,0,30,100,12,0;4,2,375,100p,ffffff,0,30,100,0,0;5,3,100p,70p,ffffff,0,30,100,0,0;6,3,100p,70p,ffffff,0,30,100,0,0;7,3,100p,70p,ffffff,0,30,100,0,0;8,3,100p,70p,ffffff,0,30,100,0,0#/area-rank', 'jump_url_web': 'https://live.bilibili.com/p/html/live-app-hotrank/index.html?clientType=2&ruid=412847209&conf_id=21#/area-rank'}}
    'ANCHOR_HELPER_DANMU', # 直播小助手 command={'cmd': 'ANCHOR_HELPER_DANMU', 'data': {'sender': '直播小助手', 'msg': '开播获得100个弹幕！邀请观众连麦互动，直播间氛围更活跃哦', 'platform': 1, 'button_platform': 3, 'button_name': '去连麦', 'button_target': 'bililive://blink/open_voicelink', 'button_label': 0, 'report_type': 'milestone', 'report': 'session_danmu:6:100'}}
    'ANCHOR_BROADCAST', # 直播小助手 command={'cmd': 'ANCHOR_BROADCAST', 'data': {'sender': '直播小助手', 'msg': '开播获得100个弹幕！邀请观众连麦互动，直播间氛围更活跃哦', 'platform': 1, 'button_info': {'button_name': '去连麦', 'blink_button_type': '', 'blink_button_target': '', 'blink_button_extra': '', 'blink_button_label': 0, 'hime_button_type': 'panel', 'hime_button_target': '1000', 'hime_button_extra': '', 'hime_button_h5_type': '0', 'hime_button_label': 0}, 'milestone_type': 'session_danmu', 'milestone_value': 100, 'milestone_index': 6}}
    'COMBO_SEND',
    'COMBO_END', # command={'cmd': 'COMBO_END', 'data': {'uid': 3494366419093890, 'ruid': 412847209, 'uname': 'thuGreth', 'r_uname': '老狗自闭', 'combo_num': 1, 'gift_id': 31164, 'gift_num': 1, 'batch_combo_num': 1, 'gift_name': '粉丝团灯牌', 'action': '投喂', 'send_master': None, 'price': 1000, 'start_time': 1706173240, 'end_time': 1706173240, 'guard_level': 0, 'name_color': '', 'combo_total_coin': 1000, 'coin_type': 'gold', 'is_mystery': False}}
    # 'COMMON_NOTICE_DANMAKU', # 特殊通知弹幕 command={'cmd': 'COMMON_NOTICE_DANMAKU', 'data': {'terminals': [4, 5], 'content_segments': [{'type': 1, 'font_color': '#61666d', 'font_color_dark': '#a2a7ae', 'text': '恭喜 <%thuGreth%> 成为 <%小花花%> 星球守护者~', 'highlight_font_color': '#FFB027', 'highlight_font_color_dark': '#FFB027'}]}}
    'WATCHED_CHANGE', # 直播观看数量改变触发？ command={'cmd': 'WATCHED_CHANGE', 'data': {'num': 14, 'text_small': '14', 'text_large': '14人看过'}}
    'ENTRY_EFFECT', # 进入直播间？？command={'cmd': 'ENTRY_EFFECT', 'data': {'id': 136, 'uid': 412847209, 'target_id': 412847209, 'mock_effect': 0, 'face': 'https://i1.hdslb.com/bfs/face/759f1c2cd63246dc2ac321186cf532579c18ca5a.jpg', 'privilege_type': 0, 'copy_writing': '欢迎 <%老狗自闭%> 进入直播间', 'copy_color': '#000000', 'highlight_color': '#FFF100', 'priority': 1, 'basemap_url': 'https://i0.hdslb.com/bfs/live/mlive/d4708dee21646e6ebcc58e7f6fa2a972c1d25b36.png', 'show_avatar': 1, 'effective_time': 2, 'web_basemap_url': 'https://i0.hdslb.com/bfs/live/mlive/d4708dee21646e6ebcc58e7f6fa2a972c1d25b36.png', 'web_effective_time': 2, 'web_effect_close': 0, 'web_close_time': 900, 'business': 3, 'copy_writing_v2': '欢迎 <^icon^> <%老狗自闭%> 进入直播间', 'icon_list': [2], 'max_delay_time': 7, 'trigger_time': 1706285079362789984, 'identities': 22, 'effect_silent_time': 0, 'effective_time_new': 0, 'web_dynamic_url_webp': '', 'web_dynamic_url_apng': '', 'mobile_dynamic_url_webp': '', 'wealthy_info': None, 'new_style': 0, 'is_mystery': False, 'uinfo': {'uid': 412847209, 'base': {'name': '老狗自闭', 'face': 'https://i1.hdslb.com/bfs/face/759f1c2cd63246dc2ac321186cf532579c18ca5a.jpg', 'name_color': 0, 'is_mystery': False, 'risk_ctrl_info': {'name': '老狗自闭', 'face': 'https://i1.hdslb.com/bfs/face/759f1c2cd63246dc2ac321186cf532579c18ca5a.jpg'}, 'origin_info': {'name': '老狗自闭', 'face': 'https://i1.hdslb.com/bfs/face/759f1c2cd63246dc2ac321186cf532579c18ca5a.jpg'}, 'official_info': {'role': 0, 'title': '', 'desc': '', 'type': -1}}, 'medal': None, 'wealth': None, 'title': None, 'guard': None, 'uhead_frame': None, 'guard_leader': None}}}
    # 'HOT_RANK_CHANGED', # 热榜排名变更？
    # 'HOT_RANK_CHANGED_V2', # 热榜排名变更？
    # 'INTERACT_WORD', # 进入直播间 command={'cmd': 'INTERACT_WORD', 'data': {'contribution': {'grade': 3}, 'contribution_v2': {'grade': 2, 'rank_type': 'monthly_rank', 'text': '月榜前3用户'}, 'core_user_type': 0, 'dmscore': 28, 'fans_medal': {'anchor_roomid': 0, 'guard_level': 0, 'icon_id': 0, 'is_lighted': 0, 'medal_color': 0, 'medal_color_border': 0, 'medal_color_end': 0, 'medal_color_start': 0, 'medal_level': 0, 'medal_name': '', 'score': 0, 'special': '', 'target_id': 0}, 'group_medal': None, 'identities': [1], 'is_mystery': False, 'is_spread': 0, 'msg_type': 1, 'privilege_type': 0, 'roomid': 30886597, 'score': 1706174295693, 'spread_desc': '', 'spread_info': '', 'tail_icon': 0, 'tail_text': '', 'timestamp': 1706174295, 'trigger_time': 1706174294633680000, 'uid': 90383004, 'uinfo': {'base': {'face': 'https://i0.hdslb.com/bfs/face/a3720664af7a993fc45ce48f190d02913d1f2c85.jpg', 'is_mystery': False, 'name': '月上小狗', 'name_color': 0, 'official_info': {'desc': '', 'role': 0, 'title': '', 'type': -1}, 'origin_info': {'face': 'https://i0.hdslb.com/bfs/face/a3720664af7a993fc45ce48f190d02913d1f2c85.jpg', 'name': '月上小狗'}, 'risk_ctrl_info': {'face': 'https://i0.hdslb.com/bfs/face/a3720664af7a993fc45ce48f190d02913d1f2c85.jpg', 'name': '月上小狗'}}, 'guard': None, 'guard_leader': None, 'medal': None, 'title': None, 'uhead_frame': None, 'uid': 90383004, 'wealth': None}, 'uname': '月上小狗', 'uname_color': ''}}
    'LIVE',
    'LIVE_INTERACTIVE_GAME',
    'NOTICE_MSG',
    'ONLINE_RANK_COUNT',
    'ONLINE_RANK_TOP3',
    'ONLINE_RANK_V2',
    # 'PK_BATTLE_END',
    # 'PK_BATTLE_FINAL_PROCESS',
    # 'PK_BATTLE_PROCESS',
    # 'PK_BATTLE_PROCESS_NEW',
    # 'PK_BATTLE_SETTLE',
    # 'PK_BATTLE_SETTLE_USER',
    # 'PK_BATTLE_SETTLE_V2',
    # 'PREPARING',
    # 'ROOM_REAL_TIME_MESSAGE_UPDATE',
    # 'STOP_LIVE_ROOM_LIST',
    # 'SUPER_CHAT_MESSAGE_JPN',
    # 'WIDGET_BANNER', # 小部件横幅？
    'GUARD_HONOR_THOUSAND', # 横幅消息？command={'cmd': 'GUARD_HONOR_THOUSAND', 'data': {'add': [], 'del': [1900141897, 1778026586, 1459104794, 672328094, 480680646, 412504829, 401315430, 399815233, 304578055, 194484313, 56748733, 10893225, 8739477, 686127, 391445, 114866, 13046]}}
    'STOP_LIVE_ROOM_LIST', # 停止直播房间通知？command={'cmd': 'STOP_LIVE_ROOM_LIST', 'data': {'room_id_list': [26134056, 27733015, 30241196, 3111310, 31210096, 31633765, 583957, 132630, 13605776, 1878685, 22254974, 26347978, 26646310, 30131067, 31043525, 31883577, 9068894, 21473355, 22376685, 22479025, 23072802, 23692844, 26364316, 27183535, 30908405, 31183446, 31412845, 31599685, 346947, 5581190, 714445, 11948353, 21602575, 2175284, 24840855, 27205276, 31002575, 31745517, 31814106, 31822065, 3406491, 5466700, 14808633, 24362801, 26193324, 27617835, 2851255, 30230515, 31309055, 31572045, 31792466, 31844625, 31883095, 31883446, 4329180, 13407895, 23776755, 25857732, 27568487, 27822717, 31583737, 31883513, 5473867, 9488965, 11853957, 24590414, 27566417, 30563397, 31061877, 31570617, 31583726, 31765226, 3436197, 13934740, 2044107, 25270307, 26914407, 27816937, 30241167, 5556097, 26320860, 269655, 27183177, 27777747, 27880760, 2826764, 30637667, 31049780, 31535426, 2283471, 24797968, 27907920, 30524453, 31146690, 31207910, 31542580, 31764770, 31782448, 2065784, 23534120, 24909030, 26914140, 27778610, 30184630, 30911422, 31354446, 31693750, 31710427, 6627923, 9056564, 14920605, 25431380, 30198500, 30382320, 31313400, 31672956, 8437310, 1758371, 23361799, 22504516, 22886883, 23387005, 30098122, 23747371, 508371, 5612200, 8287300, 10422640, 11644391, 25674182, 2695765, 27771538, 30007971, 5126047, 9318162, 12487527, 14643888, 21075066, 22841601, 22898134, 10485486, 26860584, 27149142, 31497643, 15106058, 26656064, 27930777, 31379695, 4261325, 12066164, 21441782, 25424943, 27878493, 27962953, 30961365, 31819604, 6159041, 8892113, 13817334, 22598619, 30193671, 31675309, 26843755, 26998825, 30911742, 806038, 25114227, 30970679, 24369111, 25674623, 264110, 31311768, 31727993, 5334517, 63258, 150596, 22717970, 22730263, 25674511, 31619124, 31871974, 363485, 23530960, 24228718, 30339892, 31100672, 1366096, 27633961, 2847091, 6806182, 26209819, 2708384, 27487787, 30394118, 31587278, 31615570, 12216533, 14982610, 2398772, 26049768, 26079169, 26548927, 30301316, 30339901, 30636547, 11633159, 23570440]}}
    'ENTRY_EFFECT_MUST_RECEIVE', # 空房间？command={'cmd': 'ENTRY_EFFECT_MUST_RECEIVE', 'data': {'id': 136, 'uid': 412847209, 'target_id': 412847209, 'mock_effect': 0, 'face': 'https://i1.hdslb.com/bfs/face/759f1c2cd63246dc2ac321186cf532579c18ca5a.jpg', 'privilege_type': 0, 'copy_writing': '欢迎 <%老狗自闭%> 进入直播间', 'copy_color': '#000000', 'highlight_color': '#FFF100', 'priority': 1, 'basemap_url': 'https://i0.hdslb.com/bfs/live/mlive/d4708dee21646e6ebcc58e7f6fa2a972c1d25b36.png', 'show_avatar': 1, 'effective_time': 2, 'web_basemap_url': 'https://i0.hdslb.com/bfs/live/mlive/d4708dee21646e6ebcc58e7f6fa2a972c1d25b36.png', 'web_effective_time': 2, 'web_effect_close': 0, 'web_close_time': 900, 'business': 3, 'copy_writing_v2': '欢迎 <^icon^> <%老狗自闭%> 进入直播间', 'icon_list': [2], 'max_delay_time': 7, 'trigger_time': 1706283359662552605, 'identities': 22, 'effect_silent_time': 0, 'effective_time_new': 0, 'web_dynamic_url_webp': '', 'web_dynamic_url_apng': '', 'mobile_dynamic_url_webp': '', 'wealthy_info': None, 'new_style': 0, 'is_mystery': False, 'uinfo': {'uid': 412847209, 'base': {'name': '老狗自闭', 'face': 'https://i1.hdslb.com/bfs/face/759f1c2cd63246dc2ac321186cf532579c18ca5a.jpg', 'name_color': 0, 'is_mystery': False, 'risk_ctrl_info': {'name': '老狗自闭', 'face': 'https://i1.hdslb.com/bfs/face/759f1c2cd63246dc2ac321186cf532579c18ca5a.jpg'}, 'origin_info': {'name': '老狗自闭', 'face': 'https://i1.hdslb.com/bfs/face/759f1c2cd63246dc2ac321186cf532579c18ca5a.jpg'}, 'official_info': {'role': 0, 'title': '', 'desc': '', 'type': -1}}, 'medal': None, 'wealth': None, 'title': None, 'guard': None, 'uhead_frame': None, 'guard_leader': None}}}
    'ROOM_CHANGE', # 关闭直播？ command={'cmd': 'ROOM_CHANGE', 'data': {'title': '裸辞直播：今天研究一下B站弹幕姬', 'area_id': 372, 'parent_area_id': 11, 'area_name': '校园学习', 'parent_area_name': '知识', 'live_key': '0', 'sub_session_key': ''}}
    'TRADING_SCORE', # command={'cmd': 'TRADING_SCORE', 'data': {'bubble_show_time': 3, 'num': 2, 'score_id': 3, 'uid': 412847209, 'update_time': 1706173741, 'update_type': 1}}
    'SPREAD_ORDER_START', # command={'cmd': 'SPREAD_ORDER_START', 'data': {'order_id': 5862464, 'order_status': 1, 'roomid': 30886597, 'timestamp': 1706173750, 'uid': 412847209}}
    'SPREAD_ORDER_OVER', # command={'cmd': 'SPREAD_ORDER_OVER', 'data': {'order_id': 5862464, 'order_status': 0, 'timestamp': 1706175599, 'uid': 412847209}}
    'SPREAD_SHOW_FEET', # 修改直播组件事件触发 command={'cmd': 'SPREAD_SHOW_FEET', 'data': {'click': 0, 'coin_cost': 0, 'coin_num': 5, 'order_id': 5862464, 'plan_percent': 0, 'show': 1, 'timestamp': 1706173762, 'title': '流量包推广', 'total_online': 0, 'uid': 412847209}}
    'SPREAD_SHOW_FEET_V2', # command={'cmd': 'SPREAD_SHOW_FEET_V2', 'data': {'click': 0, 'coin_cost': 0, 'coin_num': 5, 'cover_btn': '', 'cover_url': '', 'live_key': '459756646836947653', 'order_id': 5862464, 'order_type': 3, 'plan_percent': 0, 'show': 1, 'status': 1, 'timestamp': 1706173762, 'title': '流量包推广', 'total_online': 0, 'uid': 412847209}}
}
"""已打日志的未知cmd"""


class HandlerInterface:
    """
    直播消息处理器接口
    """

    def handle(self, client: ws_base.WebSocketClientBase, command: dict):
        raise NotImplementedError

    def on_client_stopped(self, client: ws_base.WebSocketClientBase, exception: Optional[Exception]):
        """
        当客户端停止时调用。可以在这里close或者重新start
        """


def _make_msg_callback(method_name, message_cls):
    def callback(self: 'BaseHandler', client: ws_base.WebSocketClientBase, command: dict):
        method = getattr(self, method_name)
        return method(client, message_cls.from_command(command['data']))
    return callback


class BaseHandler(HandlerInterface):
    """
    一个简单的消息处理器实现，带消息分发和消息类型转换。继承并重写_on_xxx方法即可实现自己的处理器
    """

    def __danmu_msg_callback(self, client: ws_base.WebSocketClientBase, command: dict):
        return self._on_danmaku(client, web_models.DanmakuMessage.from_command(command['info']))

    _CMD_CALLBACK_DICT: Dict[
        str,
        Optional[Callable[
            ['BaseHandler', ws_base.WebSocketClientBase, dict],
            Any
        ]]
    ] = {
        # 收到心跳包，这是blivedm自造的消息，原本的心跳包格式不一样
        '_HEARTBEAT': _make_msg_callback('_on_heartbeat', web_models.HeartbeatMessage),
        # 'ENTRY_EFFECT':
        # 收到弹幕
        # go-common\app\service\live\live-dm\service\v1\send.go
        'DANMU_MSG': __danmu_msg_callback,
        # 有人送礼
        'SEND_GIFT': _make_msg_callback('_on_gift', web_models.GiftMessage),
        # 特殊弹幕通知
        # 'COMMON_NOTICE_DANMAKU': _make_msg_callback('_on_spacial_danmaku', web_models.SpacialDanMaku),
        # 进入直播间
        'INTERACT_WORD': _make_msg_callback('_on_inter', web_models.UserInData),
        # 有人上舰
        'GUARD_BUY': _make_msg_callback('_on_buy_guard', web_models.GuardBuyMessage),
        # 醒目留言
        'SUPER_CHAT_MESSAGE': _make_msg_callback('_on_super_chat', web_models.SuperChatMessage),
        # 删除醒目留言
        'SUPER_CHAT_MESSAGE_DELETE': _make_msg_callback('_on_super_chat_delete', web_models.SuperChatDeleteMessage),
        # 点赞开始触发：command={'cmd': 'LIKE_INFO_V3_CLICK', 'data': {'show_area': 1, 'msg_type': 6, 'like_icon': 'https://i0.hdslb.com/bfs/live/23678e3d90402bea6a65251b3e728044c21b1f0f.png', 'uid': 90383004, 'like_text': '为主播点赞了', 'uname': '月上小狗', 'uname_color': '', 'identities': [1], 'fans_medal': {'target_id': 0, 'medal_level': 0, 'medal_name': '', 'medal_color': 0, 'medal_color_start': 12632256, 'medal_color_end': 12632256, 'medal_color_border': 12632256, 'is_lighted': 0, 'guard_level': 0, 'special': '', 'icon_id': 0, 'anchor_roomid': 0, 'score': 0}, 'contribution_info': {'grade': 0}, 'dmscore': 20, 'group_medal': None, 'is_mystery': False, 'uinfo': {'uid': 90383004, 'base': {'name': '月上小狗', 'face': 'https://i0.hdslb.com/bfs/face/a3720664af7a993fc45ce48f190d02913d1f2c85.jpg', 'name_color': 0, 'is_mystery': False, 'risk_ctrl_info': None, 'origin_info': {'name': '月上小狗', 'face': 'https://i0.hdslb.com/bfs/face/a3720664af7a993fc45ce48f190d02913d1f2c85.jpg'}, 'official_info': {'role': 0, 'title': '', 'desc': '', 'type': -1}}, 'medal': None, 'wealth': None, 'title': None, 'guard': {'level': 0, 'expired_str': ''}}}}
        'LIKE_INFO_V3_CLICK': _make_msg_callback('_click_like', web_models.ClickData),
        # 点赞结束触发：command = {'cmd': 'LIKE_INFO_V3_UPDATE', 'data': {'click_count': 171}}  应该是该点赞观众在本次直播中的汇总次数，不分时间
        'LIKE_INFO_V3_UPDATE': _make_msg_callback('_click_like', web_models.ClickData),

        #
        # 开放平台消息
        #

        # 收到弹幕
        'LIVE_OPEN_PLATFORM_DM': _make_msg_callback('_on_open_live_danmaku', open_models.DanmakuMessage),
        # 有人送礼
        'LIVE_OPEN_PLATFORM_SEND_GIFT': _make_msg_callback('_on_open_live_gift', open_models.GiftMessage),
        # 有人上舰
        'LIVE_OPEN_PLATFORM_GUARD': _make_msg_callback('_on_open_live_buy_guard', open_models.GuardBuyMessage),
        # 醒目留言
        'LIVE_OPEN_PLATFORM_SUPER_CHAT': _make_msg_callback('_on_open_live_super_chat', open_models.SuperChatMessage),
        # 删除醒目留言
        'LIVE_OPEN_PLATFORM_SUPER_CHAT_DEL': _make_msg_callback(
            '_on_open_live_super_chat_delete', open_models.SuperChatDeleteMessage
        ),
        # 点赞
        'LIVE_OPEN_PLATFORM_LIKE': _make_msg_callback('_on_open_live_like', open_models.LikeMessage),
    }
    """cmd -> 处理回调"""

    def handle(self, client: ws_base.WebSocketClientBase, command: dict):
        cmd = command.get('cmd', '')
        pos = cmd.find(':')  # 2019-5-29 B站弹幕升级新增了参数
        if pos != -1:
            cmd = cmd[:pos]

        if cmd not in self._CMD_CALLBACK_DICT:
            # 只有第一次遇到未知cmd时打日志
            if cmd not in logged_unknown_cmds:
                logger.warning('room=%d unknown cmd=%s, command=%s', client.room_id, cmd, command)
                logged_unknown_cmds.add(cmd)
            return

        callback = self._CMD_CALLBACK_DICT[cmd]
        if callback is not None:
            callback(self, client, command)

    def _on_heartbeat(self, client: ws_base.WebSocketClientBase, message: web_models.HeartbeatMessage):
        """
        收到心跳包
        """

    def _on_danmaku(self, client: ws_base.WebSocketClientBase, message: web_models.DanmakuMessage):
        """
        收到弹幕
        """

    def _on_gift(self, client: ws_base.WebSocketClientBase, message: web_models.GiftMessage):
        """
        收到礼物
        """

    def _on_buy_guard(self, client: ws_base.WebSocketClientBase, message: web_models.GuardBuyMessage):
        """
        有人上舰
        """

    def _on_super_chat(self, client: ws_base.WebSocketClientBase, message: web_models.SuperChatMessage):
        """
        醒目留言
        """

    def _on_super_chat_delete(
        self, client: ws_base.WebSocketClientBase, message: web_models.SuperChatDeleteMessage
    ):
        """
        删除醒目留言
        """

    #
    # 开放平台消息
    #

    def _on_open_live_danmaku(self, client: ws_base.WebSocketClientBase, message: open_models.DanmakuMessage):
        """
        收到弹幕
        """

    def _on_open_live_gift(self, client: ws_base.WebSocketClientBase, message: open_models.GiftMessage):
        """
        收到礼物
        """

    def _on_open_live_buy_guard(self, client: ws_base.WebSocketClientBase, message: open_models.GuardBuyMessage):
        """
        有人上舰
        """

    def _on_open_live_super_chat(
        self, client: ws_base.WebSocketClientBase, message: open_models.SuperChatMessage
    ):
        """
        醒目留言
        """

    def _on_open_live_super_chat_delete(
        self, client: ws_base.WebSocketClientBase, message: open_models.SuperChatDeleteMessage
    ):
        """
        删除醒目留言
        """

    def _on_open_live_like(self, client: ws_base.WebSocketClientBase, message: open_models.LikeMessage):
        """
        点赞
        """
