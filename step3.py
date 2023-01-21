import cv2
import pytesseract
DIRNAME = ['images', 'text']

#This file requires tesseract to installed on the system and
#saved in the system environment path
def textExtraction(file:'Image', txtdir=DIRNAME[1]) -> 'Text':
    psm = [3,4,6, 11] # Not implemented
    config  = ('-l eng --oem 3 --psm '+ str(psm[11]))
    img = cv2.imread(file)
    text = pytesseract.pytesseract.image_to_string(img, lang='eng', config=config)
    return [text, filename]

def textSave(text, filename, txtdir=DIRNAME[1]):
    if txtdir == DIRNAME[1]:
        for i in DIRNAME:
        try:
            os.makedirs(i)
            print("[!] Directory ", i, " Created")
        except FileExistsError:
            print("[X] Directory ", i, " already exists")

    filename, ext = file.split(".")
    fileTxt = open(f"{txtdir}/{filename}.txt", "w")
    fileTxt.write(text)
