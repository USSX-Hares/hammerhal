from hammerdraw.compilers import CompilerBase
from logging import getLogger
logger = getLogger('hammerdraw.compilers.core.base_compiler')

class BaseCompiler(CompilerBase):
    compiler_type = "base-compiler"
    
    def open(self, *args, **kwargs):
        self.raw = dict(name=self.compiler_type)
        return self.raw
