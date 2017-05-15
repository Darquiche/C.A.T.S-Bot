from PIL import Image
import pyscreeze
import pyocr
import pyocr.builders
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]\t%(asctime)s:\t%(message)s', datefmt='%H:%M:%S')

def InitOCR():
    #Initialisation de l'OCR
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        logging.error("No OCR tool found")
        sys.exit(1)
    #La liste est recuperee dans l'ordre des recommendations
    tool = tools[0]
    logging.debug("OCR tool: '%s'" % (tool.get_name()))

    langs = tool.get_available_languages()
    logging.debug("Available languages: %s" % ", ".join(langs))
    lang = langs[1] #chez moi 0=eng, 1=fra, 3=osd
    logging.debug("Used lang: '%s'" % (lang))
    #L'ordre et la liste des langages dependent de votre configuration
    return(tool, lang)

def GetIntOf(tool, lang, box):
    #recupere des valeurs affichees a l'ecran avec l'OCR (Reconnaissance Optique des Caracteres)
    value = ""
    digits = tool.image_to_string(
        pyscreeze.screenshot('screendebug.png', region=box),
        lang=lang,
        builder=pyocr.tesseract.DigitBuilder()
    )
    logging.debug(digits)
    for i in digits:
        if i == " ":
            break
        value=(value+i)
    return(int(value))

def GetTxtOf(tool, lang, box):
    #recupere des valeurs affichees a l'ecran avec l'OCR (Reconnaissance Optique des Caracteres)
    string = ""
    txt = tool.image_to_string(
        pyscreeze.screenshot('screendebug.png', region=box),
        lang=lang,
        builder=pyocr.builders.TextBuilder()
    )
    logging.debug(txt)
    for i in txt:
        if i == " ":
            break
        string=(string+i)
    return(string)
