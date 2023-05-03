# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import types
import typing

__all__ = ["map_recursive", "apply_to_list", "apply_to_dict", "apply_to_tuple"]

iter_types = typing.Iterable, typing.Iterator, typing.Mapping


def f(value, key=None):
    return value if key is None else key, value


def apply_to_list(elem_func, iterable, obj_func=None):
    obj_func = obj_func or f
    return list(
        apply_to_frozenset(elem_func, item, obj_func)
        if isinstance(item, frozenset)
        else apply_to_set(elem_func, item, obj_func)
        if isinstance(item, set)
        else apply_to_list(elem_func, item, obj_func)
        if isinstance(item, list)
        else apply_to_tuple(elem_func, item, obj_func)
        if isinstance(item, tuple)
        else apply_to_dict(elem_func, item, obj_func)
        if isinstance(item, dict)
        else elem_func(item)
        for item in iterable
    )


def apply_to_tuple(elem_func, iterable, obj_func=None):
    obj_func = obj_func or f
    return tuple(
        apply_to_frozenset(elem_func, item, obj_func)
        if isinstance(item, frozenset)
        else apply_to_set(elem_func, item, obj_func)
        if isinstance(item, set)
        else apply_to_tuple(elem_func, item, obj_func)
        if isinstance(item, tuple)
        else apply_to_list(elem_func, item, obj_func)
        if isinstance(item, list)
        else apply_to_dict(elem_func, item, obj_func)
        if isinstance(item, dict)
        else elem_func(item)
        for item in iterable
    )


def apply_to_dict(elem_func, iterable, obj_func=None):
    obj_func = obj_func or f
    return dict(
        obj_func(apply_to_frozenset(elem_func, item, obj_func), key)
        if isinstance(item, frozenset)
        else obj_func(apply_to_set(elem_func, item, obj_func), key)
        if isinstance(item, set)
        else obj_func(apply_to_tuple(elem_func, item, obj_func), key)
        if isinstance(item, tuple)
        else obj_func(apply_to_list(elem_func, item, obj_func), key)
        if isinstance(item, list)
        else obj_func(apply_to_dict(elem_func, item, obj_func), key)
        if isinstance(item, dict)
        else obj_func(elem_func(item), key)
        for key, item in iterable.items()
    )


def apply_to_set(elem_func, iterable, obj_func=None):
    obj_func = obj_func or f
    return set(
        apply_to_frozenset(elem_func, item, obj_func)
        if isinstance(item, frozenset)
        else apply_to_set(elem_func, item, obj_func)
        if isinstance(item, set)
        else apply_to_tuple(elem_func, item, obj_func)
        if isinstance(item, tuple)
        else apply_to_list(elem_func, item, obj_func)
        if isinstance(item, list)
        else apply_to_dict(elem_func, item, obj_func)
        if isinstance(item, dict)
        else elem_func(item)
        for item in iterable
    )


def apply_to_frozenset(elem_func, iterable, obj_func=None):
    obj_func = obj_func or f
    return frozenset(
        apply_to_frozenset(elem_func, item, obj_func)
        if isinstance(item, frozenset)
        else apply_to_set(elem_func, item, obj_func)
        if isinstance(item, set)
        else apply_to_tuple(elem_func, item, obj_func)
        if isinstance(item, tuple)
        else apply_to_list(elem_func, item, obj_func)
        if isinstance(item, list)
        else apply_to_dict(elem_func, item, obj_func)
        if isinstance(item, dict)
        else elem_func(item)
        for item in iterable
    )


def map_recursive(elem_func, iterable, obj_func=None):
    obj_func = obj_func or f
    if isinstance(iterable, dict):
        return apply_to_dict(elem_func, iterable, obj_func)
    if isinstance(iterable, list):
        return apply_to_list(elem_func, iterable, obj_func)
    if isinstance(iterable, tuple):
        return apply_to_tuple(elem_func, iterable, obj_func)
    if isinstance(iterable, set):
        return apply_to_set(elem_func, iterable, obj_func)
    if isinstance(iterable, frozenset):
        return apply_to_frozenset(elem_func, iterable, obj_func)
    if isinstance(iterable, types.GeneratorType):
        return (map_recursive(elem_func, item, obj_func) for item in iterable)
    return elem_func(iterable)


def map_r(func, iterables):
    return (map_recursive(func, iterable) for iterable in iterables)


def zip_recursive(iterables):
    # TODO make this function
    pass


#
# def _test_dict_map():
#     return map_recursive(
#         lambda x: x if isinstance(x, int) else None,
#         {"prices": [1, [2, [3.0], (9.0, 5)]]},
#     )
#
#
# def _test_generator():
#     return map_recursive(
#         lambda x: x if isinstance(x, int) else None,
#         ({"prices": [1, [2, [3.0], (9.0, 5)]]} for _ in range(3)),
#     )
#
#
# def _test_isinstance(d, f2=None):
#     return map_recursive(lambda x: x if x > 6 else None, d, f2)
#
#
# data1 = (
#     1,
#     {"prices": [(2.0, 3.0), (4.6, 5.6)], "weight": [9.0], "model": [5]},
#     {"prices": [2.0, 3.0], "weight": [9.0, 10.0], "model": [5]},
# )
#
# _ = lambda x: x ** 2
# __ = lambda v, k=None: (k.upper(), v) if k is not None else v
#
# if __name__ == "__main__":
#     data = [[2, 4, 8]]
#     print(map_recursive(_, *data))
#     print(_test_isinstance(data1, __))
