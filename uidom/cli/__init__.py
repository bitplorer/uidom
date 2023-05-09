# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from .cli import uidom

# import sys
# from importlib import import_module, resources

# PLUGINS = dict()


# def register_plugin(func):
#     """Decorator to register plug-ins"""
#     name = func.__name__
#     PLUGINS[name] = func
#     return func


# def __getattr__(name):
#     """Return a named plugin"""
#     try:
#         return PLUGINS[name]
#     except KeyError:
#         _import_plugins()
#         if name in PLUGINS:
#             return PLUGINS[name]
#         else:
#             raise AttributeError(
#                 f"module {__name__!r} has no attribute {name!r}"
#             ) from None


# def __dir__():
#     """List available plug-ins"""
#     _import_plugins()
#     return list(PLUGINS.keys())


# def _import_plugins():
#     """Import all resources to register plug-ins"""
#     for name in resources.contents(__name__):
#         if name.endswith(".py"):
#             import_module(f"{__name__}.{name[:-3]}")
