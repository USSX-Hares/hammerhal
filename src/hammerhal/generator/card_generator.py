from hammerhal.generator.generator_base import GeneratorBase

class CardGenerator(GeneratorBase):
    generator_type = 'card'

    def __init__(self):
        from hammerhal.compilers import CardCompiler as CompilerClass
        self.attached_class = CompilerClass
        super().__init__()
