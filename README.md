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