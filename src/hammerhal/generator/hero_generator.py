from hammerhal.generator.generator_base import GeneratorBase

class HeroGenerator(GeneratorBase):
    generator_type = 'hero'

    def __init__(self):
        from hammerhal.compilers import HeroCompiler as CompilerClass
        self.attached_class = CompilerClass
        super().__init__()
