# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import sys
import typing as T
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pformat

from uidom.dom.htmldocument import HtmlDocument
from uidom.dom.src import ext
from uidom.settings.paths import make_paths
from uidom.utils.logger import uidom_logger

__all__ = [
    "Document",
    "WebAssets",
    "Dir",
    "DirConfig",
    "TemplateDir",
    "StaticDir",
    "UploadDir",
    "DatabaseDir",
    "CacheDir",
]


@dataclass
class Document(object):
    head: T.Optional[T.Union[ext.Tags, list[ext.Tags]]] = None
    body: T.Optional[T.Union[ext.Tags, list[ext.Tags]]] = None
    ensure_csrf_token: bool = field(default=False)
    webassets: T.Optional["WebAssets"] = None

    def __call__(self, *args, head=None, body=None, **kwargs) -> HtmlDocument:
        html_doc = HtmlDocument
        html_doc.ensure_csrf_token = self.ensure_csrf_token
        return html_doc(
            *args,
            head=head,
            body=body,
            common_head=self.head,
            common_body=self.body,
            **kwargs,
        )


class DirType(object):
    def __iter__(self):
        for item in self.__dict__:
            if "DIR" in item:
                yield self.__dict__[item]

    def __next__(self):
        return next(self)

    def dict(self):
        return {item: self.__dict__[item] for item in self.__dict__ if "DIR" in item}

    def __str__(self):
        return str(list(self))


@dataclass
class DirConfig(DirType):
    base_dir: T.Union[str, Path]
    sub_dir: T.Union[str, Path] = ""

    def __post_init__(self):
        # if not all([self.BASE_DIR, self.SUB_DIR]):
        #     raise ValueError(f"BASE_DIR, BASE_PATH values required")
        if isinstance(self.base_dir, str):
            if os.path.isfile(self.base_dir):
                # like when __file__ is passed in the BASE_DIR param
                self.base_dir = Path(self.base_dir).parent.resolve()
            else:
                self.base_dir = Path(self.base_dir).resolve()

        subdir: T.Union[str, Path] = (
            self.sub_dir
            if not os.path.isfile(self.sub_dir)
            else os.path.dirname(self.sub_dir)
        )

        base_dir: T.Union[str, Path] = self.base_dir

        if subdir:
            if isinstance(self.base_dir, str):
                if self.base_dir != "__main__":
                    if not os.path.isfile(self.base_dir):
                        if os.path.isdir(self.base_dir):
                            base_dir = os.path.join(self.base_dir, subdir)
                        else:
                            base_dir = os.path.join(
                                self.base_dir.replace(".", os.path.sep), subdir
                            )
                    else:
                        base_dir = os.path.join(os.path.dirname(self.base_dir), subdir)
                else:
                    folder = sys.modules["__main__"].__file__ or ""
                    base_dir = (
                        Path(folder).parent / subdir
                        if folder
                        else Path(folder) / subdir
                    )
            else:
                base_dir = self.base_dir / subdir

        self.BASE_DIR = Path(
            base_dir if any([base_dir]) else os.path.abspath(f".{os.path.sep}")
        )


class Dir(DirType):
    def __init__(self, dir_config: DirConfig):
        ...


class DatabaseDir(Dir):
    DATABASE_PATH = "database"
    SQL_PATH = "sql"
    NOSQL_PATH = "no_sql"

    def __init__(self, dir_config: DirConfig):
        self.DATABASE_DIR = dir_config.BASE_DIR / self.DATABASE_PATH
        self.SQL_DIR = self.DATABASE_DIR / self.SQL_PATH
        self.NOSQL_DIR = self.DATABASE_DIR / self.NOSQL_PATH

        self.dir: Path = self.DATABASE_DIR
        self.sql: Path = self.SQL_DIR
        self.nosql: Path = self.NOSQL_DIR


class StaticDir(Dir):
    STATIC_PATH = "static"
    MEDIA_PATH = "media"
    FILE_PATH = "file"
    CSS_PATH = "css"
    JS_PATH = "js"
    FONT_PATH = "font"
    IMAGE_PATH = "image"
    AUDIO_PATH = "audio"
    VIDEO_PATH = "video"

    def __init__(self, dir_config: DirConfig):
        self.STATIC_DIR = dir_config.BASE_DIR / self.STATIC_PATH

        self.MEDIA_DIR = self.STATIC_DIR / self.MEDIA_PATH
        self.FILE_DIR = self.STATIC_DIR / self.FILE_PATH

        self.IMAGE_DIR = self.MEDIA_DIR / self.IMAGE_PATH
        self.AUDIO_DIR = self.MEDIA_DIR / self.AUDIO_PATH
        self.VIDEO_DIR = self.MEDIA_DIR / self.VIDEO_PATH

        self.CSS_DIR = self.FILE_DIR / self.CSS_PATH
        self.JS_DIR = self.FILE_DIR / self.JS_PATH
        self.FONT_DIR = self.FILE_DIR / self.FONT_PATH

        self.dir: Path = self.STATIC_DIR
        self.media: Path = self.MEDIA_DIR
        self.file: Path = self.FILE_DIR

        self.image: Path = self.IMAGE_DIR
        self.audio: Path = self.AUDIO_DIR
        self.video: Path = self.VIDEO_DIR
        self.css: Path = self.CSS_DIR
        self.js: Path = self.JS_DIR
        self.font: Path = self.FONT_DIR


