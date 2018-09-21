import json
import os
from logging import getLogger
from functools import reduce

logger = getLogger('hammerdraw.config_loader')


class ConfigLoader:
    __active_configs = {}
    __config_locations = {}
    __main_config_key = 'main'
    __main_config_path = 'configs/hammerdraw.json'

    @staticmethod
    def __find_element_in_dict_object(dict_object:dict, key_path:str):
        try:
            return reduce(lambda d, key: d[key], key_path.split('/'), dict_object)
        except KeyError:
            return None

    # @staticmethod
    # def __load_config(config_path, config_key, logging_enabled):

    @staticmethod
    def __load_main_config(main_config_path:str=None):
        logger.info("Loading main configuration")
        if (main_config_path):
            logger.debug("Overriding default config path: {configPath}".format(configPath=main_config_path))
            ConfigLoader.__main_config_path = main_config_path

        logger.debug("Config is used: {configPath}".format(configPath=ConfigLoader.__main_config_path))
        try:
            main_config_file = open(ConfigLoader.__main_config_path)
            main_config = json.load(main_config_file)
        except (FileNotFoundError, json.JSONDecodeError):
            message = "Critical error. Cannot read configuration file. Exiting now."
            logger.critical(message, exc_info=True)
            exit(1)
        else:
            main_config_file.close()

        logger.debug(json.dumps(main_config, indent=4, sort_keys=True))
        ConfigLoader.__active_configs[ConfigLoader.__main_config_key] = main_config
        ConfigLoader.__config_locations[ConfigLoader.__main_config_key] = ConfigLoader.__main_config_path
        logger.debug("Main config loaded successfully")

    @staticmethod
    def __load_config(key, path) -> bool:
        try:
            logger.info("Loading configuration: '{key}' -> {path}".format(key=key, path=path))

            config_file = open(path)
            config = json.load(config_file)
            config_file.close()

            logger.debug(json.dumps(config, indent=4, sort_keys=True))
            ConfigLoader.__active_configs[key] = config
            ConfigLoader.__config_locations[key] = path
            logger.debug("Config '{key}' loaded successfully".format(key=key))
            return True

        except:
            logger.error('Error while loading configuration', exc_info=True)
            return False

    @staticmethod
    def reload_config(config_name:str) -> bool:
        if (config_name in ConfigLoader.__config_locations):
            old_config = ConfigLoader.__active_configs[config_name]
            if (not ConfigLoader.__load_config(config_name, ConfigLoader.__config_locations[config_name])):
                ConfigLoader.__active_configs[config_name] = old_config
                return False
            else:
                return True

        return False

    @staticmethod
    def reload_configs():
        for config_name in ConfigLoader.__active_configs:
            ConfigLoader.reload_config(config_name)

    @staticmethod
    def load_configs(main_config_path:str=None):
        ConfigLoader.__load_main_config(main_config_path)
        config_dir = ConfigLoader.get_from_config('configDirectory')
        ConfigLoader.__load_config('compilers', config_dir + ConfigLoader.get_from_config('compilersConfig'))
        for _filename in os.listdir("{config_dir}/compilers".format(config_dir=config_dir)):
            compiler_name, _, tail = _filename.rpartition('.json')
            if (not tail):
                ConfigLoader.__load_config("compiler:{compiler_name}".format(compiler_name=compiler_name), path="{config_dir}/compilers/{config_filename}".format(config_dir=config_dir, config_filename=_filename))

    @staticmethod
    def get_from_config(path: str, config_name: str='main'):
        if (config_name in ConfigLoader.__active_configs):
            return ConfigLoader.__find_element_in_dict_object(ConfigLoader.__active_configs[config_name], path)
        return None
