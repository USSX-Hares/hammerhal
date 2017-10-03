from hammerhal.generator.generator_base import GeneratorBase

class AdversaryGenerator(GeneratorBase):
    generator_type = 'adversary'

    def __init__(self):
        from hammerhal.compilers import AdversaryCompiler as CompilerClass
        self.attached_class = CompilerClass
        super().__init__()
