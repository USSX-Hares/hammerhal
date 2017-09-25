import json
import logging
import logging.config
import os, sys

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


def start(argv=sys.argv):
    # Configure logger
    setup_logging()
    logger = logging.getLogger('hammerhal')
    logger.info("Logger started")
    ConfigLoader.load_configs()

    if (argv == sys.argv):
        if (len(argv) > 1):
            args = argv[1:]
        else:
            logger.error("Command is required")
            print_help(logger)
            return 2
    elif (len(argv) > 0):
        args = argv
    else:
        logger.error("Command is required")
        print_help(logger)
        return 2

    return run_command(logger, args)

def run_command(logger, args):
    command = args[0].strip().lower()

    arg = (' '.join(args[1:]) if len(args) > 1 else '').strip().lower()
    if (command in commands):
        logger.debug("Running command '{command}' with arguments '{arg}'".format(command=command, arg=arg))
        return commands[command](logger, arg)
    elif (command == 'exit'):
        logger.debug("Exiting now")
        return 0
    else:
        logger.error("Unsupported command: '{command}'".format(command=command))
        print_help(logger)
        return 3

def compile_all(logger, *args):
    e_code = 0
    e_code += compile_heroes(logger)
    e_code += compile_adversaries(logger)

    return 1 if e_code else 0

def compile_heroes(logger):
    compiler = HeroCompiler()
    heroes = compiler.search()
    e_code = 0
    logger.info("Gonna to compile heroes. There are {n} to deal with.".format(n=len(heroes)))
    for hero in heroes:
        e_code += compile_hero(logger, hero, compiler)

    return e_code

def compile_hero(logger, hero, compiler=None):
    if (not compiler):
        compiler = HeroCompiler()

    result = compiler.open(hero) and compiler.compile() and compiler.save(forced_width=720)
    if (result):
        logger.info("Success! File saved to '{filename}'".format(filename=result))
        return 0
    else:
        logger.error("Cannot compile {hero}".format(hero=hero))
        return 1


def compile_adversaries(logger):
    compiler = AdversaryCompiler()
    adversaries = compiler.search()
    e_code = 0
    logger.info("Gonna to compile adversaries. There are {n} to deal with.".format(n=len(adversaries)))
    for adversary in adversaries:
        e_code += compile_adversary(logger, adversary, compiler)

    return e_code

def compile_adversary(logger, adversary, compiler=None):
    if (not compiler):
        compiler = AdversaryCompiler()

    result = compiler.open(adversary) and compiler.compile() and compiler.save(forced_width=1080)
    if (result):
        logger.info("Success! File saved to '{filename}'".format(filename=result))
        return 0
    else:
        logger.error("Cannot compile {adversary}".format(adversary=adversary))
        return 1

def run_interactive(logger, *args):

    while True:
        print('> ', end='')
        command = input()
        _args = [ s for s in command.split() if s ]
        run_command(logger, _args)
        if (_args == [ "exit" ]):
            return 0
        print('')

def print_help(logger, *kwargs):

    print("""
Hammerhal datasheet compiler tool v0.1

Usage:
  python compile.py COMMAND [ ARGUMENT ]

Available commands (case-insensitive):
  all           Compiles all heroes and adversaries.
  hero          Compiles a specific hero (argument required).
  adversary     Compiles a specific adversary (argument required).
  
  interactive   Launches compiler in the interactive mode.
  exit          Exits the interactive mode.
  help, ?       Prints this message.
  
(c) 2017, USSX Hares, MIT License""")

    return 0

commands = \
{
    'all': compile_all,
    'hero': compile_hero,
    'adversary': compile_adversary,
    'interactive': run_interactive,
    'help': print_help,
    '?': print_help
}


if (__name__ == "__main__"):
    e_code = start()
    exit(e_code)