class CompilerError(Exception):
    pass

class InvalidConfigError(CompilerError):
    pass

class CompilerWarning(Warning):
    pass

class TextNotFitInAreaWarning(CompilerWarning):

    module = None
    module_name = None

    field_name = None
    field_text = None

    required_size = None
    actual_size = None

    def __init__(self, message=None, **kwargs):
        """
        Initializes a new instance of TextNotFitInAreaWarning.
        :param message: Ignores all optional arguments and rewrites the full message text.
        :param kwargs: Available options:
          - module/module_name: a module or its name where an error has occurred.
          - filed/text: a field in raw file or its text led to warning.
          - actual_size/required_size: a (x,y) tuple of resulting/available size of text area.
          - comment: a comment appended to the end.
        """

        _template = "{module_prefix}{text} does not fit in {area}.{comment}"

        _module_prefix = ""
        self.module = kwargs.get('module', None)
        self.module_name = kwargs.get('module_name', None) or (self.module and self.module.human_readable_name) or None
        if (self.module_name):
            _module_prefix = "Module {module_name}: ".format(module_name=self.module_name)

        _text = "Text"
        self.field_name = kwargs.get('field', None)
        self.field_text = kwargs.get('text', None) or (self.module and self.module.parent.raw.get(self.field_name, None)) or None
        if (self.field_name):
            _text += " of field '{field}'".format(field=self.field_name)
        if (self.field_text):
            _text += " ('{text}')".format(field=self.field_name, text=self.field_text)

        _area = "area"
        self.actual_size = kwargs.get('actual_size', None)
        self.required_size = kwargs.get('required_size', None)
        if (self.actual_size or self.required_size):
            _append = " ("
            if (self.required_size):
                _append += " (required: {required_size})".format(required_size=self.required_size)
            if (self.actual_size):
                _append += " (actual: {actual_size})".format(actual_size=self.actual_size)
            _append += ")"

            _area += _append

        _comment = ''
        if ('comment' in kwargs):
            _comment = " {comment}".format(**kwargs)

        if (not message is None):
            msg = message
        else:
            msg = _template.format(module_prefix=_module_prefix, text=_text, area=_area, comment=_comment)

        super().__init__(msg)
