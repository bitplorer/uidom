# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import os
from collections.abc import Iterable
from typing import List, Union

__all__ = ["make_paths", "MakePath"]


def path_exists(path):
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    path_exist = os.path.exists(path)
    return path_exist


class SubdirOrFile(object):
    def __init__(self, sub_directory_or_file: Union[str, List[str]] = None):
        self._sub_dir_or_file = (
            (
                map(lambda x: os.path.abspath(x), sub_directory_or_file)
                if isinstance(sub_directory_or_file, Iterable)
                else [os.path.abspath(sub_directory_or_file)]
            )
            if sub_directory_or_file is not None
            else [sub_directory_or_file]
        )

        self._iter_sub_dir_or_file = None

    def sub_dir_or_file(self):
        return self._sub_dir_or_file

    def __iter__(self):
        for sub_dir_or_file in self.sub_dir_or_file():
            yield sub_dir_or_file

    def __next__(self):
        if self._iter_sub_dir_or_file is None:
            self._iter_sub_dir_or_file = iter(self)
        return next(self._iter_sub_dir_or_file)

    def _get_path(self, sub_directory_or_file=None, directory=None):
        sub_directory_or_file = (
            sub_directory_or_file
            if isinstance(sub_directory_or_file, Iterable)
            else [sub_directory_or_file]
            if sub_directory_or_file is not None
            else iter(self)
        )

        if directory is None:
            paths = sub_directory_or_file
        else:
            paths = list()
            for sub_dir in sub_directory_or_file:
                if sub_dir:
                    if isinstance(directory, Iterable):
                        for direct in directory:
                            paths.extend(os.path.join(direct, sub_dir))
                    else:
                        paths = os.path.join(directory, sub_dir)
        return paths

    @staticmethod
    def existing(paths):
        if any(paths):
            for p in paths:
                if path_exists(p):
                    yield p
        else:
            yield paths


class MakePath(SubdirOrFile):
    def __init__(self, sub_directory_or_file, directory=None, create_file=False):
        super(MakePath, self).__init__(sub_directory_or_file=sub_directory_or_file)
        self._directory = directory
        self._create_file = create_file

        self._all_paths = self._get_path(sub_directory_or_file, self._directory)
        self._paths_that_exits = set(self.existing(self._all_paths))
        self._paths_to_create = set(self._all_paths).difference(self._paths_that_exits)
        self._paths_created = set()

    def paths_exists(self, path_name=None):
        if path_name:
            return path_name in self._paths_that_exits
        return self._paths_that_exits

    def paths_to_create(self):
        return self._paths_to_create

    def paths_created(self):
        return self._paths_created

    def make_path(self):
        paths_created = list()

        for path in self._paths_to_create:
            if "." not in os.path.basename(path):
                if not path_exists(path):
                    if path == "__main__":
                        continue
                    os.makedirs(path)
                    paths_created.append(path)
            elif self._create_file:
                path_dir = os.path.dirname(path)
                if not path_exists(path_dir):
                    os.makedirs(path_dir)
                    paths_created.append(path_dir)

                with open(path, mode="a"):
                    paths_created.append(path)

        for path in paths_created:
            self._paths_to_create.remove(path)
            self._paths_created.add(path)
            if path not in self._paths_that_exits:
                self._paths_that_exits.add(path)

    def __str__(self):
        return "<MakePath({files})>".format(files=self._all_paths)


def make_paths(dirs_list):
    paths = MakePath(dirs_list)
    paths.make_path()
    return paths.paths_created()
