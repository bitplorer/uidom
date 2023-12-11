# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


__all__ = ["HTMLRoute", "StreamingRoute", "DirectoryRouter"]


import importlib
import re
import sys
from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Type, Union

from fastapi import params, routing
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.types import IncEx
from fastapi.utils import generate_unique_id
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute
from starlette.types import ASGIApp, Lifespan

from uidom.response.starlette import (
    HTMLResponse,
    StreamingResponse,
    html_response,
    streaming_response,
)


class HTMLRoute(routing.APIRoute):
    def __init__(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        response_model: Optional[Type[Any]] = None,
        status_code: Optional[int] = None,
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        name: Optional[str] = None,
        methods: Optional[Union[Set[str], List[str]]] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[IncEx] = None,
        response_model_exclude: Optional[IncEx] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
        dependency_overrides_provider: Optional[Any] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
        generate_unique_id_function: Union[
            Callable[["routing.APIRoute"], str], DefaultPlaceholder
        ] = Default(generate_unique_id),
    ) -> None:
        super().__init__(
            path=path,
            endpoint=html_response(endpoint),
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            name=name,
            methods=methods,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            dependency_overrides_provider=dependency_overrides_provider,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )


class StreamingRoute(routing.APIRoute):
    def __init__(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        response_model: Optional[Type[Any]] = None,
        status_code: Optional[int] = None,
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        name: Optional[str] = None,
        methods: Optional[Union[Set[str], List[str]]] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[IncEx] = None,
        response_model_exclude: Optional[IncEx] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
        dependency_overrides_provider: Optional[Any] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
        generate_unique_id_function: Union[
            Callable[["routing.APIRoute"], str], DefaultPlaceholder
        ] = Default(generate_unique_id),
    ) -> None:
        super().__init__(
            path=path,
            endpoint=streaming_response(endpoint),
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            name=name,
            methods=methods,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            dependency_overrides_provider=dependency_overrides_provider,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )


