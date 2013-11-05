# coding: utf-8

#============================================================================#
class jsDict(dict):
    """jsDict is like a js-object.
        >>> o = jsDict(a=1)
        >>> o.a
        1
        >>> o['a']
        1
        >>> o.a = 2
        >>> o['a']
        2
        >>> del o.a
        >>> o.a
        Traceback (most recent call last):
            ...
        AttributeError: 'a'
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self): return '<jsDict ' + dict.__repr__(self) + '>'

#==============================================================================
if __name__ == "__main__":
    x = jsDict(a=1, w=2)
    print x
