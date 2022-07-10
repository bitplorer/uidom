# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import sys
import typing as T
from dataclasses import dataclass
from pathlib import Path

from uidom.dom.htmldocument import HtmlDocument
from uidom.dom.src import ext
from uidom.settings.paths import make_paths

__all__ = ["UiDOM", "WebAssets", "FileSettings"]


@dataclass
class UiDOM(object):
    head: T.Optional[T.Union[ext.Tags, list[ext.Tags]]] = None
    body: T.Optional[T.Union[ext.Tags, list[ext.Tags]]] = None
    ensure_csrf_token_in_meta: T.Union[bool, None] = False
    webassets: T.Optional["WebAssets"] = None

    def __call__(self, *args, head=None, body=None, **kwargs) -> HtmlDocument:
        html_doc = HtmlDocument
        if not self.ensure_csrf_token_in_meta:
            html_doc.ensure_csrf_token_in_meta = self.ensure_csrf_token_in_meta
        return html_doc(
            *args,
            head=head,
            body=body,
            common_head=self.head,
            common_body=self.body,
            **kwargs
        )


@dataclass
class FileSettings(object):
    BASE_DIR: T.Union[str, Path]
    SUB_DIR: T.Union[str, Path] = ""
    TEMPLATE_PATH = "template"
    CACHE_PATH = "cache"
    STATIC_PATH = "static"
    DATABASE_PATH = "database"
    UPLOAD_PATH = "upload"
    MEDIA_PATH = "media"
    FILE_PATH = "file"
    CSS_PATH = "css"
    JS_PATH = "js"
    FONT_PATH = "font"
    IMAGE_PATH = "image"
    AUDIO_PATH = "audio"
    VIDEO_PATH = "video"

    SQL_PATH = "sql"
    NOSQL_PATH = "no_sql"

    def __post_init__(self):
        # if not all([self.BASE_DIR, self.SUB_DIR]):
        #     raise ValueError(f"BASE_DIR, BASE_PATH values required")
        if isinstance(self.BASE_DIR, str):
            if os.path.isfile(self.BASE_DIR):
                self.BASE_DIR = Path(self.BASE_DIR).parent.resolve()
            else:
                self.BASE_DIR = Path(self.BASE_DIR).resolve()


