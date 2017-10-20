from logging import getLogger
import sys

import hammerhal.generator
from hammerhal import ConfigLoader
from hammerhal.preloads import setup_logging, preload_fonts


def start(argv=sys.argv):

    # Configure logger
    setup_logging()
    preload_fonts()
    logger = getLogger('hammerhal')
    logger.info("Logger started")
    ConfigLoader.load_configs()

    if (not hammerhal.generator.generator_supported):
        msg = "Generator feature is not supported on your system"
        logger.critical(msg)
        from tkinter import messagebox
        messagebox.showerror(message=msg)
        return 2
    from hammerhal.generator import CardGenerator

    file = None
    if (argv == sys.argv):
        if (len(argv) > 1):
            file = argv[1]
    elif (len(argv) > 0):
        file = argv[0]


    try:
        _gen = CardGenerator()
        if (file):
            _gen.open(file)
        result = _gen.show()
    except:
        logger.exception("Uncaught exception!")
        result = 1

    return result

if (__name__ == "__main__"):
    e_code = start()
    exit(e_code)