class DirectoryRouter(routing.APIRouter):
    # picked from https://github.com/ebubekir/fastapi-directory-routing
    _METHODS = ["get", "post", "put", "patch", "delete", "options", "head"]

    """DirectoryRouter class inherit from fastapi.APIRouter.

    This class begins automatic route scanning upon initialization.

    Args:
        base_directory (str, optional): Defines the folder to be subjected to automatic route scanning.
        route_file_name (str, optional): Specifies the file name within the folder where route scanning will be conducted

    Examples:
        >>> from fastapi import FastAPI
        >>> from uidom.routing.fastapi import DirectoryRouter
        >>> app = FastAPI()
        >>> dir_router = DirectoryRouter()
        >>> app.include_router(prefix="/dir-routes", router=dir_router)

    Todo:
        * For each route configuration, the __config__ variable will be searched within the files.
        * Error and exception handling scenarios will be enhanced/developed.

    """

    def __init__(
        self,
        base_directory: str = "app",
        route_file_name: str = "route",
        *,
        prefix: str = "",
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        default_response_class: Type[Response] = Default(JSONResponse),
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        routes: Optional[List[routing.BaseRoute]] = None,
        redirect_slashes: bool = True,
        default: Optional[ASGIApp] = None,
        dependency_overrides_provider: Optional[Any] = None,
        route_class: Type[routing.APIRoute] = StreamingRoute,
        on_startup: Optional[Sequence[Callable[[], Any]]] = None,
        on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
        # the generic to Lifespan[AppType] is the type of the top level application
        # which the router cannot know statically, so we use typing.Any
        lifespan: Optional[Lifespan[Any]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
        generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
            generate_unique_id
        ),
    ):
        self._base_directory = base_directory
        self._route_file_name = route_file_name
        super().__init__(
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            default_response_class=default_response_class,
            responses=responses,
            callbacks=callbacks,
            routes=routes,
            redirect_slashes=redirect_slashes,
            default=default,
            dependency_overrides_provider=dependency_overrides_provider,
            route_class=route_class,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            generate_unique_id_function=generate_unique_id_function,
        )

        self.build_router()

    def build_router(self):
        current_module = sys.modules["__main__"]
        parent = Path(current_module.__file__).parent
        _package_name = parent.name
        files = (parent / self.base_directory).absolute().rglob("*.py")

        for file in files:
            # ===================================================== #
            #     path to file module: excluding package folder     #
            # ===================================================== #
            #           example: app/module/                        #
            relative_file_folder = Path(file.parent).relative_to(parent)

            # ===================================================== #
            #     path to file module: including package folder     #
            # ===================================================== #
            #           example: package/app/module/                #
            file_package_path = str(_package_name / relative_file_folder)

            relative_file_folder = str(relative_file_folder)

            # example: package/app/module/ -> package.app.module
            module = file_package_path.replace("/", ".") + "." + file.stem
            # Import route file
            route_file = importlib.import_module(module)

            # Find routes
            if file.stem == self.route_file_name:
                # first we will search the declared functions in __all__
                # if we don't find any we will proceed to scan CRUD methods
                # like in self._METHODS and add them to routes
                # for example:
                #
                # app/login/route.py
                #
                # def get():...
                #
                # def post():...
                #
                route_methods = getattr(
                    route_file,
                    "__all__",
                    [r for r in dir(route_file) if r.lower() in self._METHODS],
                )
            else:
                # if the file name is NOT "route.py" and we want to include method from that
                # file in router, we can scan __all__ variable in directory for pyobjects
                # that declare route methods, for example
                #
                # shoppers.py
                #
                #   __all__ = ["Shoppers"]
                #
                #   class Shoppers(Component):
                #       routes = ["get", "post", "cart", etc...]
                #
                #       def get(self, ...):...
                #
                route_methods = defaultdict(dict)

                for klass_name in getattr(
                    route_file,
                    "__all__",
                    [r for r in dir(route_file) if r.lower() in self._METHODS],
                ):
                    klass = getattr(route_file, klass_name)
                    if getattr(klass, "routes", []):
                        for mthd in getattr(klass, "routes"):
                            route_methods[klass_name.lower()][mthd] = getattr(
                                klass, mthd
                            )
                    else:
                        route_methods["_FILE_ROUTES"][klass_name] = klass

            if route_methods:
                # braces_or_brackets = self._find_braces_or_brackets(
                #     relative_path_to_file_module
                # )
                # TODO: make a {items}, tags parsed well in advance
                # tag_string = ""
                # for str_to_remove in braces_or_brackets:
                #     tag_string = relative_path_to_file_module.replace(
                #         "/" + str_to_remove, ""
                #     )

                # Making "base_directory" prefix as default
                if relative_file_folder == self.base_directory:
                    tags = ["default"]
                else:
                    tags = relative_file_folder.split("/")

                if relative_file_folder.startswith(self.base_directory):
                    # remove base_directory prefix from path as "base_directory"
                    # is default folder.
                    rel_path_without_base_directory_prefix = (
                        relative_file_folder.replace(self.base_directory, "")
                    )
                    prefix = (
                        rel_path_without_base_directory_prefix
                        if rel_path_without_base_directory_prefix
                        else ""
                    )
                else:
                    prefix = "/" + relative_file_folder

                if prefix:
                    # remove private folders starting with "_" i.e. underscore
                    # from prefix as we treat them as not included in api paths
                    prefix = "/" + "/".join(
                        filter(
                            lambda x: x if not x.startswith("_") else None,
                            prefix.split("/"),
                        )
                    )

                    prefix = prefix if prefix != "/" else ""
                    _router = routing.APIRouter(prefix=prefix, tags=tags)
                else:
                    _router = routing.APIRouter(tags=tags)
                #########################################################
                #   important to pass on route_class to sub routers as  #
                #   we have to use StreamingRoute for UiDOM components  #
                #########################################################
                _router.route_class = self.route_class

                if isinstance(route_methods, list):
                    # these are methods inside normal route.py files
                    for method in route_methods:
                        _method_attr = getattr(route_file, method)
                        name = f"{module}:{_method}"
                        _method_attr.__dict__["name"] = name
                        if method in self._METHODS:
                            _router.add_api_route(
                                "/",
                                _method_attr,
                                name=_method_attr.name,
                                methods=[method.lower()],
                                description=_method_attr.__doc__,
                            )
                        else:
                            _router.add_api_route(
                                f"/{method.lower()}",
                                _method_attr,
                                name=_method_attr.name,
                                methods=["get"],
                                description=_method_attr.__doc__,
                            )

                else:
                    # these are methods inside non route.py files
                    # with __all__ variable declared, important thing to
                    # note is that all methods inside class MUST BE
                    # classmethod or staticmethod
                    for klass_name in route_methods:
                        for _method in route_methods[klass_name]:
                            _method_attr = route_methods[klass_name][_method]
                            # here we set .name attribute to method because we want
                            # htmx to use the route via hx_get=url_for(klass.method.name)
                            name = f"{module}.{klass_name}:{_method}"
                            _method_attr.__dict__["name"] = name

                            if _method.lower() in self._METHODS:
                                # case for [get, post, patch, delete, etc] CRUD methods
                                _router.tags.extend([file.stem, klass_name])
                                if not file.stem.startswith("_"):
                                    _route_ = (
                                        f"/{file.stem}/{klass_name}"
                                        if not klass_name.startswith("_")
                                        else f"/{file.stem}"
                                    )
                                else:
                                    _route_ = (
                                        f"/{klass_name}"
                                        if not klass_name.startswith("_")
                                        else f"/"
                                    )
                                _router.add_api_route(
                                    _route_,
                                    _method_attr,
                                    name=_method_attr.name,
                                    methods=[_method.lower()],
                                    description=_method_attr.__doc__,
                                )
                            else:
                                # case for other methods that are named other than CRUD
                                # operations such as Counter.increment, they all will
                                # default to "get" method.
                                _router.tags.extend([file.stem, klass_name])
                                if not file.stem.startswith("_"):
                                    _route_ = (
                                        f"/{file.stem}/{klass_name}/{_method.lower()}"
                                        if not klass_name.startswith("_")
                                        else f"/{file.stem}/{_method.lower()}"
                                    )
                                else:
                                    _route_ = (
                                        f"/{klass_name}/{_method.lower()}"
                                        if not klass_name.startswith("_")
                                        else f"/{_method.lower()}"
                                    )
                                _router.add_api_route(
                                    _route_,
                                    _method_attr,
                                    name=_method_attr.name,
                                    methods=["get"],
                                    description=_method_attr.__doc__,
                                )

                self.include_router(_router)

    def _find_braces_or_brackets(self, string):
        # bing search query that generated the below pattern
        # create a regex in python to match string inside
        # {} and [] where strings can be of pattern
        # "/hello/{world}/one/{plus}" or "/hello/[world]/[two]" etc

        pattern = re.compile(r"\{[^}]*\}|\[[^\]]*\]")
        return re.findall(pattern=pattern, string=string)

    @property
    def base_directory(self):
        return self._base_directory

    @base_directory.setter
    def base_directory(self, value):
        self._base_directory = value

    @property
    def route_file_name(self):
        return self._route_file_name
