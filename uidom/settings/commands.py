# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import asyncio
import logging
import platform
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union

import valio

from uidom.settings import WebAssets

__all__ = ["Command", "TailwindCommand"]


logger = logging.getLogger(__name__)


def is_windows():
    if platform.system() == "Windows":
        return True
    if platform.system().startswith("MINGW64_NT-"):
        return True
    return False


IS_WINDOWS = is_windows()


@dataclass
class Command(object):
    # command = valito.StringField(logger=False, debug=True)

    def run_command(self, *cmd, **kw) -> tuple[int, list[str]]:
        # self.command.logger.info(f'# {" ".join(cmd)}')

        if kw.get("shell"):
            while isinstance(cmd, list) or isinstance(cmd, tuple):
                cmd = cmd[0]
            # self.command.logger.debug(f'shell: {cmd}')
        with subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kw
        ) as p:
            if not p.stdout:
                raise Exception("fail to popen")
            while p.poll() is None:
                lines = []
                for line_bytes in iter(p.stdout.readline, b""):
                    line_bytes = line_bytes.rstrip()
                    try:
                        line = line_bytes.decode(kw.get("encoding"))
                    except (Exception,):
                        encoding = "utf-8"
                        line = line_bytes.decode(encoding)
                    # self.command.logger.debug(line.rstrip())
                    lines.append(line)
                returncode = p.wait()
        if returncode != 0:
            raise subprocess.CalledProcessError(returncode, cmd)
        return p.returncode, lines


# GROUPS = Union[str, list[str], None]


# class GroupValidator(valio.Validator):
#     annotation = GROUPS


# class GroupField(valio.Field):
#     validator = GroupValidator


# @dataclass
# class Group(Command):
#     groups = GroupField(logger=False, debug=True)
#
#     @groups.add_post_validator
#     def groups_as_list(self, group):
#         if isinstance(group, str):
#             return (group,)
#         return group
#
#     def exists(self) -> dict:
#         groups = dict()
#         for grp in self.group:
#             self.groups.logger.info(grp)
#             try:
#                 result = self.run_command('getent', 'group', grp)
#                 groups[grp] = result[1]
#                 self.groups.logger.info(result)
#             except (Exception,) as e:
#                 self.groups.logger.error(e)
#                 groups[grp] = False
#         return groups
#
#     def add(self, name):
#         ...
#
#     def remove(self, name):
#         ...
#
#     group: GROUPS = groups.validator


class TailwindValidator(valio.Validator):
    annotation = Union[str, list[str], None]


