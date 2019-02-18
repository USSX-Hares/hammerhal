import string
from typing import Iterable, TypeVar, List, Sequence, Callable, Union, Any

def capitalize_first(s: str) -> str:
    if (len(s) > 0):
        return s[0].upper() + s[1:]
    return s

def decapitalize_first(s: str) -> str:
    if (len(s) > 0):
        return s[0].lower() + s[1:]
    return s

def capitalize(s: str) -> str:
    return ' '.join(_word.capitalize() for _word in s.split(' '))

def decapitalize(s: str) -> str:
    return s.lower()

def capitalize_smart(s: str) -> str:
    return ' '.join(capitalize_first(_word) for _word in s.split(' '))

def decapitalize_smart(s: str) -> str:
    return ' '.join(decapitalize_first(_word) for _word in s.split(' '))

# _sep_symbols = list(string.whitespace + string.punctuation + '«»')
# def capitalize_smart(s: str) -> str:
#     _s = s
#     for i in iter_index(s, _sep_symbols, method=index_of_any):
#         pass
# 
T = TypeVar('T')
def iter_index(seq: Sequence[T], element: T, start: int = None, end: int = None, *, method: Union[Callable[[Sequence[T], Any, int, int], int], str]='index') -> Iterable[int]:
    if (isinstance(method, str)):
        method = getattr(type(seq), method)
    if (start is None):
        start = 0
    if (end is None):
        end = len(seq)
    
    while True:
        try:
            i = method(seq, element, start, end)
        except ValueError:
            break
        else:
            yield i
            start = i + 1

def index_of_any(seq: Sequence[T], elements: Iterable[T], start: int = None, end: int = None) -> int:
    if (start is None):
        start = 0
    if (end is None):
        end = len(seq)
    
    _find = set(elements) 
    for i in range(start, end):
        x = seq[i]
        if (x in _find):
            return i
    
    raise ValueError("Elements not presented in sequence")

