# blivedm-voice

Fork Form：[blivedm](https://github.com/xfgryujk/blivedm)

## package

执行 `pip install pyinstaller` 安装 `pyinstaller`，然后执行下面的打包脚本：

Execute `pip install pyinstaller` to install `pyinstaller`, and then execute the following packaging script:
```shell
# pyinstaller --onefile blivemd-voice.py

# windows azure
pyinstaller --onefile --add-data "./.venv/Lib/site-packages/azure;azure" blivemd-voice.py
```

## config_blive

### platform

> 目前仅支持windows。

可选配置（select）: 
- win (`default`)
- mac
- linux

### mode

可选配置（select）:
- local (`default`)
- azure

### bilibili_SESSION

这里应该写一个已登录的`SESSDATA`，你可以在`cookie`中获取它。
不填写也可以连接，但是不会获取用户名和id。

There should to write a logged in `SESSDATA`, you can get it in `cookie`.
You can connect without filling it in, but username and id will not be obtained.

### bilibili_heart_print

心跳监控信息打印间隔。

Heartbeat monitoring information printing interval.

### voice_text

用于配置常用的语音文本。

Used to configure commonly used voice texts.

默认配置（default）：
```json
{
    "enter": "欢迎 {uname} 进入直播间，记得常来玩哦！",
    "danmaku": "{uname}说：{msg}",
    "gift": "感谢 {uname} 赠送的 {num}个{gift_name}，谢谢老板，老板大气！",
    "like": "感谢 {uname} {like_text}",
    "like_total": "本次直播点赞数量达到 {click_count} 次"
}
```
配置详细说明：
- enter：进入直播间的语音文字，`uname` 会自动替换为用户昵称；
- danmaku：弹幕播报的语音文字，`uname`-用户昵称、`msg`-弹幕内容；
- gift：礼物播报的语音文字，`uname`-用户昵称、`num`-礼物个数、`gift_name`-礼物名称；
- like：用户点赞的语音文字，`uname`-用户昵称、`like_text`-B站官方点赞提示文字；
- like_total：点赞总结的语音文字，`click_count`-总点赞次数。

## azure_config

### azure_model

[语音服务的语言和声音支持](https://learn.microsoft.com/zh-cn/azure/ai-services/speech-service/language-support?tabs=tts)

[Language and voice support for the Speech service](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts)

- 中文模型（2024年1月记录）：
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

## config_alibaba

已支持阿里巴巴的【[智能语音交互](https://nls-portal.console.aliyun.com/overview)】，目前以测试方式集成，需要每天申请token。

```json
{
  "alibaba_appkey":"",
  "alibaba_token":"",
  "alibaba_model":"xiaoyun",
  "alibaba_endpoint":"nls-gateway-cn-shanghai.aliyuncs.com"
}
```

`alibaba` 智能语音交互的配置如上所示，参数介绍：
- `alibaba_appkey`：智能语音交互创建项目后，项目的`appkey`；
- `alibaba_token`：目前仅支持通过控制台获取临时token，临时token有效时间为24小时，失效后需要重新获取，获取方式可参考：[阿里云文档](https://help.aliyun.com/zh/isi/getting-started/obtain-an-access-token-in-the-console)；
- `alibaba_model`：参考官方文档：[语音合成-接口说明](https://help.aliyun.com/zh/isi/developer-reference/overview-of-speech-synthesis)；
- `alibaba_endpoint`：阿里云接口节点，有上海`shanghai`、北京`beijing `、深圳`shenzhen`三个节点，自行修改即可。
