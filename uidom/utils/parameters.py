# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import inspect
from typing import Callable, Type

# from collections import OrderedDict as Odict


__all__ = ["Parameters"]

Odict: Type[dict] = dict
# replaced dict with old Ordered dict as that is totally ordered by default since py 3.8

PARAM = inspect.Parameter
PARAM_KINDS: dict = {
    "ARGS": [PARAM.POSITIONAL_ONLY, PARAM.POSITIONAL_OR_KEYWORD, PARAM.VAR_POSITIONAL],
    "KWARGS": [PARAM.KEYWORD_ONLY, PARAM.VAR_KEYWORD],
}


def _parameters(func_signature):
    def get_parameters(args: bool = False, kwargs: bool = False):
        def get(param_kind):
            nonlocal func_signature
            return filter(
                lambda tup: (tup[1].name, tup[1])
                if tup[1].kind in PARAM_KINDS[param_kind]
                else None,
                func_signature.parameters.items(),
            )

        _args = list(get("ARGS"))
        _kwargs = list(get("KWARGS"))

        _args_only = list(tup for tup in _args if tup[1].kind is PARAM_KINDS["ARGS"][0])
        args_only = list(
            (k, v.default)
            if v.default is not inspect.Parameter.empty
            else (k, None)
            if k not in ("self", "mcs", "cls")
            else (k, k)
            for (k, v) in _args_only
        )

        _args_p = list(tup for tup in _args if tup[1].kind is PARAM_KINDS["ARGS"][1])
        args_p = list(
            (k, v.default)
            if v.default is not inspect.Parameter.empty
            else (k, None)
            if k not in ("self", "mcs", "cls")
            else (k, k)
            for (k, v) in _args_p
        )

        var_args = list(
            (tup[0], ()) for tup in _args if tup[1].kind is PARAM_KINDS["ARGS"][2]
        )
        _args = (args_only + args_p, *var_args)

        kw_only = (tup for tup in _kwargs if tup[1].kind is PARAM_KINDS["KWARGS"][0])
        kw_only: dict = Odict(
            (k, v.default)
            if v.default is not inspect.Parameter.empty
            else (k, None)
            if k not in ("self", "mcs", "cls")
            else (k, k)
            for (k, v) in kw_only
        )

        var_kwargs: list = [
            (tup[0], {}) for tup in _kwargs if tup[1].kind is PARAM_KINDS["KWARGS"][1]
        ]
        _kwargs = (Odict(**kw_only), *var_kwargs)

        if all([args, kwargs]):
            return _args, _kwargs
        elif not args and kwargs:
            return (), _kwargs
        elif not kwargs and args:
            return _args, {}
        else:
            return (), {}

    return get_parameters


class Parameters(object):
    empty = inspect.Parameter.empty

    def __init__(
        self,
        func: Callable,
        args: bool = True,
        kwargs: bool = True,
        in_single_kwargs: bool = True,
    ):
        self._func_signature = inspect.signature(func)
        self._in_single_kwargs = in_single_kwargs
        self._args, self._kwargs = _parameters(self._func_signature)(
            args=args, kwargs=kwargs
        )

        self._p_args = None
        self._v_args = None
        self._p_kwargs = None
        self._v_kwargs = None
        self._params = self()
        self._annotation = Odict(
            {
                param: self._func_signature.parameters[param].annotation
                for param in self._params.keys()
            }
            if not isinstance(self._params, tuple)
            else {
                param: self._func_signature.parameters[param].annotation
                for _dict in self._params
                for param in _dict
            }
        )

    @property
    def pos_arg(self):
        p_arg, _ = self.args
        return p_arg

    @property
    def var_arg(self):
        _, v_arg = self.args
        return v_arg

    @property
    def var_arg_name(self):
        var_arg_name = ""
        _, var_arg = self.args
        if any(var_arg):
            (var_arg,) = var_arg
            var_arg_name = var_arg[0]
        return var_arg_name

    @property
    def args(self):
        if len(self._args) > 1:
            self._p_args = self._args[0]
            self._v_args = self._args[1]
            return self._p_args, [self._v_args]
        (_args,) = self._args if any(self._args) else ((),)
        return _args, ()

    @property
    def kwargs(self):
        if len(self._kwargs) > 1:
            self._p_kwargs = self._kwargs[0]
            self._v_kwargs = self._kwargs[1]
            return Odict(self._p_kwargs), Odict([self._v_kwargs])

        (_kwargs,) = self._kwargs if any(self._kwargs) else ({},)
        return Odict(**_kwargs), {}

    @property
    def parameters(self):
        return self._params

    @property
    def annotations(self):
        return self._annotation

    @property
    def signature(self):
        return self._func_signature

    def default(self, param_name):
        return self.signature.parameters[param_name].default

    def __str__(self):
        return str(self.parameters)

    def __call__(self):
        in_single_kwarg = self._in_single_kwargs
        (p_arg, v_arg), (p_kwarg, v_kwarg) = self.args, self.kwargs
        if all([v_arg is not None, v_kwarg is not None]):
            if not in_single_kwarg:
                return Odict(**Odict(p_arg), **Odict(v_arg)), Odict(
                    **p_kwarg, **v_kwarg
                )
            return Odict(
                **Odict(**Odict(p_arg), **Odict(v_arg)), **Odict(**p_kwarg, **v_kwarg)
            )

        elif v_arg is not None and v_kwarg:
            if not in_single_kwarg:
                return Odict(**Odict(p_arg)), Odict(**p_kwarg, **v_kwarg)
            return Odict(**Odict(**Odict(p_arg)), **Odict(**p_kwarg, **v_kwarg))

        elif v_kwarg is not None and v_arg:
            if not in_single_kwarg:
                return Odict(**Odict(p_arg), **Odict(v_arg)), Odict(**p_kwarg)
            return Odict(**Odict(**Odict(p_arg), **Odict(v_arg)), **Odict(**p_kwarg))

        else:
            if not in_single_kwarg:
                return Odict(**Odict(p_arg)), Odict(**p_kwarg)
            return Odict(**Odict(**Odict(p_arg)), **Odict(**p_kwarg))


if __name__ == "__main__":

    def kwarg(name="xyz", **kwargs):
        pass

    def arg(_arg, parg=None, *varg):
        pass

    arg_param = Parameters(arg)
    print(arg_param.args)
    print(arg_param.pos_arg)
    print(arg_param.var_arg)
