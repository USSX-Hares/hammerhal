import json
import logging
import logging.config
import os

from hammerhal.compilers import HeroCompiler
from hammerhal import ConfigLoader

def setup_logging(
    default_path='configs/logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def start():
    # Configure logger
    setup_logging()
    logger = logging.getLogger('hammerhal')
    logger.info("Logger started")

    ConfigLoader.load_configs()
    compiler = HeroCompiler()
    heroes = [ 'wight-king', 'grey-seer' ]
    for hero in heroes:
        result = compiler.open(hero) and compiler.compile() and compiler.save()
        if (result):
            message = "Success! File saved to {filename}".format(filename=result)
            logger.info(message)
            print(message)
        else:
            logger.error("Cannot compile {hero}".format(hero=hero))

start()