@dataclass
class TailwindCommand(Command):
    tailwindcss = TailwindValidator(debug=True, logger=False, default="tailwindcss")
    file_path: Union[str, Path]
    webassets: WebAssets
    input_css: Optional[Union[str, Path]] = field(default="tailwind.css")
    output_css: Optional[Union[str, Path]] = field(default="styles.css")
    minify: bool = False

    def __post_init__(self):
        self.output_css = Path(self.output_css)
        self._root_dir = self.webassets.dir
        self._project_dir = Path(self.file_path).parent
        self._input_file: Path = self._root_dir / self.input_css
        self._output_file: Path = self.webassets.static.css / self.output_css

        # this sections of the code is for
        try:
            all_output_files = sorted(
                Path(self.webassets.static.css).glob(f"*{self._output_file.suffix}"),
                reverse=True,
            )
            old_output_file = all_output_files[0]
            if len(all_output_files) > 1:
                [file.unlink(missing_ok=True) for file in all_output_files[1:]]
        except IndexError as e:
            old_output_file = None

        if old_output_file:
            self._output_file = self.webassets.static.css / old_output_file
            self._output_file = self._output_file.replace(
                self._output_file.with_name(
                    f"{self.output_css.stem}_{time.strftime('%d_%b_%Y_%H_%M_%S')}{self._output_file.suffix}"
                )
            )
            self.output_css = self._output_file.name

        self.init_tailwind_project()

    def init_tailwind_project(self):
        if self.is_tailwindcss_available():
            tailwind_config_js = self._root_dir / "tailwind.config.js"
            if not tailwind_config_js.exists():
                logger.info("initialising Tailwindcss Config")
                self.init_tailwind_config(init_dir=self._root_dir)
                if tailwind_config_js.exists():
                    with tailwind_config_js.open("w", encoding="utf-8") as tw:
                        tw.write(
                            f"""module.exports = {{
    mode: "jit",
    darkMode: "class",
    content: {{
        files:[
        "../../{self._project_dir.relative_to(self._root_dir.parent.parent)}/*.{{html,py}}",
        "../../{self._project_dir.relative_to(self._root_dir.parent.parent)}/**/*.{{html,py}}",
        "../../{self._project_dir.relative_to(self._root_dir.parent.parent)}/**/**/*.{{html,py}}",
        "../../{self._project_dir.relative_to(self._root_dir.parent.parent)}/**/**/**/*.{{html,py}}",
        ]
        }},
    plugins: [
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('tailwindcss/colors'),
    ],
    theme: {{
        extend: {{
            keyframes:{{
                ripple:{{
                    '0%': {{opacity:1, scale:0}},
                    '100':{{opacity:0, scale:1.5}}
                }}
            }},
            animation:{{
                ripple: 'ripple 0.5s linear infinite'
            }}
        }}
    }}
    
    }}"""
                        )
            if not self._input_file.exists() and tailwind_config_js.exists():
                with self._input_file.open("w", encoding="utf-8") as f:
                    f.write(
                        """@tailwind base;\n@tailwind components;\n@tailwind utilities;"""
                    )
            if not self._output_file.exists():
                self._output_file.touch()

    def is_tailwindcss_available(self):
        output = subprocess.run(
            ["which" if not IS_WINDOWS else "where", self.tailwindcss],
            cwd=self._root_dir.as_posix().encode()
            if not IS_WINDOWS
            else str(self._root_dir).encode(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        # logger.info("tailwindcss command :> ", output)
        return output

    def init_tailwind_config(self, init_dir: Path):
        logger.info("trying to init tailwindcss config")
        output = subprocess.run(
            [self.tailwindcss, "init"],
            cwd=init_dir.as_posix().encode()
            if not IS_WINDOWS
            else str(self._root_dir).encode(),
        )
        logger.info(f"intialisation: { bool(output)}")

    def run(self):
        logger.info(f"cwd: { self._root_dir}")
        logger.info(f"input_file: { self._input_file}")
        logger.info(f"output_file: { self._output_file}")
        try:
            output = subprocess.run(
                [
                    self.tailwindcss,
                    "-i",
                    self._input_file.relative_to(self._root_dir),
                    "-o",
                    self._output_file.relative_to(self._root_dir),
                    f"--{(self.minify and 'minify') or 'watch'}",
                ],
                cwd=self._root_dir,
            )
            return output
        except (Exception,) as e:
            logger.error(e)

    async def async_run(self):
        logger.info(f"cwd: { self._root_dir}")
        logger.info(f"input_file: { self._input_file}")
        logger.info(f"output_file: { self._output_file}")

        try:
            if not hasattr(self, "_tailwind_process"):
                tailwind_process = asyncio.create_subprocess_shell(
                    " ".join(
                        [
                            self.tailwindcss,
                            "-i",
                            str(self._input_file.relative_to(self._root_dir)),
                            "-o",
                            str(self._output_file.relative_to(self._root_dir)),
                            f"--{(self.minify and 'minify') or 'watch'}",
                        ]
                    ),
                    cwd=self._root_dir,
                    stdout=subprocess.PIPE,  # if you want the output in the terminal comment this line
                    stderr=subprocess.PIPE,
                )
                self._tailwind_process = tailwind_process
            process = await self._tailwind_process
            stdout, stderr = await process.communicate()
            logger.info(f"Output: { stdout}")
            logger.info(f"Error: { stderr}")
        except (Exception,) as e:
            logger.error(e)


#
# if __name__ == "__main__":
#     print(Group(["asdf", "kubctrl"]).exists())
