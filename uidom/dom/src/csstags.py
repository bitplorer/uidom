# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.src.main import extension

__all__ = [
    "CSSClass",
    "CSSId",
    "CSS",
    "CSSProperty"
]


class CSS(extension.StyleTags):
    pass


class CSSClass(extension.StyleTags):
    is_class = True
    is_inline = True


class CSSId(extension.StyleTags):
    is_id = True
    is_inline = True


class CSSProperty(extension.StyleTags):

    def __set_name__(self, owner, name):
        self._id = f"{owner.__name__}.{name}".replace(".", "-").replace("_", "-")
        self._class = name.replace("_", "-")
        self._apply = f"{owner.__name__}::part({name})".replace("_", "-")

        class Class(CSSClass):
            tagname = self._class

        class Id(CSSId):
            tagname = self._id.lower()

        class CSS(extension.StyleTags):
            tagname = name.replace("_", "-")

        class Apply(extension.StyleTags):
            tagname = self._apply.lower()
            is_apply = True
            left_delimiter = "{@"

        self.css_class = Class
        self.css_id = Id
        self.css = CSS
        self.css_apply = Apply


if __name__ == '__main__':
    # from myst_parser import parse_html

    class Order(object):
        product_name = CSSProperty()
        product_category = CSSProperty()
        product_id = CSSProperty()


    order = Order()
    products = order.product_name.css_id(background_color='red', width="12%")
    category = order.product_category.css_class(color="#23cfff")
    csss = order.product_id.css_apply(apply="bg-rose-500")
    id = order.product_id.css_id()


    # ast = parse_html.tokenize_html(html(style(products, category)).render())
    # print(list(ast.walk()))

    class product(CSSClass):
        pass


    cs = products
    # cs.attributes.update(padding="10px")
    cs["boxsize"] = "border-box"
    cs["background-color"] = "red"
    print(cs)
    print(category)
    print(csss.render(pretty=False))
