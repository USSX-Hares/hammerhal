import json
import logging
import logging.config
import os

from hammerhal.compilers import HeroCompiler, AdversaryCompiler
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

    e_code = 0
    e_code += compile_heroes(logger)
    e_code += compile_adversaries(logger)
    return e_code

def compile_heroes(logger):
    compiler = HeroCompiler()
    heroes = \
    [
        'wight-king',
        'grey-seer',
        'orruk-weirdnob-shaman',
        'battlemage',
        'chaos-sorcerer-lord',
        'great-bray-shaman',
        'lord-castellant',
    ]
    e_code = len(heroes)
    for hero in heroes:
        result = compiler.open(hero) and compiler.compile() and compiler.save(forced_width=720)
        if (result):
            message = "Success! File saved to '{filename}'".format(filename=result)
            logger.info(message)
            print(message)
            e_code -= 1
        else:
            logger.error("Cannot compile {hero}".format(hero=hero))

    return e_code

def compile_adversaries(logger):
    compiler = AdversaryCompiler()
    adversaries = \
    [
        'chaos-sorcerer-lord',
    ]
    e_code = len(adversaries)
    for adversary in adversaries:
        result = compiler.open(adversary) and compiler.compile() and compiler.save(forced_width=720)
        if (result):
            message = "Success! File saved to '{filename}'".format(filename=result)
            logger.info(message)
            print(message)
            e_code -= 1
        else:
            logger.error("Cannot compile {adversary}".format(adversary=adversary))

    return e_code

if (__name__ == "__main__"):
    e_code = start()
    exit(e_code)