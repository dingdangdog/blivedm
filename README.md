# blivedm-voice

Fork Form：[blivedm](https://github.com/xfgryujk/blivedm)

## package

执行 `pip install pyinstaller` 安装 `pyinstaller`，然后执行下面的打包脚本：

Execute `pip install pyinstaller` to install `pyinstaller`, and then execute the following packaging script:

```shell
# pyinstaller --onefile blivemd-voice.py

# windows azure
# pyinstaller --onefile --add-data "./.venv/Lib/site-packages/azure;azure" blivemd-voice.py

pyinstaller --onefile --add-data "C:/Users/ddd/AppData/Roaming/Python/Python310/site-packages/azure;azure" blivemd-voice.py
```

## config

文件名：`config.json`，该配置文件负责系统主要行为的配置，包括弹幕/礼物/点赞等语音控制。

基本参数配置教程可前往B站观看视频：[B站直播弹幕语音播报机器人-使用教程](https://www.bilibili.com/video/BV1St421b7Ht/)

最新版默认配置如下：

```json
{
  "platform":"win",
  "mode":"local",
  "room_ids":[],
  "bilibili_SESSION":"",
  "bilibili_heart_print": 10,
  "continuous_gift_interval": 1,
  "welcome_level": 0,
  "voice_text": {
    "enter": "欢迎 {uname} 进入直播间，记得常来玩哦！",
    "danmaku": "{uname}说：{msg}",
    "gift": "感谢 {uname} 赠送的 {num}个{gift_name}，谢谢老板，老板大气！",
    "like": "感谢 {uname} {like_text}",
    "like_total": "本次直播点赞数量超过 {limit_num} 次，达到 {click_count} 次"
  },
  "like_nums": [66, 188, 300, 500, 666, 888, 999, 1666],
  "max_next_interval": 100,
  "black_user": ["屏蔽用户1", "屏蔽用户2"],
  "black_text": ["屏蔽词1", "屏蔽词2"]
}
```

### 基本配置说明

1. `platform`：目前仅支持windows。win
2. `mode`：可选配置（select）: local (`default`)/azure/alibaba/sovits
3. `bilibili_SESSION`：这里应该写一个已登录的`SESSDATA`，你可以在浏览器`cookie`中获取它。不填写也可以连接，但是不会获取用户名和id。
4. `bilibili_heart_print`：心跳监听输出间隔，默认值：`10`。
5. `welcome_level`：用户粉丝牌等级， 默认值：`0`。作用：进场提示音等级控制，粉丝牌大于等于指定等级的用户进入房间，才会用欢迎语音和弹幕提示。
6. `continuous_gift_interval`：秒，默认值：`1`。作用：用于配置连续礼物的时间间隔，时间间隔内的相同礼物将会合并播报。
7. `voice_text`：用于配置常用的语音文本。    默认配置（default）：

    ```json
    {
        "enter": "欢迎 {uname} 进入直播间，记得常来玩哦！",
        "danmaku": "{uname}说：{msg}",
        "gift": "感谢 {uname} 赠送的 {num}个{gift_name}，谢谢老板，老板大气！",
        "like": "感谢 {uname} {like_text}",
        "like_total": "本次直播点赞数量达到 {click_count} 次"
    }
    ```

    详细说明：

    - `enter`：进入直播间的语音文字，`uname` 会自动替换为用户昵称；
    - `danmaku`：弹幕播报的语音文字，`uname`-用户昵称、`msg`-弹幕内容；
    - `gift`：礼物播报的语音文字，`uname`-用户昵称、`num`-礼物个数、`gift_name`-礼物名称；
    - `like`：用户点赞的语音文字，`uname`-用户昵称、`like_text`-B站官方点赞提示文字；
    - `like_total`：点赞总结的语音文字，`click_count`-总点赞次数。

8. `like_nums`：点赞数量数组，默认值：`[66, 188, 300, 500, 666, 888, 999, 1666]`。作用：指定需要语音播报的点赞数量，当低于最小值时，语音不会做任何播报。
9. `max_next_interval`：点赞超过上限后的递增数量，默认值：`100`。作用：点赞数量超过设定数组 `like_nums` 的最大值后，后续语音播报与上次语音播报的间隔。
10. `black_user`：黑名单用户数组，全名！配置其中的用户行为将不被播报，包括：进场/弹幕/礼物/点赞。
11. `black_text`：屏蔽词数组，模糊匹配！弹幕内容包含屏蔽词中任意一个时，则不会播报。

## azure_config

文件名：`config_azure.json`，默认配置：

```json
{
  "azure_key":"",
  "azure_model":"",
  "azure_region":"",
  "azure_endpoint":""
}
```

### azure配置说明

1. `azure_key`：Azure平台的私钥。
2. `azure_model`：[语音服务的语言和声音支持](https://learn.microsoft.com/zh-cn/azure/ai-services/speech-service/language-support?tabs=tts)，常用中文模型（2024年1月记录）：

    ```json
    {
    "zh-CN-XiaoxiaoNeural": "（女）(default)",
    "zh-CN-YunxiNeural": "（男）",
    "zh-CN-YunjianNeural": "（男）",
    "zh-CN-XiaoyiNeural": "（女）",
    "zh-CN-YunyangNeural": "（男）",
    "zh-CN-XiaochenNeural": "（女）",
    "zh-CN-XiaohanNeural": "（女）",
    "zh-CN-XiaomengNeural": "（女）",
    "zh-CN-XiaomoNeural": "（女）",
    "zh-CN-XiaoqiuNeural": "（女）",
    "zh-CN-XiaoruiNeural": "（女）",
    "zh-CN-XiaoshuangNeural": "（女性、儿童）",
    "zh-CN-XiaoxuanNeural": "（女）",
    "zh-CN-XiaoyanNeural": "（女）",
    "zh-CN-XiaoyouNeural": "（女性、儿童）",
    "zh-CN-XiaozhenNeural": "（女）",
    "zh-CN-YunfengNeural": "（男）",
    "zh-CN-YunhaoNeural": "（男）",
    "zh-CN-YunxiaNeural": "（男）",
    "zh-CN-YunyeNeural": "（男）",
    "zh-CN-YunzeNeural": "（男）",
    "zh-CN-XiaochenMultilingualNeural1": "（女）",
    "zh-CN-XiaorouNeural1": "（女）",
    "zh-CN-XiaoxiaoDialectsNeural1": "（女）",
    "zh-CN-XiaoxiaoMultilingualNeural1": "（女）no voice？",
    "zh-CN-YunjieNeural1": "（男）",
    "zh-CN-YunyiMultilingualNeural1": "（男）"
    }
    ```

3. `azure_region`：Azure平台地区编码
4. `azure_endpoint`：Azure平台接口地址

## config_alibaba

已支持阿里巴巴的【[智能语音交互](https://nls-portal.console.aliyun.com/overview)】，目前以测试方式集成，需要每天申请token。

文件名：`config_alibaba.json`，默认配置：

```json
{
  "alibaba_appkey":"",
  "alibaba_token":"",
  "alibaba_model":"xiaoyun",
  "alibaba_endpoint":"nls-gateway-cn-shanghai.aliyuncs.com"
}
```

### alibaba配置说明

`alibaba` 智能语音交互的配置如上所示，参数介绍：

1. `alibaba_appkey`：智能语音交互创建项目后，项目的`appkey`；
2. `alibaba_token`：目前仅支持通过控制台获取临时token，临时token有效时间为24小时，失效后需要重新获取，获取方式可参考：[阿里云文档](https://help.aliyun.com/zh/isi/getting-started/obtain-an-access-token-in-the-console)；
3. `alibaba_model`：参考官方文档：[语音合成-接口说明](https://help.aliyun.com/zh/isi/developer-reference/overview-of-speech-synthesis)；
4 `alibaba_endpoint`：阿里云接口节点，有上海`shanghai`、北京`beijing`、深圳`shenzhen`三个节点，自行修改即可。

## config_soVits

以下是使用 `GPT-soVITS-Interface` 时需要配置的信息，其中除 `sovits_host` 配置项外，都可以忽略不填，具体配置参数请自行学习 `GPT-soVITS-Interface`，本仓库不做介绍。

```json
{
  "sovits_host":"http://127.0.0.1:5000/tts",
  "sovits_model":"Hutao",
  "sovits_language":"auto",
  "sovits_emotion":"",
  "sovits_top_k":"",
  "sovits_top_p":"",
  "sovits_temperature":"",
  "sovits_batch_size":"",
  "sovits_speed":"1.0",
  "sovits_save_temp":"false",
  "sovits_stream":"false",
  "sovits_format":"wav"
}
```
