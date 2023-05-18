# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.src.main import extension

__all__ = ["CSSClass", "CSSId", "CSS", "CSSProperty", "Keyframes"]


class CSS(extension.StyleTags):
    pass


class CSSClass(extension.StyleTags):
    tagname_prefix = "."
    is_inline = True


class CSSId(extension.StyleTags):
    tagname_prefix = "#"
    is_inline = True


class Keyframes(extension.StyleTags):
    tagname_prefix = "@keyframes "
    attribute_joiner = "%s %s"

    class EmptyStyleTag(extension.StyleTags):
        tagname = ""
        is_inline = True

    def _render_attribute(self, /, sb, indent_level, indent_str, pretty, xhtml):
        for key, value in self.attributes.items():
            if not isinstance(value, (dict, self.EmptyStyleTag)):
                raise TypeError(
                    f"{key}={value} is not dict or {self.EmptyStyleTag.__class__} type"
                )
            if not isinstance(value, self.EmptyStyleTag):
                self.attributes[key] = self.EmptyStyleTag(value)
        return super()._render_attribute(sb, indent_level, indent_str, pretty, xhtml)

    @staticmethod
    def _to_kebab_case(string):
        kebab_string = ""
        for i, char in enumerate(string):
            if char.isupper():
                if i > 0:
                    kebab_string += "-"
                kebab_string += char.lower()
            else:
                kebab_string += char
        return kebab_string

    def _clean_name(self, name):
        name = name.replace("_", "-")
        name = self._to_kebab_case(name)
        return super()._clean_name(name)


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
            attribute_joiner = "@%s %s;"
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

    order = Order()
    prod_name = Order.product_name.id(background_color="red", width="12%")
    category = Order.product_category.cls(color="#23cfff")
    prod_id = Order.product_id.apply(apply="bg-rose-500 text-rose-400")
    # products.attributes.update(padding="10px")
    prod_name["boxsize"] = "border-box"
    prod_name["background-color"] = "red"
    # print(order.product_name.css(textdecoration="none"))
    print(category)
    prod_id.add(prod_name)

    class chart_animation(Keyframes):
        pass

    x = chart_animation(
        _from=dict(transform="translateX(0%)", height="10px"),
        to=dict(transform="translateX(100%)"),
    )
    print(x)
