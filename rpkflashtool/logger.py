import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler
import appdirs

def excepthook(*exc_args):
    """
    Log exception and exit cleanly.
    """
    logging.error('Unrecoverable error', exc_info=(exc_args))
    sys.__excepthook__(*exc_args)
    sys.exit(1)

def setupLogger():
    LOG_DIR = appdirs.user_log_dir(appname='rpk-flash-tool', appauthor='python')
    LOG_FILE = os.path.join(LOG_DIR, 'rpk_flash_tool.log')

    if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

    log_fmt = ('%(asctime)s - %(name)s:%(lineno)d(%(funcName)s) '
               '%(levelname)s: %(message)s')
    formatter = logging.Formatter(log_fmt)

    handler = TimedRotatingFileHandler(LOG_FILE, when='midnight',
                                       backupCount=5, delay=0,
                                       encoding='utf-8')
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    # set up primary log
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    log.addHandler(handler)
    sys.excepthook = excepthook
    print('Logging to {}'.format(LOG_FILE))
