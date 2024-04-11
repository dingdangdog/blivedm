# blivedm-voice

Fork Form：[blivedm](https://github.com/xfgryujk/blivedm)

## package

- need: `pip install pyinstaller`

```shell
# pyinstaller --onefile blivemd-voice.py

# windows azure
pyinstaller --onefile --add-data "./.venv/Lib/site-packages/azure;azure" blivemd-voice.py
```

## config

### platform

> Currently only supports windows.

select: 
- win (`default`)
- mac
- linux

### mode

select:
- local (`default`)
- azure

### bilibili_SESSION

There should to write a logged in `SESSDATA`, you can get it in `cookie`.
You can connect without filling it in, but username and id will not be obtained.

### bilibili_heart_print

Heartbeat monitoring information printing interval.

### azure_model

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

### alibaba

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
