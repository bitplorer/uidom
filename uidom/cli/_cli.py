# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import argparse
import typing as t
from functools import lru_cache
from inspect import _empty
from pathlib import Path
from typing import get_args

from typingx import isinstancex
from valio import Validator

from uidom.utils.functional import map_recursive
from uidom.utils.parameters import Parameters


class CLIValidator(Validator):
    def custom_type(self, value, type_: type):
        if not hasattr(type_, "__args__") and isinstance(type_, type):
            # Handle the case where the type is a single type
            return (
                map_recursive(lambda v: self._convert_value(v, type_), value)
                if value is not None
                else value
            )
        elif hasattr(type_, "__args__"):
            # Handle the case where the type is a Union, Optional, or generic type
            subtypes = get_args(type_)

            if len(subtypes) == 1:
                # Handle the case where the type is a List or Tuple with a single subtype
                subtype = subtypes[0]
                try:
                    return self.custom_type(value, subtype)
                except ValueError:
                    pass

            if type(None) in subtypes and len(subtypes) == 2:
                # Handle the case where the type is Optional[T]
                subtype = subtypes[0] if subtypes[0] != type(None) else subtypes[1]
                try:
                    return self.custom_type(value, subtype)
                except ValueError:
                    pass

            # Handle the case where the type is a Union[T1, T2, ...] with multiple subtypes

            for subtype in subtypes:
                try:
                    return self.custom_type(value, subtype)
                except ValueError:
                    pass
            raise ValueError(f"Value {value} is not a valid {type_}")
        else:
            raise ValueError(f"Type {type_} not supported")

    def _convert_value(self, value, type_: type):
        if type_ is bool:
            if str(value).lower() in ("yes", "true", "t", "y", "1"):
                return True
            elif str(value).lower() in ("no", "false", "f", "n", "0"):
                return False
            else:
                raise ValueError(f"Value {value} is not a valid {type_}")
        try:
            return type_(value) if type_ is not type(None) else value
        except TypeError:
            return value
        except ValueError:
            raise ValueError(f"Value {value} is not a valid {type_}")

    def pre_set(self, instance, value):
        value = self.custom_type(value=value, type_=self.annotation)
        return super().pre_set(instance, value)

    def __call__(self, value, instance=None):
        value = self.pre_set(value=value, instance=instance)
        return value

    def __hash__(self) -> int:
        return hash(self.annotation)

    def __instancecheck__(self, instance):
        return isinstancex(instance, self.annotation)


def cli(function: t.Callable, *args):
    parser, func_param = _func_to_argparse_and_param(function, add_subparsers=True)
    namespace = parser.parse_args(args)
    arg_dict, kwarg_dict = func_param.parameters
    var_arg_name = func_param.var_arg_name
    args_ = []
    for arg_name in list(arg_dict):
        arg_value = getattr(namespace, arg_name)
        if arg_name == var_arg_name:
            args_.extend(arg_value)
        else:
            args_.append(arg_value)
    kwargs = {kw: getattr(namespace, kw) for kw in kwarg_dict}
    if all([args_, kwargs]):
        return function(*args_, **kwargs)
    if args_:
        return function(*args_)
    if kwargs:
        return function(**kwargs)
    return function()


