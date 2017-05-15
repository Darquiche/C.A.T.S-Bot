import time
import logging

import pycatsbot.bot as bot
import pycatsbot.config as config
import pycatsbot.key as key
import pycatsbot.ocr as ocr

#Initialisation du logger
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]\t%(asctime)s:\t%(message)s', datefmt='%H:%M:%S')
#logging.disable(logging.INFO)

CHEST_VERIFICATION, CHAMPIONSHIP, FAILSAFE, OCR_MODE, CHECK_CHESTS_ONSTARTUP, SPONSOR_VERIFICATION, DEBUG = config.Config()

logging.info('- C.A.T.S - Auto battler -')
logging.info('Initializing...')

if not DEBUG:
    logging.disable(logging.DEBUG)

GAME_REGION = bot.GetGameRegion()
WINS, DEFEATS, GOLDS_ST, RANK_ST = config.GetStats()
###############################################################################
#(x1,y1) = Coin haut gauche de la zone de jeu
#(x2,y2) = Coin bas droit de la zone de jeu
x1, y1, x2, y2 = GAME_REGION[0], GAME_REGION[1], GAME_REGION[2], GAME_REGION[3]

#Coordonnées des coffres
CHEST_topleft = (x1+125, y1+160)
CHEST_topright = (x1+235, y1+160)
CHEST_botleft = (x1+125, y1+325)
CHEST_botright = (x1+235, y1+325)

#Zones textuelles (les box)
GOLD_BOX = (x1+45, y1, 95, 50)#zone qui affiche le nombre de pieces
RANK_BOX = (x1+490, y1, 80, 50)#zone qui affiche le nombre de points
###############################################################################

logging.debug("- Debug -")
logging.debug("Chest Verification: %s" % CHEST_VERIFICATION)
logging.debug("Sponsor Verification: %s" % SPONSOR_VERIFICATION)
logging.debug("Auto championship: %s" % CHAMPIONSHIP)
logging.debug("Check chest on startup: %s" % CHECK_CHESTS_ONSTARTUP)
logging.debug("Failsafe: %s" % FAILSAFE)
logging.debug("OCR_MODE: %s" % OCR_MODE)

logging.info('- Stats -')
logging.info('Wins: ' + str(WINS))
logging.info('Defeats: ' + str(DEFEATS))
if WINS != 0 and DEFEATS != 0:
    logging.info('Winrate: ' + ('%.2f' % (WINS/DEFEATS)).replace('.', ','))


if OCR_MODE == True:
    try:
        tool, lang = ocr.InitOCR()
        GOLDS = (ocr.GetIntOf(tool, lang, GOLD_BOX))
        RANK = (ocr.GetIntOf(tool, lang, RANK_BOX))
        logging.info('- OCR results -')
        logging.info("Golds (OCR): %s" % GOLDS)
        logging.info("Rank (OCR): %s" % RANK)
    except:
        logging.error('OCR Processing error')
        logging.info("Golds (stats): %s" % GOLDS_ST)
        logging.info("Rank (stats): %s" % RANK_ST)
        GOLDS = 0
        RANK = 0
else:
    logging.error('OCR is disabled. Golds and Rank cannot be tracked.')
    GOLDS = 0
    RANK = 0

logging.info('Starting the bot... [Ctrl + C] to quit at any time')
milli_time = int(round(time.time() * 1000))

if CHECK_CHESTS_ONSTARTUP:
    test = 1
else:
    test = 0

champion = 0
check_rank = 0

try:
    while True:
        in_menu = bot.Check_menu()
        if in_menu:
            current_milli_time = int(round(time.time() * 1000))
            if current_milli_time > (milli_time + 480000): #test 8 minutes
                milli_time = int(round(time.time() * 1000))
                test = 1
                check_rank = 1
                champion = 1
            if CHEST_VERIFICATION == True and test == 1:
                test = 0
                bot.Check_chests(CHEST_topleft)
                bot.Check_chests(CHEST_topright)
                bot.Check_chests(CHEST_botleft)
                bot.Check_chests(CHEST_botright)
                logging.info('Chest verification every 8 minutes!')
            if CHAMPIONSHIP == True and champion == 1:
                champion = 0
                bot.Click_Championship()
                logging.info('Test the championship every 8 minutes!')
            if check_rank == 1 and OCR_MODE==True:
                check_rank = 0
                RANK = (ocr.GetIntOf(tool, lang, RANK_BOX))
                logging.info("Actual Rank (OCR): %s" % RANK)
            if SPONSOR_VERIFICATION == True:
                bot.Check_sponsor()
            WINS, DEFEATS = bot.Click_battle(WINS, DEFEATS)
            time.sleep(1)
            in_menu = bot.Check_menu()
        else:
            reconnect = bot.Check_reconnect()
            if reconnect:
                time.sleep(5)
            in_menu = bot.PressEsc()

except KeyboardInterrupt:
    file = open('stats.dat', 'w')
    stats = (str(WINS) +"\n"+ str(DEFEATS) + "\n" + str(GOLDS) + "\n" + str(RANK))
    file.write(stats)
    logging.info('Stats saved!')
    file.close()
    logging.error('Bot stopped!')
