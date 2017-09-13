import os, glob, sys
from fontTools import ttLib
from logging import getLogger
logger = getLogger('hammerhal.text_drawer.fond_finder')

# From
# https://github.com/gddc/ttfquery/blob/master/ttfquery/describe.py
# and
# http://www.starrhorne.com/2012/01/18/how-to-extract-font-names-from-ttf-files-using-python-and-our-old-friend-the-command-line.html
# and
# https://gist.github.com/pklaus/dce37521579513c574d0
# ported to Python 3
#
# Heavily modified for font-finding & cross-platform by USSX.Hares / Peter Zaitcev


class FontFinder:

    __FONT_SPECIFIER_NAME_ID = 4
    __FONT_SPECIFIER_FAMILY_ID = 1

    cached = {}
    __in_cache = set()

    @staticmethod
    def get_font_name(font):
        if (isinstance(font, str)):
            if (os.path.isfile(font)):
                _path = font
            # elif (os.path.isfile('C:\\Windows\\Fonts\\' + font)):
            #     _path = os.path.isfile('C:\\Windows\\Fonts\\' + font)
            else:
                logger.error("Cannot open font file: {font_path}".format(font_path=_path))
                raise FileNotFoundError

            logger.debug("Openning font {path}".format(path=_path))
            _font_obj = ttLib.TTFont(_path)
        else:
            _font_obj = font

        # Get the short name from the font's names table
        name = None
        family = None
        for record in _font_obj['name'].names:
            if (b'\x00' in record.string):
                name_str = record.string.decode('utf-16-be')
            else:
                name_str = record.string.decode('utf-8')

            if (record.nameID == FontFinder.__FONT_SPECIFIER_NAME_ID and not name):
                name = name_str
            elif (record.nameID == FontFinder.__FONT_SPECIFIER_FAMILY_ID and not family):
                family = name_str

            if (name and family):
                break

        logger.debug("Font detected: {name} from {family}".format(name=name, family=family))
        return name, family

    @staticmethod
    def get_fonts_directories():
        if (os.name == 'nt'):
            return [ os.path.join(os.environ['WINDIR'], 'Fonts') ]
        elif (os.name == 'posix'):
            return \
            [
                '/usr/share/fonts',
                '/usr/local/share/fonts',
                os.environ['HOME'] + '/.fonts',
                '/usr/X11R6/lib/X11/fonts',
                '/usr/share/X11/fonts/Type1',
                '/usr/share/X11/fonts/OTF',
            ]
        else:
            return []

    @staticmethod
    def __verify_font(lower_font_name, bold, italic):
        return (('bold' in lower_font_name) == bold) and (('italic' in lower_font_name) == italic)

    def find_font_file(self, family_name, bold=False, italic=False):
        if (family_name in self.cached):
            for lower_font_name in self.cached[family_name]:
                if (FontFinder.__verify_font(lower_font_name, bold, italic)):
                    logger.debug("Font info restored from cache: {path}".format(path=self.cached[family_name][lower_font_name]))
                    return self.cached[family_name][lower_font_name]

        result = self.__find_and_cache(validate=True, family_name=family_name, bold=bold, italic=italic)
        if (result):
            logger.debug("Font found by direct search: {path}".format(path=result))
            return result

        return None


    def cache_all(self):
        self.__find_and_cache(validate=False)

    def __find_and_cache(self, validate, family_name=None, bold=False, italic=False):
        for font_dir in FontFinder.get_fonts_directories():
            all_fonts = glob.glob(font_dir + '/*')
            for font_path in all_fonts:
                if not (font_path in self.__in_cache):
                    logger.debug("Trying to open {font_path}".format(font_path=font_path))
                    try:
                        _name, _family_name = FontFinder.get_font_name(font_path)
                    except:
                        # logger.warning("Cannot parse font file: {font_path}".format(font_path=font_path))
                        pass
                    else:
                        lower_font_name = _name.lower()
                        if (not _family_name in self.cached):
                            self.cached[_family_name] = { lower_font_name: font_path }
                        else:
                            self.cached[_family_name][lower_font_name] = font_path

                        if (validate):
                            if (_family_name == family_name and FontFinder.__verify_font(lower_font_name, bold, italic)):
                                return font_path

                    self.__in_cache.add(font_path)

        return None

# def test_fonts():
#     ff = FontFinder()
#     x2 = ff.find_font_file('Times New Roman', bold=True)
#     x = ff.find_font_file('Arial')
#     # import json
#     # print(json.dumps(ff.cached, sort_keys=True, indent=4))
#     print(x)
#     print(x2)

# def test_fonts():
#     import matplotlib.font_manager as font_manager
#     import pygame
#
#     pygame.font.init()
#
#     print(font_manager.findfont('Segoe UI'))
#     print(pygame.font.match_font('Segoe UI'))
#     print(font_manager.findfont('Arial'))
#     print(pygame.font.match_font('Arial'))