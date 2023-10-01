# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from fastapi.requests import Request

from .product import Product


def get(request: Request):
    return Product(request)
