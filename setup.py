from setuptools import setup
import os

_dirs = \
[
    'logs',
    'output',
    'output/heroes',
    'output/adversaries',
]

for _dir in _dirs:
    if (not os.path.isdir(_dir)):
        os.makedirs(_dir)


setup \
(
    name='hammerhal',
    version='0.1',
    install_requires =
    [
        'jsonschema',
        'Pillow',
        'fontTools',
    ],
    packages =
    [
        'hammerhal',
        'hammerhal.diftool',
        'hammerhal.compilers',
        'hammerhal.generator',
        'hammerhal.text_drawer',
        'shared_funcs',
    ],
    package_dir={ '': 'src' },
    url='https://github.com/USSX-Hares/hammerhal',
    license='MIT',
    author='USSX Hares / Peter Zaitcev',
    author_email='USSX.Hares@yandex.ru',
    description='Tools for card generation in Warhammer Quest: Shadow over Hammerhal'
)
