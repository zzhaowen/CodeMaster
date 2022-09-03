#Google Text-to-Speech
from gtts import gTTS
import os

# language = ‘zh-cn’ or 'en' or..
def playsound(text,language):
    mytext = text
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("playsound.mp3")
    # os.system("../Oscar/playsound.mp3")
    os.system("playsound.mp3")