class DirConfig(object):

    def __init__(self, file_settings: FileSettings):
        subdir = (
            file_settings.SUB_DIR
            if not os.path.isfile(file_settings.SUB_DIR)
            else os.path.dirname(file_settings.SUB_DIR)
        )

        root_dir = (
            os.path.join(file_settings.BASE_DIR, subdir)
            if os.path.isdir(file_settings.BASE_DIR)
            else os.path.join(file_settings.BASE_DIR.replace(".", os.path.sep), subdir)
            if not os.path.isfile(file_settings.BASE_DIR)
            else os.path.join(os.path.dirname(file_settings.BASE_DIR), subdir)
            if file_settings.BASE_DIR != "__main__"
            else os.path.join(os.path.dirname(sys.modules["__main__"].__file__), subdir)
        ) if isinstance(file_settings.BASE_DIR, str) \
            else os.path.join(file_settings.BASE_DIR, subdir) if any(subdir) else file_settings.BASE_DIR

        self.ROOT_DIR = Path(
            root_dir if any([root_dir]) else os.path.abspath(f".{os.path.sep}")
        )
        self.TEMPLATE_DIR = self.ROOT_DIR / file_settings.TEMPLATE_PATH
        self.CACHE_DIR = self.ROOT_DIR / file_settings.CACHE_PATH
        self.DATABASE_DIR = self.ROOT_DIR / file_settings.DATABASE_PATH
        self.STATIC_DIR = self.ROOT_DIR / file_settings.STATIC_PATH
        self.UPLOAD_DIR = self.ROOT_DIR / file_settings.UPLOAD_PATH

        self.STATIC_MEDIA_DIR = self.STATIC_DIR / file_settings.MEDIA_PATH
        self.STATIC_FILE_DIR = self.STATIC_DIR / file_settings.FILE_PATH

        self.STATIC_CSS_DIR = self.STATIC_FILE_DIR / file_settings.CSS_PATH
        self.STATIC_JS_DIR = self.STATIC_FILE_DIR / file_settings.JS_PATH
        self.STATIC_FONT_DIR = self.STATIC_FILE_DIR / file_settings.FONT_PATH

        self.STATIC_IMAGE_DIR = self.STATIC_MEDIA_DIR / file_settings.IMAGE_PATH
        self.STATIC_AUDIO_DIR = self.STATIC_MEDIA_DIR / file_settings.AUDIO_PATH
        self.STATIC_VIDEO_DIR = self.STATIC_MEDIA_DIR / file_settings.VIDEO_PATH

        self.UPLOAD_MEDIA_DIR = self.UPLOAD_DIR / file_settings.MEDIA_PATH
        self.UPLOAD_FILE_DIR = self.UPLOAD_DIR / file_settings.FILE_PATH
        self.UPLOAD_IMAGE_DIR = self.UPLOAD_MEDIA_DIR / file_settings.IMAGE_PATH
        self.UPLOAD_AUDIO_DIR = self.UPLOAD_MEDIA_DIR / file_settings.AUDIO_PATH
        self.UPLOAD_VIDEO_DIR = self.UPLOAD_MEDIA_DIR / file_settings.VIDEO_PATH

        self.SQL_DATABASE_DIR = self.DATABASE_DIR / file_settings.SQL_PATH
        self.NOSQL_DATABASE_DIR = self.DATABASE_DIR / file_settings.NOSQL_PATH

    def __iter__(self):
        for item in self.__dict__:
            if "ROOT" in item or "DIR" in item:
                yield self.__dict__[item]

    def __next__(self):
        return next(self)

    def dict(self):
        return {item: self.__dict__[item]
                for item in self.__dict__
                if "ROOT" or "DIR" in item}

    def __str__(self):
        return str(list(self))


class UrlConfig(object):
    def __init__(self, dir_config: DirConfig):
        self.ROOT_URL = dir_config.ROOT_DIR
        self.TEMPLATE_URL = Path(os.path.sep) / dir_config.TEMPLATE_DIR.relative_to(dir_config.ROOT_DIR)
        self.STATIC_URL = Path(os.path.sep) / dir_config.STATIC_DIR.relative_to(dir_config.ROOT_DIR)
        self.UPLOAD_URL = Path(os.path.sep) / dir_config.UPLOAD_DIR.relative_to(dir_config.ROOT_DIR)

        self.STATIC_MEDIA_URL = Path(os.path.sep) / dir_config.STATIC_MEDIA_DIR.relative_to(dir_config.STATIC_DIR)
        self.STATIC_FILE_URL = Path(os.path.sep) / dir_config.STATIC_FILE_DIR.relative_to(dir_config.STATIC_DIR)

        self.STATIC_CSS_URL = Path(os.path.sep) / dir_config.STATIC_CSS_DIR.relative_to(dir_config.STATIC_FILE_DIR)
        self.STATIC_JS_URL = Path(os.path.sep) / dir_config.STATIC_JS_DIR.relative_to(dir_config.STATIC_FILE_DIR)
        self.STATIC_FONT_URL = Path(os.path.sep) / dir_config.STATIC_FONT_DIR.relative_to(dir_config.STATIC_FILE_DIR)
        self.STATIC_IMAGE_URL = Path(os.path.sep) / dir_config.STATIC_IMAGE_DIR.relative_to(dir_config.STATIC_MEDIA_DIR)
        self.STATIC_AUDIO_URL = Path(os.path.sep) / dir_config.STATIC_AUDIO_DIR.relative_to(dir_config.STATIC_MEDIA_DIR)
        self.STATIC_VIDEO_URL = Path(os.path.sep) / dir_config.STATIC_VIDEO_DIR.relative_to(dir_config.STATIC_MEDIA_DIR)

        self.UPLOAD_MEDIA_URL = Path(os.path.sep) / dir_config.UPLOAD_MEDIA_DIR.relative_to(dir_config.UPLOAD_DIR)
        self.UPLOAD_IMAGE_URL = Path(os.path.sep) / dir_config.UPLOAD_IMAGE_DIR.relative_to(dir_config.UPLOAD_MEDIA_DIR)
        self.UPLOAD_AUDIO_URL = Path(os.path.sep) / dir_config.UPLOAD_AUDIO_DIR.relative_to(dir_config.UPLOAD_MEDIA_DIR)
        self.UPLOAD_VIDEO_URL = Path(os.path.sep) / dir_config.UPLOAD_VIDEO_DIR.relative_to(dir_config.UPLOAD_MEDIA_DIR)
        self.UPLOAD_FILE_URL = Path(os.path.sep) / dir_config.UPLOAD_FILE_DIR.relative_to(dir_config.UPLOAD_DIR)

        self.SQL_DATABASE_URL = Path(os.path.sep) / dir_config.SQL_DATABASE_DIR.relative_to(dir_config.ROOT_DIR)

    def __iter__(self):
        for item in self.__dict__:
            if "URL" in item:
                yield self.__dict__[item]

    def __next__(self):
        return next(self)

    def dict(self):
        return {item: self.__dict__[item]
                for item in self.__dict__
                if "URL" in item}

    def __str__(self):
        return str(list(self))


