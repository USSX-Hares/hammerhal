from hammerdraw.generator.generator_base import GeneratorBase

class AdversaryGenerator(GeneratorBase):
    generator_type = 'adversary'

    def __init__(self):
        from hammerdraw.compilers import AdversaryCompiler as CompilerClass
        self.attached_class = CompilerClass
        super().__init__()
