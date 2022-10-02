from PIL import Image
import pytesseract
import requests
import base64
import numpy as np

def parse(url):
    img = Image.open(url)
    txt = pytesseract.image_to_string(img)
    actualTextSplit = []
    atsTarr = []

    for word in txt.split('\n'):
        if(word == ''):
            actualTextSplit.append(atsTarr)
            atsTarr = []
        else:
            atsTarr.append(word)

    actualText = ''
    for array in actualTextSplit:
        actualText += ' '.join(array) + '\n'
    actualText = actualText.replace('made with mematic',' ')
    return actualText

#'en_us_006', text, savefilename
def tts(req_text, filename,text_speaker='en_us_006'):
    
    req_text = req_text.replace("+", "plus")
    req_text = req_text.replace(" ", "+")
    req_text = req_text.replace("&", "and")

    url = f"https://api16-normal-useast5.us.tiktokv.com/media/api/text/speech/invoke/?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0"

    r = requests.post(url)

    vstr = [r.json()["data"]["v_str"]][0]

    b64d = base64.b64decode(vstr)
    with open(filename, "wb") as f:
        f.write(b64d)

