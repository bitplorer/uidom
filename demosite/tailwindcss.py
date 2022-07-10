# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from uidom import TailwindCommand

from demosite.dom import document

if __name__ == '__main__':
    if document.webassets:
        tailwind = TailwindCommand(
            file_path=__file__,
            webassets=document.webassets,
            input_file="tailwind.css",
            output_file="styles.css"
        )
        tailwind.start()
    