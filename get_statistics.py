import json

from hammerdraw import ConfigLoader
from hammerdraw.preloads import setup_logging
from hammerdraw.compilers.warhammer_quest import HeroCompiler, CardCompiler

def main():
    from logging import getLogger
    setup_logging()
    logger = getLogger('hammerdraw')
    logger.setLevel('WARNING')
    ConfigLoader.load_configs()

    heroes_stat = get_heroes_stat()
    all_traits = list(heroes_stat['traits'].keys())

    skill_stat = get_skills_stat(all_traits)
    treasures_stat = get_treasures_stat()

    if (print_result):
        print()
        print("Heroes Info:")
        print(json.dumps(heroes_stat, indent=4, sort_keys=True))

        print()
        print("Skills Info:")
        print(json.dumps(skill_stat, indent=4, sort_keys=True))

        print()
        print("Treasures Info:")
        print(json.dumps(treasures_stat, indent=4, sort_keys=True))


def get_heroes_stat():
    compiler = HeroCompiler()
    heroes_stat = { 'traits': dict(), 'total_count': 0 }

    all_heroes = compiler.search(ignore_dummies=False)
    for filename in all_heroes:
        traits = get_hero_info(compiler, filename)
        for _trait in traits:
            trait = _trait.capitalize()
            heroes_stat['traits'][trait] = heroes_stat['traits'].get(trait, 0) + 1
        heroes_stat['total_count'] += 1

    return heroes_stat

def get_hero_info(compiler:HeroCompiler, filename:str):
    compiler.open(filename)
    name = compiler.raw.get('name')
    traits = compiler.raw.get('traits', None) or [ 'no trait' ]
    for _to_find in find_heroes:
        if (_to_find in traits):
            print("hero / {trait}: {hero}".format(trait=_to_find, hero=name))
    return traits


def get_skills_stat(all_traits=[], all_categories=[]):

    _all_traits = all_traits + [ 'No trait' ]
    _all_categories = all_categories + [ 'No category' ]

    compiler = CardCompiler()
    set_info = dict()

    all_skills = compiler.search(type="skill", ignore_dummies=False)
    for filename in all_skills:
        resp = get_skill_info(compiler, filename)
        if (resp is None):
            continue
        set, affects, categories = resp
        if (not set in set_info):
            set_info[set] = { "perCategory": { category: 0 for category in _all_categories }, "perTrait": { trait: 0 for trait in _all_traits }, "totalCount": 0 }

        for _trait in affects:
            trait = _trait.capitalize()
            if (all_traits):
                set_info[set]["perTrait"][trait] += 1
            else:
                set_info[set]["perTrait"][trait] = set_info[set]["perTrait"].get(trait, 0) + 1

        for _category in categories:
            category = _category.capitalize()
            if (all_categories):
                set_info[set]["perCategory"][category] += 1
            else:
                set_info[set]["perCategory"][category] = set_info[set]["perCategory"].get(category, 0) + 1

        set_info[set]["totalCount"] += 1

    return set_info

def get_skill_info(compiler:CardCompiler, filename:str):
    compiler.open(filename)
    name = compiler.raw.get('name')
    set = compiler.raw.get('set')
    affects = compiler.raw.get('affects', None) or [ 'no trait' ]
    categories = compiler.raw.get('categories', None) or [ 'no category' ]

    if (not set in find_sets):
        return None

    for _to_find in find_skills:
        if (_to_find in affects):
            print("skill / {trait}: {skill} ({set})".format(trait=_to_find, skill=name, set=set))
        if (_to_find in categories):
            print("skill / {category}: {skill} ({set})".format(category=_to_find, skill=name, set=set))

    return set, affects, categories


def get_treasures_stat(all_categories=[], all_types=[]):

    _all_categories = all_categories + [ 'No category' ]
    _all_tpyes = all_categories + [ 'Other' ]

    compiler = CardCompiler()
    set_info = dict()

    all_treasures = compiler.search(type="treasure", ignore_dummies=False)
    for filename in all_treasures:
        resp = get_treasure_info(compiler, filename)
        if (resp is None):
            continue
        set, categories, item_type = resp
        if (not set in set_info):
            set_info[set] = { "perCategory": { category: 0 for category in _all_categories }, "perType": { item_type: 0 for item_type in _all_tpyes}, "totalCount": 0 }

        for _category in categories:
            category = _category.capitalize()
            if (all_categories):
                set_info[set]["perCategory"][category] += 1
            else:
                set_info[set]["perCategory"][category] = set_info[set]["perCategory"].get(category, 0) + 1

        item_type = item_type.capitalize()
        if (all_types):
            set_info[set]["perType"][item_type] += 1
        else:
            set_info[set]["perType"][item_type] = set_info[set]["perType"].get(item_type, 0) + 1

        set_info[set]["totalCount"] += 1

    return set_info

def get_treasure_info(compiler:CardCompiler, filename:str):
    compiler.open(filename)
    name = compiler.raw.get('name')
    set = compiler.raw.get('set')
    categories = compiler.raw.get('categories', None) or [ 'no category' ]
    item_type = compiler.raw.get('itemType', None) or 'other'

    if (not set in find_sets):
        return None

    for _to_find in find_treasures:
        if (_to_find in categories):
            print("treasure / {category}: {treasure} ({set})".format(category=_to_find, treasure=name, set=set))
        if (_to_find == item_type):
            print("treasure / {type}: {treasure} ({set})".format(type=_to_find, treasure=name, set=set))

    return set, categories, item_type


find_heroes = \
[
    # 'academic',
    # 'chaotic',
    # 'crazed',
    # 'swift',
    # 'totemic',
]

find_sets = \
[
    # 'silver-tower',
    # 'hammerdraw',
    'twilight-god',
]

find_skills = \
[
    # 'academic',
    # 'arcane',
    # 'chaotic',
    # 'crazed',
    # 'damage'
    # 'swift',
    # 'totemic',
]

find_treasures = \
[
    # 'reusable',
    # 'potion',
    # 'scroll',
]

print_result = True
# print_result = False

if (__name__ == '__main__'):
    main()
