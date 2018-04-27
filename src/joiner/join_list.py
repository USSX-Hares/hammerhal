def join_list(list:list, separator:str=', ', last_separator:str=None, formatter:callable="{0}".format) -> str:
    if (not list):
        return ""

    if (last_separator is None):
        last_separator = separator

    if (isinstance(formatter, str)):
        formatter = formatter.format
    list_str = [ formatter(x) for x in list ]

    if (len(list) == 1):
        result = list_str[0]
    else:
        result = "{leadingItems}{lastSeparator}{lastItem}".format(leadingItems=separator.join(list_str[:-1]), lastSeparator=last_separator, lastItem=list_str[-1])

    return result