class UploadDir(Dir):
    UPLOAD_PATH = "upload"
    MEDIA_PATH = "media"
    FILE_PATH = "file"
    IMAGE_PATH = "image"
    AUDIO_PATH = "audio"
    VIDEO_PATH = "video"

    def __init__(self, dir_config: DirConfig):
        self.UPLOAD_DIR = dir_config.BASE_DIR / self.UPLOAD_PATH

        self.MEDIA_DIR = self.UPLOAD_DIR / self.MEDIA_PATH
        self.FILE_DIR = self.UPLOAD_DIR / self.FILE_PATH

        self.IMAGE_DIR = self.MEDIA_DIR / self.IMAGE_PATH
        self.AUDIO_DIR = self.MEDIA_DIR / self.AUDIO_PATH
        self.VIDEO_DIR = self.MEDIA_DIR / self.VIDEO_PATH

        self.dir: Path = self.UPLOAD_DIR
        self.media: Path = self.MEDIA_DIR
        self.file: Path = self.FILE_DIR

        self.image: Path = self.IMAGE_DIR
        self.audio: Path = self.AUDIO_DIR
        self.video: Path = self.VIDEO_DIR


class TemplateDir(Dir):
    TEMPLATE_PATH = "templates"

    def __init__(self, dir_config: DirConfig):
        self.TEMPLATE_DIR = dir_config.BASE_DIR / self.TEMPLATE_PATH
        self.dir: Path = self.TEMPLATE_DIR


class CacheDir(Dir):
    CACHE_PATH = "cache"

    def __init__(self, dir_config: DirConfig):
        self.CACHE_DIR = dir_config.BASE_DIR / self.CACHE_PATH
        self.dir = self.CACHE_DIR


class WebAssets(DirConfig):
    template: TemplateDir
    upload: UploadDir
    static: StaticDir
    database: DatabaseDir
    cache: CacheDir

    def __init__(
        self,
        base_dir: T.Union[str, Path],
        sub_dir: T.Optional[T.Union[str, Path]] = None,
        template_dir: T.Type[TemplateDir] = TemplateDir,
        upload_dir: T.Type[UploadDir] = UploadDir,
        static_dir: T.Type[StaticDir] = StaticDir,
        database_dir: T.Type[DatabaseDir] = DatabaseDir,
        cache_dir: T.Type[CacheDir] = CacheDir,
        *dir_types: T.Type[Dir],
        dry_run=True,
    ):
        super().__init__(base_dir=base_dir, sub_dir=sub_dir or "")
        # basic settings
        self.dir = self.BASE_DIR

        self.dir_logger = uidom_logger

        # directories
        self.template: TemplateDir = template_dir(dir_config=self)
        self.upload: UploadDir = upload_dir(dir_config=self)
        self.static: StaticDir = static_dir(dir_config=self)
        self.database: DatabaseDir = database_dir(dir_config=self)
        self.cache: CacheDir = cache_dir(dir_config=self)
        directories = [
            *self,
            *self.template,
            *self.upload,
            *self.static,
            *self.database,
            *self.cache,
        ]
        for dir_type in dir_types:
            directories.extend(*dir_type(self))
        if dry_run:
            self.dir_logger.info(f"(DIR):{self.dir.parent}")
            self.dir_logger.info("== Following directories would be created ==")
            for dir_name in directories:
                self.dir_logger.info(pformat(dir_name))
        else:
            self.make_dirs(directories)

    def make_dirs(self, directories):
        dirs_created: list[T.Union[str, Path]] = make_paths(directories)

        if dirs_created:
            self.dir_logger.info(f"(DIR):{self.dir.parent}")
            for file in sorted(dirs_created):
                if file:
                    self.dir_logger.info(pformat(Path(file)))

    def __dir__(self) -> T.Iterable[str]:
        return sorted(
            iter(self.__dict__),
            key=lambda k: (~k.startswith("__"), k[0].lower(), k[0]),
        )
