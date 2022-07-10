# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import platform
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Union

import valio
from uidom.settings import WebAssets

__all__ = [
    "Command",
    "TailwindCommand"
]

def is_windows():
    if platform.system() == 'Windows':
        return True
    if platform.system().startswith('MINGW64_NT-'):
        return True
    return False


IS_WINDOWS = is_windows()

@dataclass
class Command(object):
    # command = valito.StringField(logger=False, debug=True)

    def run_command(self, *cmd, **kw) -> tuple[int, list[str]]:
        # self.command.logger.info(f'# {" ".join(cmd)}')

        if kw.get('shell'):
            while isinstance(cmd, list) or isinstance(cmd, tuple):
                cmd = cmd[0]
            # self.command.logger.debug(f'shell: {cmd}')
        with subprocess.Popen(cmd,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              **kw) as p:
            if not p.stdout:
                raise Exception("fail to popen")
            while p.poll() is None:
                lines = []
                for line_bytes in iter(p.stdout.readline, b''):
                    line_bytes = line_bytes.rstrip()
                    try:
                        line = line_bytes.decode(encoding)
                    except (Exception,):
                        encoding = 'utf-8'
                        line = line_bytes.decode(encoding)
                    # self.command.logger.debug(line.rstrip())
                    lines.append(line)
                returncode = p.wait()
        if returncode != 0:
            raise subprocess.CalledProcessError(returncode, cmd)
        return p.returncode, lines


GROUPS = Union[str, list[str], None]


class GroupValidator(valio.Validator):
    annotation = GROUPS


class GroupField(valio.Field):
    validator = GroupValidator


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
    input_file: Union[str, Path]
    output_file: Union[str, Path]
    minify: bool = False

    def __post_init__(self):
        self.root_dir = self.webassets.directory.ROOT_DIR
        self.project_dir = Path(self.file_path).parent
        self.input_file = self.root_dir / self.input_file
        self.output_file = self.webassets.static.css / self.output_file
        sys.exit(self.init_tailwind_project())

    def init_tailwind_project(self):
        if self.is_tailwindcss_available():
            tailwind_config_js = (self.root_dir / 'tailwind.config.js')
            if not tailwind_config_js.exists():
                print("initialising Tailwindcss Config")
                self.init_tailwind_config(init_dir=self.root_dir)
                if tailwind_config_js.exists():
                    with tailwind_config_js.open("w", encoding="utf-8") as tw:
                        tw.write(f'''
    module.exports = {{
        mode: "jit",
        content: {{
            files:[
            "../../{self.project_dir.relative_to(self.root_dir.parent.parent)}/*.{{html,py}}",
            "../../{self.project_dir.relative_to(self.root_dir.parent.parent)}/**/*.{{html,py}}",
            "../../{self.project_dir.relative_to(self.root_dir.parent.parent)}/**/**/*.{{html,py}}",
            ]
          }},
        plugins: [
            require('@tailwindcss/aspect-ratio'),
            require('@tailwindcss/forms'),
            require('@tailwindcss/line-clamp'),
            require('@tailwindcss/typography'),
            require('tailwindcss/colors'),
        ],
        theme: {{
            extend: {{}}
        }}
        
        }}''')
            if not self.input_file.exists() and tailwind_config_js.exists():
                with self.input_file.open("w", encoding="utf-8") as f:
                    f.write('''@tailwind base;\n@tailwind components;\n@tailwind utilities;''')

    def run_command(self, *cmd, **kw) -> tuple[int, list[str]]:
        # self.command.logger.info(f'# {" ".join(cmd)}')

        if kw.get('shell'):
            while isinstance(cmd, list) or isinstance(cmd, tuple):
                cmd = cmd[0]
            # self.command.logger.debug(f'shell: {cmd}')
        with subprocess.Popen(cmd,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              **kw) as p:
            if not p.stdout:
                raise Exception("fail to popen")
            while p.poll() is None:
                lines = []
                for line_bytes in iter(p.stdout.readline, b''):
                    line_bytes = line_bytes.rstrip()
                    try:
                        line = line_bytes.decode(encoding)
                    except (Exception,):
                        encoding = 'utf-8'
                        line = line_bytes.decode(encoding)
                    # self.command.logger.debug(line.rstrip())
                    lines.append(line)
                returncode = p.wait()
        if returncode != 0:
            raise subprocess.CalledProcessError(returncode, cmd)
        return p.returncode, lines

    def is_tailwindcss_available(self):
        output = subprocess.run([self.tailwindcss], cwd=self.root_dir.as_posix().encode() if not IS_WINDOWS else str(self.root_dir).encode())
        print("tailwindcss command :> ", output)
        return output

    def init_tailwind_config(self, init_dir: Path):
        print("trying to init tailwindcss config")
        output = subprocess.run([self.tailwindcss, "init"], cwd=init_dir.as_posix().encode() if not IS_WINDOWS else str(self.root_dir).encode())
        print("intialisation > ", bool(output))

    def start(self):
        print("cwd", self.root_dir)
        print("input_file > ", self.input_file)
        print("output_file > ", self.output_file)
        try:
            output = subprocess.run([
                self.tailwindcss,
                '-i', self.input_file.relative_to(self.root_dir),
                "-o", self.output_file.relative_to(self.root_dir),
                f"--{(self.minify and 'minify') or 'watch'}",
                ],
                cwd=self.root_dir
            )
            return output
        except (Exception,) as e:
            print(e)

#
# if __name__ == "__main__":
#     print(Group(["asdf", "kubctrl"]).exists())
