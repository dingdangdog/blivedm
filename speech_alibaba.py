from readConfig import read_json_config
import http.client
# Python 2.x引入urllib模块。
# import urllib
# Python 3.x引入urllib.parse模块。
import urllib.parse
import json
import pygame
import os

ALIBABA_CLOUD_TTS_APPKEY: str = ''
ALIBABA_CLOUD_TTS_TOKEN: str = ''
VOICE: str = 'xiaoyun'  # 声音模型，默认xiaoyun
ENDPOINT: str = 'nls-gateway-cn-shanghai.aliyuncs.com'


def init_alibaba_config():
    global ALIBABA_CLOUD_TTS_APPKEY
    global ALIBABA_CLOUD_TTS_TOKEN
    global VOICE
    global ENDPOINT
    config = read_json_config("config_alibaba.json")
    ALIBABA_CLOUD_TTS_APPKEY = config['alibaba_appkey']
    ALIBABA_CLOUD_TTS_TOKEN = config['alibaba_token']
    VOICE = config['alibaba_model']
    ENDPOINT = config['alibaba_endpoint']


def alibaba_tts_speech(text):
    audioSaveFile = 'aliAudio.wav'
    format = 'wav'
    sampleRate = 16000

    processPOSTRequest(text, audioSaveFile, format, sampleRate)

    pygame.mixer.init()
    pygame.mixer.music.load(audioSaveFile)
    pygame.mixer.music.play()

    # 循环处理事件，直到音频播放完成并删除文件
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)
    pygame.mixer.music.stop()  # 停止音频播放
    # 关闭文件
    pygame.mixer.music.fadeout(200)  # 淡出效果，1000毫秒
    pygame.mixer.quit()
    os.remove(audioSaveFile)


# def processGETRequest(text, audioSaveFile, format, sampleRate):
# 采用RFC 3986规范进行urlencode编码。
# textUrlencode = text
# Python 3.x请使用urllib.parse.quote_plus。
# textUrlencode = urllib.parse.quote_plus(textUrlencode)
# textUrlencode = textUrlencode.replace("+", "%20")
# textUrlencode = textUrlencode.replace("*", "%2A")
# textUrlencode = textUrlencode.replace("%7E", "~")
# print('text: ' + textUrlencode)
#     url = f'https://{ENDPOINT}/stream/v1/tts'
#     # 设置URL请求参数
#     url = url + '?appkey=' + ALIBABA_CLOUD_TTS_APPKEY
#     url = url + '&token=' + ALIBABA_CLOUD_TTS_TOKEN
#     url = url + '&text=' + textUrlencode
#     url = url + '&format=' + format
#     url = url + '&sample_rate=' + str(sampleRate)
#     # voice 发音人，可选，默认是xiaoyun。
#     # url = url + '&voice=' + 'xiaoyun'
#     # volume 音量，范围是0~100，可选，默认50。
#     # url = url + '&volume=' + str(50)
#     # speech_rate 语速，范围是-500~500，可选，默认是0。
#     # url = url + '&speech_rate=' + str(0)
#     # pitch_rate 语调，范围是-500~500，可选，默认是0。
#     # url = url + '&pitch_rate=' + str(0)
#     print(url)
#     # Python 3.x请使用http.client。
#     conn = http.client.HTTPSConnection(ENDPOINT)
#     conn.request(method='GET', url=url)
#     # 处理服务端返回的响应。
#     response = conn.getresponse()
#     print('Response status and response reason:')
#     print(response.status, response.reason)
#     contentType = response.getheader('Content-Type')
#     print(contentType)
#     body = response.read()
#     if 'audio/mpeg' == contentType:
#         # 保存文件
#         with open(audioSaveFile, mode='wb') as f:
#             f.write(body)
#         print('The GET request succeed!')
#     else:
#         print('The GET request failed: ' + str(body))
#     conn.close()


def processPOSTRequest(text, audioSaveFile, format, sampleRate):
    url = f'https://{ENDPOINT}/stream/v1/tts'
    # 设置HTTPS Headers。
    httpHeaders = {
        'Content-Type': 'application/json'
    }
    # 设置HTTPS Body。
    body = {'appkey': ALIBABA_CLOUD_TTS_APPKEY, 'token': ALIBABA_CLOUD_TTS_TOKEN, 'text': text, 'format': format,
            'voice': VOICE, 'sample_rate': sampleRate}
    body = json.dumps(body)
    # print('The POST request body content: ' + body)
    # Python 2.x请使用httplib。
    # conn = httplib.HTTPSConnection(host)
    # Python 3.x请使用http.client。
    conn = http.client.HTTPSConnection(ENDPOINT)
    conn.request(method='POST', url=url, body=body, headers=httpHeaders)
    # 处理服务端返回的响应。
    response = conn.getresponse()
    # print('Response status and response reason:')
    # print(response.status, response.reason)
    contentType = response.getheader('Content-Type')
    # print(contentType)
    body = response.read()
    if 'audio/mpeg' == contentType:
        with open(audioSaveFile, mode='wb') as f:
            f.write(body)
        # print('The POST request succeed!')
    else:
        print('The POST request failed: ' + str(body))
    conn.close()


if __name__ == '__main__':
    init_alibaba_config()
    alibaba_tts_speech("你好，alibaba！")
