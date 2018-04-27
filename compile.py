from logging import getLogger
import sys

from hammerhal.preloads import setup_logging, preload_fonts
from hammerhal import ConfigLoader
from hammerhal.compilers import HeroCompiler, AdversaryCompiler, CardCompiler, MinionCompiler


def start(argv=sys.argv):
    # Configure logger
    setup_logging()
    preload_fonts()
    logger = getLogger('hammerhal')
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
    e_code += compile_cards(logger)

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
    if (hero == "all"):
        return compile_heroes(logger)

    if (not compiler):
        compiler = HeroCompiler()

    result = compiler.open(hero) and compiler.compile() and compiler.save_compiled(forced_width=720)
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
    if (adversary == "all"):
        return compile_adversaries(logger)

    if (not compiler):
        compiler = AdversaryCompiler()

    result = compiler.open(adversary) and compiler.compile() and compiler.save_compiled(forced_width=1600)
    if (result):
        logger.info("Success! File saved to '{filename}'".format(filename=result))
        return 0
    else:
        logger.error("Cannot compile {adversary}".format(adversary=adversary))
        return 1


def compile_minions(logger):
    compiler = MinionCompiler()
    minions = compiler.search()
    e_code = 0
    logger.info("Gonna to compile minions. There are {n} to deal with.".format(n=len(minions)))
    for minion in minions:
        e_code += compile_minion(logger, minion, compiler)

    return e_code

def compile_minion(logger, minion, compiler=None):
    if (minion == "all"):
        return compile_minions(logger)

    if (not compiler):
        compiler = MinionCompiler()

    result = compiler.open(minion) and compiler.compile() and compiler.save_compiled(forced_width=720)
    if (result):
        logger.info("Success! File saved to '{filename}'".format(filename=result))
        return 0
    else:
        logger.error("Cannot compile {minion}".format(minion=minion))
        return 1


def compile_cards(logger, type=None, set=None):
    compiler = CardCompiler()
    cards = compiler.search(type=type, set=set)
    e_code = 0
    logger.info("Gonna to compile cards. There are {n} to deal with.".format(n=len(cards)))
    for card in cards:
        e_code += compile_card(logger, card, compiler)

    return e_code

def compile_card(logger, card, compiler=None):
    keywords = card.split()
    type = None
    set = None
    compile_all_cards = False
    for i in range(len(keywords)):
        keyword = keywords[i].strip()
        if (keyword == "all"):
            compile_all_cards = True
        elif (keyword.startswith("type:")):
            type = keyword[5:]
        elif (keyword.startswith("set:")):
            set = keyword[4:]
        else:
            break

    if (compile_all_cards):
        return compile_cards(logger, type=type, set=set)

    card = ' '.join(keywords[i:])

    if (not compiler):
        compiler = CardCompiler()

    result = compiler.open(card, set=set, type=type) and compiler.compile() and compiler.save_compiled(forced_width=640)
    if (result):
        logger.info("Success! File saved to '{filename}'".format(filename=result))
        return 0
    else:
        logger.error("Cannot compile {card}".format(card=card))
        return 1


def compile_artifacts(logger, type=None, set=None):
    compiler = CardCompiler()
    artifacts = compiler.search(type=type, set=set)
    e_code = 0
    logger.info("Gonna to compile artifacts. There are {n} to deal with.".format(n=len(artifacts)))
    for artifact in artifacts:
        e_code += compile_artifact(logger, artifact, compiler)

    return e_code

def compile_artifact(logger, artifact, compiler=None):
    keywords = artifact.split()
    set = None
    compile_all_artifacts = False
    for i in range(len(keywords)):
        keyword = keywords[i].strip()
        if (keyword == "all"):
            compile_all_artifacts = True
        elif (keyword.startswith("set:")):
            set = keyword[4:]
        else:
            break

    if (compile_all_artifacts):
        return compile_artifacts(logger, type=type, set=set)

    artifact = ' '.join(keywords[i:])

    if (not compiler):
        compiler = CardCompiler()

    result = compiler.open(artifact, set=set, type=type) and compiler.compile() and compiler.save_compiled(forced_width=640)
    if (result):
        logger.info("Success! File saved to '{filename}'".format(filename=result))
        return 0
    else:
        logger.error("Cannot compile {artifact}".format(artifact=artifact))
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
  hero          Compiles a specific hero (argument required; "all" for compiling all adversaries).
  adversary     Compiles a specific adversary (argument required; "all" for compiling all heroes).
  card          Compiles a specific card (argument required; "all" for compiling all cards; may specify set {SET} by passing argument 'set:{SET}' and card type {TYPE} py passing 'type:{TYPE}').
  artifact      Compiles a specific artifact (argument required; "all" for compiling all artifacts; may specify set {SET} by passing argument 'set:{SET}').
  minion        Compiles a specific minion (argument required; "all" for compiling all minions).
  
  interactive   Launches compiler in the interactive mode.
  exit          Exits the interactive mode.
  help, ?       Prints this message.
  
(c) 2017-2018, USSX Hares, MIT License""")

    return 0

commands = \
{
    'all': compile_all,
    'hero': compile_hero,
    'adversary': compile_adversary,
    'card': compile_card,
    'artifact': compile_artifact,
    'minion': compile_minion,
    'interactive': run_interactive,
    'help': print_help,
    '?': print_help
}


if (__name__ == "__main__"):
    e_code = start()
    exit(e_code)
