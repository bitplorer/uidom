# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


__all__ = ["Element", "Sheet"]

VALUES_LINKED = list()


def link_values(list_a, list_b, values_linked: list = None or VALUES_LINKED):
    if not all(
            (isinstance(v, (tuple, list)) and len(v) == 2) for v in (list_a, list_b)
    ):
        raise TypeError(f"pass values as list or tuple")

    if not all(
            isinstance(v[0], Element) or isinstance(v[1], str) for v in (list_a, list_b)
    ):
        raise TypeError(
            f"not all values are of "
            f"[{Element.__name__}, {type(str).__name__}] types"
        )
    list_a = list(list_a)
    list_b = list(list_b)
    values_linked.append([list_a, list_b])


class Element(dict):
    values_linked = list()

    def __init__(self, **kwargs):
        super(Element, self).__init__(**kwargs)

    def link_values(self, attr, element, elem_attr):
        link_values([self, attr], [element, elem_attr], values_linked=self.values_linked)

    def __getattr__(self, item):
        return super(Element, self).__getitem__(item)

    def __missing__(self, key):
        return key

    def __setattr__(self, key, value):
        super(Element, self).__setitem__(key, value)
        for lst in self.values_linked:
            if [self, key] in lst:
                idx = lst.index([self, key])
                this = lst.pop(idx)
                other = lst.pop(0)
                other[0][other[1]] = value
                lst.extend([this, other])

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __str__(self):
        return str(dict(super(Element, self).items()))

    def __repr__(self):
        return f"{type(self).__qualname__}({self.__str__()})"

    def __dir__(self):
        return super().__dir__()


class FieldError(Exception):
    pass


class FieldToElementsMeta(type):
    def __new__(mcs, name, bases, namespace):  # NOQA
        _conflicting_fields = dict()
        for base in bases:
            if all(
                    [
                        any([base.__dict__.get("fields", None)]),
                        any([namespace.get("fields", None)]),
                    ]
            ):
                for f in namespace.get("fields"):
                    if f in base.__dict__.get("fields"):
                        if base not in _conflicting_fields:
                            _conflicting_fields[base] = list()
                        _conflicting_fields[base].append(f)

                for f in base.__dict__.get("fields"):
                    if not hasattr(base, f):
                        setattr(base, f, Element())
                    else:
                        if not isinstance(getattr(base, f), Element):
                            raise AttributeError(
                                f"{getattr(base, f)!r} must be instance of {Element!r}"
                            )

        if any(_conflicting_fields):
            raise FieldError(
                "conflicting fields found in {cf}".format(cf=_conflicting_fields)
            )
        return super(FieldToElementsMeta, mcs).__new__(mcs, name, bases, namespace)

    def __init_subclass__(mcs, **kwargs):
        if any([getattr(mcs, "fields", None)]):
            for f in getattr(mcs, "fields"):
                if not hasattr(mcs, f):
                    setattr(mcs, f, Element())
                else:
                    if not isinstance(getattr(mcs, f), Element):
                        raise AttributeError(
                            f"{getattr(mcs, f)!r} must be instance of {Element!r}"
                        )


class KeyToElementsAtrBase(object):
    def __getitem__(self, item):
        return self.__getattr__(item)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __setattr__(self, key, value):
        if key in type(self).__dict__ or key in self.__dict__:
            raise AttributeError(f"attribute [{key}] already exists")
        object.__setattr__(self, key, value)

    def __getattr__(self, item):
        if item not in type(self).__dict__:
            if item not in self.__dict__:
                object.__setattr__(self, item, Element())
            return self.__dict__[item]
        return type(self).__dict__[item]

    def __contains__(self, item):
        return hasattr(self, item)

    def __repr__(self):
        return repr(
            {i: f"{self.__dict__[i]!s}" for i in self.__dict__ if not i.startswith("_")}
        )


class Sheet(KeyToElementsAtrBase, metaclass=FieldToElementsMeta):
    def __init__(self, *args):
        self._args = args

    def __iter__(self):
        return iter(self._args)

    def __init_subclass__(cls, *args):
        super(Sheet, cls).__init__(cls, *args)

    def __dir__(self):
        return sorted(i for i in self.__dict__ if not i.startswith("_"))


class HeaderSheet(Sheet):
    fields = ["charset", "description", "lang", "link", "title", "viewport"]