class DatabaseFile(object):

    def __init__(self, dir_config: DirConfig):
        self.sql: Path = dir_config.SQL_DATABASE_DIR
        self.nosql: Path = dir_config.NOSQL_DATABASE_DIR


class StaticFile(object):
    def __init__(self, dir_config: DirConfig):
        self.dir: Path = dir_config.STATIC_DIR
        self.images: Path = dir_config.STATIC_IMAGE_DIR
        self.audios: Path = dir_config.STATIC_AUDIO_DIR
        self.videos: Path = dir_config.STATIC_VIDEO_DIR
        self.files: Path = dir_config.STATIC_FILE_DIR
        self.css: Path = dir_config.STATIC_CSS_DIR
        self.js: Path = dir_config.STATIC_JS_DIR
        self.fonts: Path = dir_config.STATIC_FONT_DIR
        self.medias: Path = dir_config.STATIC_MEDIA_DIR


class UploadedFile(object):
    def __init__(self, dir_config: DirConfig):
        self.dir: Path = dir_config.UPLOAD_DIR
        self.images: Path = dir_config.UPLOAD_IMAGE_DIR
        self.audios: Path = dir_config.UPLOAD_AUDIO_DIR
        self.videos: Path = dir_config.UPLOAD_VIDEO_DIR
        self.files: Path = dir_config.UPLOAD_FILE_DIR
        self.medias: Path = dir_config.UPLOAD_MEDIA_DIR


class TemplateFile(object):
    def __init__(self, dir_config: DirConfig):
        self.dir: Path = dir_config.TEMPLATE_DIR


class WebAssets(object):
    files: FileSettings
    directory: DirConfig
    url: UrlConfig
    template: TemplateFile
    upload: UploadedFile
    static: StaticFile
    database: DatabaseFile

    def __init__(self, file_settings: FileSettings):

        # basic settings
        self.directory = DirConfig(file_settings=file_settings)
        self.url = UrlConfig(dir_config=self.directory)

        # files
        self.template = TemplateFile(dir_config=self.directory)
        self.upload = UploadedFile(dir_config=self.directory)
        self.static = StaticFile(dir_config=self.directory)
        self.database = DatabaseFile(dir_config=self.directory)
        files_created = make_paths(self.directory)
        if files_created:
            print("files created :: ")
            for file in files_created:
                print("\tfile: ", file)


if __name__ == '__main__':
    from pathlib import Path

    from uidom.dom import div, meta, title
    doc = UiDOM()
    print(doc("hahah"))
