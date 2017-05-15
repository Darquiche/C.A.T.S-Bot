import logging
import os
import sys
import time

import pyautogui
import pycatsbot.key as key

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]\t%(asctime)s:\t%(message)s', datefmt='%H:%M:%S')

def GetFolder(filename):
    #simplifie le nom d'acces aux images
    return os.path.join('images', filename)

def GetGameRegion():
    #recupere la zone de jeu
    global GAME_REGION
    logging.info('Analyzing the screen...')
    region = pyautogui.locateOnScreen(GetFolder('top_left_corner.png'))
    logging.debug('NoxPlayer: %s' %(region,))
    if region is None:
        logging.error('Unable to find NoxPlayer. Make sure the game is visible!')
        sys.exit(1)

    topleftX = region[0]
    topleftY = region[1] + region[3]
    pyautogui.click((topleftX, topleftY), duration=0.25)
    logging.debug('Mouse initialized in the corner')

    GAME_REGION = (topleftX, topleftY, 800, 480) #configurer NoxPlayer en 480x800
    logging.info('Game region: %s' %(GAME_REGION,))
    return(GAME_REGION)

def Check_menu():
    menu = pyautogui.locateCenterOnScreen(GetFolder('friends.png'), region=GAME_REGION)
    if menu:
        logging.debug('Main menu detected')
        return True

def Check_sponsor():
    sponsor = pyautogui.locateCenterOnScreen(GetFolder('sponsor.png'), region=GAME_REGION)
    if sponsor:
        logging.info('Sponsor box detected!')
        pyautogui.click(sponsor, duration=0.25)
        menu = PressEsc()
        if menu:
            logging.info('Sponsor box opened!')
        else:
            logging.error('An error occurred during the opening!')
    time.sleep(1)

def Check_chests(chest):
    logging.debug('Test chest:' + str(chest))
    pyautogui.click(chest, duration=0.25)
    time.sleep(2)
    menu = Check_menu()
    if not menu:
        quit = pyautogui.locateCenterOnScreen(GetFolder('quit.png'), region=GAME_REGION)
        quit_alt = pyautogui.locateCenterOnScreen(GetFolder('quit_alt.png'), region=GAME_REGION)
        quit_big = pyautogui.locateCenterOnScreen(GetFolder('quit_big.png'), region=GAME_REGION)
        if quit:
            logging.info('Normal box locked.')
            unlock = pyautogui.locateCenterOnScreen(GetFolder('unlock.png'), region=GAME_REGION)
            if unlock:
                logging.info('Normal box can be unlocked...')
                pyautogui.click(unlock, duration=0.25)
                time.sleep(1)
            pyautogui.click(quit, duration=0.25)
        elif quit_alt:
            logging.info('Super box locked.')
            unlock = pyautogui.locateCenterOnScreen(GetFolder('unlock.png'), region=GAME_REGION)
            if unlock:
                logging.info('Super box can be unlocked...')
                pyautogui.click(unlock, duration=0.25)
                time.sleep(1)
            pyautogui.click(quit_alt, duration=0.25)
        elif quit_big:
            logging.debug('No box at:' + str(chest))
            pyautogui.click(quit_big, duration=0.25)
        else:
            menu = PressEsc()
            if menu:
                logging.info('Chest opened!')
            else:
                logging.error('An error occurred during the opening!')
    else:
        logging.debug('No chest at:' + str(chest))
    time.sleep(1)

def Check_reconnect():
    reconnect = pyautogui.locateCenterOnScreen(GetFolder('reconnect.png'), region=GAME_REGION)
    if reconnect:
        pyautogui.click(reconnect, duration=0.25)
        logging.info('Reconnect...')
        return True

def PressEsc():
    time.sleep(1)
    key.PressKey(0x1B)
    time.sleep(1)
    menu = Check_menu()
    if menu:
        return True
    else:
        return False

def Click_Championship():
    menu = Check_menu()
    if menu:
        pyautogui.click((GAME_REGION[0]+256, GAME_REGION[1]+399), duration=0.25)
        time.sleep(1)
        carte = pyautogui.locateCenterOnScreen(GetFolder('map.png'), region=GAME_REGION)
        reconnect = Check_reconnect()
        if carte:
            pyautogui.click((GAME_REGION[0]+710, GAME_REGION[1]+450), duration=0.25)
            while True:
                ok = pyautogui.locateCenterOnScreen(EasyPath('ok4.png'), region=GAME_REGION)
                if ok:
                    pyautogui.click(ok, duration=0.25)
                    break
                else:
                    time.sleep(2)
        elif reconnect:
            time.sleep(5)
            return
    time.sleep(1)

def Click_battle(WINS, DEFEATS):
    menu = Check_menu()
    if menu:
        pyautogui.click((GAME_REGION[0]+511, GAME_REGION[1]+399), duration=0.25)
        logging.info('Quick fight...')
        combat = False
        while not combat:
            skip = pyautogui.locateCenterOnScreen(GetFolder('skip.png'), region=GAME_REGION)
            reconnect = Check_reconnect()
            if reconnect:
                time.sleep(5)
                return
            if skip:
                logging.info('Fight found!')
                in_combat = 1
                break
        time.sleep(0.5)
        pyautogui.click((GAME_REGION[0]+400, GAME_REGION[1]+300), duration=0.25)
        logging.info('In fight!')
        end = False
        while not end:
            victory = pyautogui.locateCenterOnScreen(GetFolder('victory.png'), region=GAME_REGION)
            defeat = pyautogui.locateCenterOnScreen(GetFolder('defeat.png'), region=GAME_REGION)
            reconnect = Check_reconnect()
            if reconnect:
                time.sleep(5)
                return
            if defeat:
                logging.info('Defeat!')
                menu = PressEsc()
                DEFEATS = DEFEATS + 1
                break
            if victory:
                logging.info('Victory!')
                menu = PressEsc()
                WINS = WINS + 1
                break
    return (WINS, DEFEATS)

"""
GAME_REGION = GetGameRegion()
test = pyautogui.locateCenterOnScreen(GetFolder('test.png'), region=GAME_REGION)
if test:
    print(test[0]-GAME_REGION[0])
    print(test[1]-GAME_REGION[1])
"""
