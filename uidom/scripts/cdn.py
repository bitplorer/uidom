from __future__ import annotations

import asyncio
import hashlib
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

import httpx
from httpx._exceptions import InvalidURL

__all__ = ["CDNToStatic"]


class CDNToStatic:
    def __init__(
        self,
        static_dir: Path,
        static_url: Path,
        base_url: str,
        default_ext: str = ".js",
    ):
        self.static_dir: Path = static_dir
        self.static_url: Path = static_url
        self.base_url: str = base_url
        self.default_ext: str = default_ext
        self.url_maps: defaultdict = defaultdict(list)

    def _valid_path_to_url(self, path):
        # checks if path contains the base_url, if not then create a valid url from
        # this path else just return it
        if self.base_url not in path:
            if path and not path.startswith(("/", "@")):
                raise InvalidURL(
                    "For absolute URLs, path must begin with either '/' or '@'"
                )
            return f"{self.base_url}{path}"
        return path

    def _file_name_from_path(self, path):
        path_hash_hex_str = str(hashlib.sha256(path.encode()).hexdigest())
        _file_ = Path(path)
        _file_name = (
            # here we are hashing path because the many versions of path can have same file stem
            # like for path = "@1.8.6/dist/htmx.min.js" stem is "htmx.min.js". This can be same
            # across many versions so include the hash of the path to be sure about the version
            # that exists.
            # using .name to get file name with extension
            "".join([path_hash_hex_str, self.default_ext])
            if not _file_.suffix
            else "".join([_file_.stem, path_hash_hex_str, _file_.suffix])
        )
        return _file_name

    async def _get_path(self, path):
        if path not in self.url_maps:
            url = self.url_maps[path] = self._valid_path_to_url(path)
        else:
            url = self.url_maps[path]

        _file_name = self._file_name_from_path(path)

        download_file = Path(self.static_dir) / _file_name
        api_url_path = f"{self.static_url}/{_file_name}"

        if download_file.exists():
            return api_url_path

        try:
            response = await self._get(url)

            if response.status_code != 200:
                raise ValueError(
                    f"Failed to download from URL: {url} to {download_file}, response status: {response.status_code}"
                )
            if not download_file.parent.exists():
                download_file.parent.mkdir()

            with download_file.open(mode="wb") as f:
                f.write(response.content)

        except httpx.RequestError:
            raise ValueError(f"Failed to connect to CDN")

        return api_url_path

    @lru_cache
    def __getitem__(self, path):
        return asyncio.run(self._getpath(path))

    def __truediv__(self, path):
        if self.base_url not in path:
            if path and path.startswith("/"):
                raise InvalidURL(
                    f"While using absolute paths with {self.__div__}, {path} must not begin with '/'"
                )

        path_from_div = "".join(["/", path])
        new_base_url = self._valid_path_to_url(path_from_div)

        # we check if the "new_base_url" is "path" itself and if not it means that "path" provided
        # here is just an absolute path so we can create a new folder in static dir
        new_static_dir = (
            self.static_dir if new_base_url == path_from_div else self.static_dir / path
        )

        # now we are going to update the static_url too if new_static_dir is not same as old static_dir
        # as it means new folder is going to be created in
        new_static_url = (
            self.static_url
            if new_static_dir == self.static_dir
            else self.static_url / path
        )

        return CDNToStatic(
            static_dir=new_static_dir,
            static_url=new_static_url,
            base_url=new_base_url,
            default_ext=self.default_ext,
        )

    def __div__(self, path):
        return self.__truediv__(path)

    async def _get(self, url):
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            return await client.get(url)

    async def main(*args):
        return await asyncio.gather(*args)

    def __call__(self, *paths):
        return asyncio.run(self.main(*map(lambda path: self._get_path(path), paths)))
