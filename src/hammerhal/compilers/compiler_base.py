import json
import jsonschema.exceptions
from jsonschema import validate
from PIL import Image

from hammerhal import ConfigLoader
from logging import getLogger
logger = getLogger('hammerhal.compilers.compiler_base')

class CompilerBase():

    compiler_type = None
    schema_path = None
    raw_directory = None
    output_directory = None
    output_name = None

    raw = None
    compiled = None

    def __init__(self):
        self.schema_path = "{directory}{type}.json".format(directory=ConfigLoader.get_from_config('schemasDirectory', 'compilers'), type=self.compiler_type)
        self.raw_directory = "{rawRoot}{rawOffset}".format(rawRoot=ConfigLoader.get_from_config('rawDirectoryRoot'), rawOffset=ConfigLoader.get_from_config('compilerTypeSpecific/{type}/rawDirectory'.format(type=self.compiler_type), 'compilers'))
        self.output_directory = "{rawRoot}{rawOffset}".format(rawRoot=ConfigLoader.get_from_config('outputDirectoryRoot', 'compilers'), rawOffset=ConfigLoader.get_from_config('compilerTypeSpecific/{type}/outputDirectory'.format(type=self.compiler_type), 'compilers'))

    def search(self, name):
        # Temporary decision
        return "{directory}{name}.json".format(directory=self.raw_directory, name=name)

    def open(self, name):
        filename = self.search(name)
        logger.info("Reading {filename}...".format(filename=filename))
        file = open(filename)
        raw = json.load(file)
        file.close()
        
        filename = self.schema_path
        logger.debug("Reading {filename}...".format(filename=filename))
        file = open(filename)
        schema = json.load(file)
        file.close()

        try:
            logger.debug("Validating {name}...".format(name=name))
            validate(raw, schema)
        except jsonschema.exceptions.ValidationError:
            logger.error("Raw file is not valid")
            self.raw = None
        else:
            logger.debug("Raw file is valid")
            self.raw = raw

        return self.raw

    def compile(self):
        raise NotImplementedError

    def save(self):
        if (not self.compiled):
            logger.error("Could not save not compiled result")
            return None

        name = self.output_name or self.raw.get('name', None)
        if (not name):
            logger.error("Could find proper name")
            return None

        filename = "{directory}{name}.png".format(directory=self.output_directory, name=name)
        try:
            logger.debug("Saving compiled file: {filename}".format(filename=filename))
            self.compiled.save(filename)
        except:
            logger.exception("Error while saving file {filename}".format(filename=filename))
            return None
        else:
            return filename
