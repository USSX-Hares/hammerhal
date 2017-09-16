__positive = [ 'y', 'yes', 'true', '+', 'positive' ]
__negative = [ 'n', 'no', 'false', '-', 'negative' ]

def yn_input(message="Confirm:"):
    result = None
    _yn = "y/n"
    mask = "{message} ({yn}) "
    while (result is None):
        _message = mask.format(message=message, yn=_yn)
        print(_message, end='')
        test = input().lower()
        if (test in __positive):
            return True
        if (test in __negative):
            return False
        mask = "Please, type {yn}"


