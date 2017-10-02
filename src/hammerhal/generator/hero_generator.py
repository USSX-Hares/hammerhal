from hammerhal.generator.generator_base import GeneratorBase

class HeroGenerator(GeneratorBase):
    generator_type = 'hero'

    def __init__(self):
        from hammerhal.compilers.hero_compiler import HeroCompiler
        self.attached_class = HeroCompiler
        super().__init__()
