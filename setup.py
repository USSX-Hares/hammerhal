from setuptools import setup
import os

_dirs = \
[
    'logs',
    'output',
]

for _dir in _dirs:
    if (not os.path.isdir(_dir)):
        os.makedirs(_dir)


setup \
(
    name='hammerdraw',
    version='0.3',
    install_requires =
    [
        'jsonschema',
        'Pillow',
        'fontTools',
        'camel-case-switcher>=1.2',
        'yn-input',
    ],
    extra_requires =
    {
        'GeneratorFeature': [ 'pythonnet' ],
    },
    packages =
    [
        'hammerdraw',
        'hammerdraw.diftool',
        'hammerdraw.compilers',
        'hammerdraw.generator',
        'hammerdraw.text_drawer',
    ],
    package_dir={ '': 'src' },
    url='https://github.com/USSX-Hares/hammerdraw',
    license='MIT',
    author='USSX Hares / Peter Zaitcev',
    author_email='USSX.Hares@yandex.ru',
    description='Tools for card generation in Warhammer Quest: Shadow over hammerdraw'
)
