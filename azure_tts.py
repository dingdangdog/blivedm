from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

from readConfig import read_json_config

SECRET_KEY: str = ''
MODEL: str = 'zh-CN-XiaoxiaoNeural'
REGION: str = ''
ENDPOINT: str = ''

SPEECH_CONFIG: SpeechConfig = None
SYNTHESIZER: SpeechSynthesizer = None


def init_azure_config():
    global MODEL
    global SECRET_KEY
    global REGION
    global ENDPOINT
    config = read_json_config()
    SECRET_KEY = config['azure_key']
    MODEL = config['azure_model']
    REGION = config['azure_region']
    ENDPOINT = config['azure_endpoint']

    global SPEECH_CONFIG
    global SYNTHESIZER
    # SpeechConfig
    SPEECH_CONFIG = SpeechConfig(subscription=SECRET_KEY, region=REGION)
    SPEECH_CONFIG.speech_synthesis_voice_name = MODEL
    # SpeechSynthesizer
    SYNTHESIZER = SpeechSynthesizer(speech_config=SPEECH_CONFIG)


def azure_tts_speech(text):
    SYNTHESIZER.speak_text(text)

    # 检查转换是否成功
    # if result.reason == ResultReason.SynthesizingAudioCompleted:
    #     print("Speech synthesized to speaker for text [{}]".format(text))
    #     # 将语音保存到本地文件
    #     audio_file_path = "output.wav"
    #     result = synthesizer.synthesize_to_file(text, audio_file_path)
    #     if result.reason == ResultReason.SynthesizingAudioCompleted:
    #         print("Speech synthesized to file: {}".format(audio_file_path))
    #     else:
    #         print("Speech synthesis to file failed: {}".format(result.reason))
    #
    #     # 使用本地音频播放器播放
    #     os.system("start " + audio_file_path)
    # else:
    #     print("Speech synthesis failed: {}".format(result.reason))


if __name__ == '__main__':
    azure_tts_speech("你好，azure！")