@lru_cache
def _func_to_argparse_and_param(
    function: t.Callable,
    arg_parser=argparse.ArgumentParser,
    add_subparsers: bool = False,
) -> tuple[argparse.ArgumentParser, Parameters]:
    # refer: https://pymotw.com/3/argparse/#mutually-exclusive-options
    func_param = Parameters(function, in_single_kwargs=False)
    func_name = function.__name__
    annotations = func_param.annotations
    arg_dict, kwarg_dict = func_param.parameters
    pos_arg, var_arg = func_param.args
    kw_only, var_kw = func_param.kwargs
    file = Path(function.__module__)
    if arg_parser is argparse.ArgumentParser:
        if function.__class__.__name__ != "function":
            description = (
                f"{file.parent.stem}.{file.stem}:{func_name}"[1:]
                if not function.__doc__
                else function.__doc__
            )
        else:
            func_name = function.__qualname__
            description = (
                f"{file.parent.stem}.{file.stem}:{func_name}"[1:]
                if not function.__doc__
                else function.__doc__
            )
        parser = arg_parser(prog=func_name, description=description)
    else:
        parser = arg_parser
    required_positional_only = parser.add_argument_group(
        f"{func_name}: POSITIONAL_ONLY"
    )
    optional_positional_or_keyword = parser.add_argument_group(
        f"{func_name}: POSITIONAL_OR_KEYWORD"
    )
    optional_var_positional = parser.add_argument_group(f"{func_name}: VAR_POSITIONAL")
    optional_keyword_only = parser.add_argument_group(f"{func_name}: KEYWORD_ONLY")
    optional_var_keyword = parser.add_argument_group(f"{func_name}: VAR_KEYWORD")
    filter_attr = ["self", "cls", "mcs"]

    for orig_arg_name in arg_dict:
        if orig_arg_name not in filter_attr:
            arg_default_val = func_param.default(orig_arg_name)
            arg_val = arg_dict[orig_arg_name]
            arg_annotation = annotations[orig_arg_name]
            arg_annotation_name = arg_annotation.__name__
            arg_name = orig_arg_name.replace("_", "-")
            arg_cli_validator = CLIValidator(debug=True, logger=False)
            arg_cli_validator.annotation = arg_annotation
            if arg_default_val is func_param.empty and not any([arg_val]):
                # these are required arguments whoes default values are not present
                # it may or may not have annotations
                # refer: https://stackoverflow.com/a/59286623
                # why --arg_name is required or not.
                if arg_annotation is _empty:
                    required_positional_only.add_argument(
                        arg_name,
                        help=f"{arg_name} is a required parameter",
                    )
                else:
                    required_positional_only.add_argument(
                        arg_name,
                        help=f"{arg_name} is a required {arg_annotation_name}  parameter",
                        type=arg_cli_validator,
                    )
            else:
                # these are optional arguments whoes default value is present:
                # it can be None, () or any val, it too may or may not have
                # annotations. if pos_arg, var_arg = ([], [('args', ())]),
                # func.args is present it indicates that the pos_arg is empty
                # and only variable argument present
                if any(pos_arg) and any(orig_arg_name == ar[0] for ar in pos_arg):
                    # if pos_arg is present then the default value is present for sure
                    if arg_annotation is _empty:
                        optional_positional_or_keyword.add_argument(
                            f"--{arg_name}",
                            default=arg_val,
                            help=f"{arg_name} is an optional parameter, default {arg_val}",
                            required=False,
                            nargs="?",
                        )
                    else:
                        optional_positional_or_keyword.add_argument(
                            f"--{arg_name}",
                            default=arg_val,
                            type=arg_cli_validator,
                            help=f"{arg_name} is an optional {arg_annotation_name} parameter, default {arg_val}",
                            required=False,
                            nargs="?",
                        )
                if any(var_arg) and any(orig_arg_name == ar[0] for ar in var_arg):
                    # we dont add any default value here as it is an optional field but also
                    # we don't know what will be the future value so leave it without defaults.
                    # PLEASE dont add defaults here.
                    if arg_annotation is _empty:
                        optional_var_positional.add_argument(
                            f"--{arg_name}",
                            help=f"{arg_name} is an optional parameter",
                            required=False,
                            nargs="*",
                        )
                    else:
                        optional_var_positional.add_argument(
                            f"--{arg_name}",
                            type=arg_cli_validator,
                            help=f"{arg_name} is an optional {arg_annotation_name} parameter",
                            required=False,
                            nargs="*",
                        )

    for orig_kw_name in kwarg_dict:
        kw_annotation = annotations[orig_kw_name]
        kw_annotation_name = kw_annotation.__name__
        cli_kw_name = orig_kw_name.replace("_", "-")
        kw_cli_validator = CLIValidator(debug=True, logger=False)
        kw_cli_validator.annotation = kw_annotation

        if any(kw_only) and orig_kw_name in kw_only:
            if kw_annotation is _empty:
                optional_keyword_only.add_argument(
                    f"--{cli_kw_name}",
                    default=kwarg_dict[orig_kw_name],
                    help=f"{cli_kw_name} is an optional parameter, default {kwarg_dict[orig_kw_name]}",
                    required=False,
                )
            else:
                optional_keyword_only.add_argument(
                    f"--{cli_kw_name}",
                    default=kwarg_dict[cli_kw_name],
                    help=f"{cli_kw_name} is an optional {kw_annotation_name} parameter, default {kwarg_dict[orig_kw_name]}",
                    type=kw_cli_validator,
                    required=False,
                )
        elif any(var_kw) and orig_kw_name in var_kw:
            if kw_annotation is _empty:
                optional_var_keyword.add_argument(
                    f"--{cli_kw_name}",
                    help=f"{cli_kw_name} is an optional parameter",
                    required=False,
                )
            else:
                optional_var_keyword.add_argument(
                    f"--{cli_kw_name}",
                    help=f"{cli_kw_name} is an optional {kw_annotation_name} parameter",
                    type=kw_cli_validator,
                    required=False,
                )
    if function.__class__.__name__ == "type" and add_subparsers:
        subparsers = None
        for attr in function.__dict__:
            func_attr = getattr(function, attr)
            if callable(func_attr) and not attr.startswith("_"):
                if subparsers is None:
                    subparsers = parser.add_subparsers(
                        title="Sub Commands",
                        description="valid subcommands",
                        help=f" additional {func_name} sub-commands",
                    )
                attr_parser = subparsers.add_parser(attr, help=func_attr.__doc__)
                _, _ = _func_to_argparse_and_param(func_attr, attr_parser)
    return parser, func_param


if __name__ == "__main__":
    import sys

    from demosite.server import run

    vali = CLIValidator(debug=True, logger=False, name="vali")
    vtype = t.Union[bool, Path, list[bool]]
    vali.annotation = vtype
    val = vali.custom_type(["1", ["we"]], type_=vtype)
    print(val)
    # print(isinstance(val, vali))
    # cli(run, *sys.argv[1:])
