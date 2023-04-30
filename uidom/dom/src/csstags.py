# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.src.main import extension

__all__ = ["CSSClass", "CSSId", "CSS", "CSSProperty"]


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
        self.is_inline = getattr(owner, "is_inline", False)
        self._id = f"{owner.__name__}.{name}".replace(".", "-").replace("_", "-")
        self._class = name.replace("_", "-")
        self._apply_part = f"{owner.__name__}::part({name})".replace("_", "-")
        self._apply = f"{owner.__name__}".replace("_", "-")

        class Class(CSSClass):
            tagname = self._class
            is_inline = self.is_inline

        class Id(CSSId):
            tagname = self._id.lower()
            is_inline = self.is_inline

        class CSS(extension.StyleTags):
            tagname = name.replace("_", "-")
            is_inline = self.is_inline

        class Apply(extension.StyleTags):
            tagname = self._apply.lower()
            is_apply = True
            is_inline = self.is_inline

        self.cls = Class
        self.id = Id
        self.css = CSS
        self.apply = Apply


if __name__ == "__main__":

    class div(extension.Tags):
        pass

    class Order(extension.Tags):
        render_tag = False
        product_name = CSSProperty()
        product_category = CSSProperty()
        product_id = CSSProperty()

    order = Order(div("hello"))
    prod_name = Order.product_name.id(background_color="red", width="12%")
    category = Order.product_category.cls(color="#23cfff")
    prod_id = Order.product_id.apply(apply="bg-rose-500 text-rose-400")
    print(order)
    # products.attributes.update(padding="10px")
    prod_name["boxsize"] = "border-box"
    prod_name["background-color"] = "red"
    # print(prod_name)
    # print(order.product_name.css(textdecoration="none"))
    print(category)
    prod_id.add(prod_name)
    print(prod_id)
