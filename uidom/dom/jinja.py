# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.src import component

__all__ = [
    "JinjaComponent"
]


class JinjaComponent(component.Component):
    file_extension = ".html"

    def render(self, *args, **kwargs):
        pass

    def __block__(self, block_name, *args):
        return self.jinja_tags.Block(block_name, *args)

    def __if__(self, if_condition, *if_args):
        return self.jinja_tags.If(if_condition, *if_args)

    def __elif__(self, elif_condition, *elif_args):
        return self.jinja_tags.Elif(elif_condition, *elif_args)

    def __else__(self, *else_args):
        return self.jinja_tags.Else(*else_args)

    def __if_else__(self, if_condition, *else_args):
        return self.__if__(if_condition, self.__else__(*else_args))

    def __if_elif__(self, if_condition, elif_condition, *elif_args):
        self.__if__(if_condition, self.__elif__(elif_condition, *elif_args))

    def __load__(self, load, *args):
        return self.jinja_tags.Load(load, *args)

    def __include__(self, include, *args):
        return self.jinja_tags.Include(include, *args)

if __name__ == '__main__':
    from uidom.dom import Elif, Else, If, p

    print(If("test", p("testing", p('ok')), Elif("staging", p("staging")), Else(p("production"), p("a"))))
