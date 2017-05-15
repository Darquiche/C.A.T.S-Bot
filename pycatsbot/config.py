import configparser

def Config(chest_verification=True,
    test_championship=False,
    failsafe=True,
    OCR_MODE=False,
    check_chest_on_startup=False,
    sponsor_verification=True,
    debug=False):
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        chest_verification = config.getboolean('CONFIG', 'chest_verification')
        test_championship = config.getboolean('CONFIG', 'test_championship')
        failsafe = config.getboolean('CONFIG', 'failsafe')
        OCR_MODE = config.getboolean('CONFIG', 'OCR_MODE')
        check_chest_on_startup = config.getboolean('CONFIG', 'check_chest_on_startup')
        sponsor_verification = config.getboolean('CONFIG', 'sponsor_verification')
        debug = config.getboolean('CONFIG', 'debug')

        return (chest_verification, test_championship, failsafe, OCR_MODE, check_chest_on_startup, sponsor_verification, debug)
    except:
        config = configparser.ConfigParser()
        config['CONFIG'] = {'chest_verification': chest_verification,
                            'test_championship': test_championship,
                            'failsafe': failsafe,
                            'OCR_MODE': OCR_MODE,
                            'check_chest_on_startup': check_chest_on_startup,
                            'sponsor_verification': sponsor_verification,
                            'debug': debug}

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        return (chest_verification, test_championship, failsafe, OCR_MODE, check_chest_on_startup, sponsor_verification, debug)

def GetStats(WINS=0, DEFEATS=0, GOLDS=0, RANK=0):
    try:
        file = open('stats.dat', 'r')
        stats = (file.read().splitlines())
        WINS = int(stats[0])
        DEFEATS = int(stats[1])
        GOLDS_ST = int(stats[2])
        RANK_ST = int(stats[3])
        file.close()
        return WINS, DEFEATS, GOLDS_ST, RANK_ST
    except:
        file = open('stats.dat', 'w+')
        file.close()
        return WINS, DEFEATS, GOLDS, RANK
