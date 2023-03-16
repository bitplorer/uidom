# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from demosite import settings
from uidom import TailwindCommand

if __name__ == '__main__':
    if settings.DEBUG:
        tailwind = TailwindCommand(
                file_path=__file__,
                webassets=settings.webassets,
                input_file="tailwind.css",
                output_file="styles.css"
            )
        tailwind.start()
    