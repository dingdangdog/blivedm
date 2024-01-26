from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, ResultReason
import os


# 指定声音模型，例如 "en-US-GuyNeural" 为英语男声模型
voice_model = "zh-CN-YunzeNeural"

# 替换成你的 Azure 订阅密钥和终结点
subscription_key = "ad46a4efab11412e8db6bcf10dd79d69"
region = "japanwest"

# 替换成你的 Text-to-Speech 资源的终结点
endpoint = "https://japanwest.api.cognitive.microsoft.com/"

# 设置 SpeechConfig
speech_config = SpeechConfig(subscription=subscription_key, region=region)
speech_config.speech_synthesis_voice_name = voice_model

# 创建 SpeechSynthesizer
synthesizer = SpeechSynthesizer(speech_config=speech_config)

def azure_tts_speech(text):
    # 开始文本到语音转换
    result = synthesizer.speak_text(text)

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
