from readConfig import read_json_config
import pygame
import os

import requests

SOVITS_HOST: str = ''
SOVITS_MODEL: str = ''
SOVITS_LANGUAGE: str = 'auto'
SOVITS_EMOTION: str = ''
SOVITS_TOP_K: str = ''
SOVITS_TOP_P: str = ''
SOVITS_TEMPERATURE: str = ''
SOVITS_BATCH_SIZE: str = ''
SOVITS_SPEED: str = '1.0'
SOVITS_SAVE_TEMP: str = 'false'
SOVITS_STREAM: str = 'false'
SOVITS_FORMAT: str = 'wav'

def init_sovits_config():
    global SOVITS_HOST
    global SOVITS_MODEL
    global SOVITS_LANGUAGE
    global SOVITS_EMOTION
    global SOVITS_TOP_K
    global SOVITS_TOP_P
    global SOVITS_TEMPERATURE
    global SOVITS_BATCH_SIZE
    global SOVITS_SPEED
    global SOVITS_SAVE_TEMP
    global SOVITS_STREAM
    global SOVITS_FORMAT

    config = read_json_config("config_sovits.json")
    SOVITS_HOST = config['sovits_host']
    SOVITS_MODEL = config['sovits_model']
    SOVITS_LANGUAGE = config['sovits_language']
    SOVITS_EMOTION = config.get('sovits_emotion', '')  # Provide default value if key is missing
    SOVITS_TOP_K = config.get('sovits_top_k', '')  # Provide default value if key is missing
    SOVITS_TOP_P = config.get('sovits_top_p', '')  # Provide default value if key is missing
    SOVITS_TEMPERATURE = config.get('sovits_temperature', '')  # Provide default value if key is missing
    SOVITS_BATCH_SIZE = config.get('sovits_batch_size', '')  # Provide default value if key is missing
    SOVITS_SPEED = config.get('sovits_speed', '1.0')  # Provide default value if key is missing
    SOVITS_SAVE_TEMP = config.get('sovits_save_temp', 'false')  # Provide default value if key is missing
    SOVITS_STREAM = config.get('sovits_stream', 'false')  # Provide default value if key is missing
    SOVITS_FORMAT = config.get('sovits_format', 'wav')  # Provide default value if key is missing

def sovits_tts_speech(text):
    audioSaveFile = 'sovitsAudio.wav'

    processGETRequest(text, audioSaveFile)

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


def processGETRequest(text, audioSaveFile):
    url = f'{SOVITS_HOST}?character={SOVITS_MODEL}&text={text}'

    # Append optional parameters if they are not empty
    optional_params = {
        'text_language': SOVITS_LANGUAGE,
        'emotion': SOVITS_EMOTION,
        'top_k': SOVITS_TOP_K,
        'top_p': SOVITS_TOP_P,
        'temperature': SOVITS_TEMPERATURE,
        'batch_size': SOVITS_BATCH_SIZE,
        'speed': SOVITS_SPEED,
        'save_temp': SOVITS_SAVE_TEMP,
        'stream': SOVITS_STREAM,
        'format': SOVITS_FORMAT,
    }

    for key, value in optional_params.items():
        if value:  # Only add the parameter if it has a value
            url += f"&{key}={value}"

    # Make the GET request
    response = requests.get(url, stream=True)
    # Check if the request was successful
    if response.status_code == 200:
        # Save the response content to a local file
        with open(audioSaveFile, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        print(f"Failed to fetch the audio. Status code: {response.status_code}")
        print(response.text)  # Print the error message for debugging


if __name__ == '__main__':
    init_sovits_config()
    sovits_tts_speech("你好，sovits！")
