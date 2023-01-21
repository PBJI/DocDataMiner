# This script require abiword to be installed and 
# the executable path saved to system environment path.
# Step 1:
from pdf2image import convert_from_path as cpdf_img
from docx2pdf import convert as cword_pdf
from PIL import Image
from os.path import exists
from os.path import basename
import os.path import splitext
from os import system
from os import remove as removePDF
from os import sep
from mimetypes import guess_type as guessFile
DIRNAME = ['images', 'text']

#fileopen loads any format specified and transforms them into PIL Image Object
def fileopen(file:'Image/Pdf/Word path', dpi=300) -> '[PIL image object]':
    if (exists(file)):
        if "pdf" in guessFile(file)[0]:
            pil_images = cpdf_img(file, dpi)
            return [pil_images, basename(file)]
        elif "image" in guessFile(file)[0]:
            pil_image = Image.open(file)
            return [[pil_image], basename(file)]
        elif "word" in guessFile(file)[0]:
            cmd = "abiword --to=PDF --to-name='temp.pdf' " + file
            system(cmd)
            pil_images = cpdf_img('temp.pdf', dpi)
            removePDF('temp.pdf')
            return [pil_images, basename(file)]
        else:
            return None

#imagesave saves list of PIL Image object in the specified folder or default if none
#specified.
#also if we want we can give custom names to the saved images by supplying filename
def imageSave(pil_list:'[PIL image object]', dirname=DIRNAME[0], filename):
    if dirname == DIRNAME[0]:
        for i in DIRNAME:
        try:
            os.makedirs(i)
            print("[!] Directory ", i, " Created")
        except FileExistsError:
            print("[X] Directory ", i, " already exists")

    if "str" not in type(filename):
        filename, ext = splitext(pil_list[1])
    file_index = "0"
    for ob in pil_list[0]:
        imagePath = '.'+sep+dirname+sep+filename+'['+file_index+']'".png"
        ob.save(imagePath)
