from hammerdraw.generator.generator_base import GeneratorBase

class CardGenerator(GeneratorBase):
    generator_type = 'card'

    def __init__(self):
        from hammerdraw.compilers import CardCompiler as CompilerClass
        self.attached_class = CompilerClass
        super().__init__()
