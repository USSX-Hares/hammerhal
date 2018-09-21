try:
    __generator_supported_temp = generator_supported
except NameError:
    __generator_supported_temp = None

if (__generator_supported_temp is None):
    from logging import getLogger as __get_logger
    __looger = __get_logger("hammerdraw.generator")
    try:
        import clr
        clr.AddReference("System.Windows.Forms")
        import System
        from System.Windows.Forms import Form, Application
    except (ImportError, NameError):
        generator_supported = False
        __looger.warning("Generator is not supported, skipping dependency")
    else:
        generator_supported = True
        __looger.info("Generator supported, ready to import")

from hammerdraw.generator.generator_error import GeneratorError, GeneratorNotSupported
if (generator_supported):
    from hammerdraw.generator.input_control import InputControl
    from hammerdraw.generator.generator_base import GeneratorBase
    from hammerdraw.generator.adversary_generator import AdversaryGenerator
    from hammerdraw.generator.hero_generator import HeroGenerator
    from hammerdraw.generator.card_generator import CardGenerator
