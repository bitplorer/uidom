import unittest

import toml

from uidom import __version__
from uidom.dom import *


class TestVersion(unittest.TestCase):
    def setUp(self) -> None:
        self.version = toml.load("pyproject.toml")["tool"]["poetry"]["version"]

    def test_version(self):
        self.assertEqual(__version__, self.version)


class TestSingleTag(unittest.TestCase):
    def setUp(self) -> None:
        class SingleTagTest(SingleTags):
            tagname = "single-tag"
            child_dedent = True

        class DoubleTagTest(DoubleTags):
            tagname = "double-tag"

        self.SingleTagTest = SingleTagTest
        self.DoubleTagTest = DoubleTagTest

    def test_single_tag(self):
        # test when __render__(pretty=True)
        self.assertEqual(str(self.SingleTagTest()), "<single-tag>")
        self.assertEqual(str(self.SingleTagTest(x=1)), """<single-tag x="1">""")
        self.assertEqual(
            str(self.SingleTagTest().__render__(xhtml=True)), "<single-tag/>"
        )
        self.assertEqual(
            str(self.SingleTagTest(x=1).__render__(xhtml=True)),
            """<single-tag x="1"/>""",
        )

        # test when __render__(pretty=False)
        self.assertEqual(
            str(self.SingleTagTest().__render__(pretty=False)), "<single-tag>"
        )
        self.assertEqual(
            str(self.SingleTagTest(x=1).__render__(pretty=False)),
            """<single-tag x="1">""",
        )
        self.assertEqual(
            str(self.SingleTagTest().__render__(xhtml=True, pretty=False)),
            "<single-tag/>",
        )
        self.assertEqual(
            str(self.SingleTagTest(x=1).__render__(xhtml=True, pretty=False)),
            """<single-tag x="1"/>""",
        )

    def test_single_tag_with_children(self):
        self.assertEqual(
            str(self.SingleTagTest(self.SingleTagTest())),
            """<single-tag>\n<single-tag>""",
        )
        self.assertEqual(
            str(self.SingleTagTest(self.DoubleTagTest())),
            """<single-tag>\n<double-tag>\n</double-tag>""",
        )


class TestDoubleTag(unittest.TestCase):
    def setUp(self) -> None:
        class DoubleTagTest(DoubleTags):
            tagname = "double-tag"

        class SingleTagTest(SingleTags):
            tagname = "single-tag"

        self.DoubleTagTest = DoubleTagTest
        self.SingleTagTest = SingleTagTest

    def test_double_tag(self):
        # test when __render__(pretty=True)
        self.assertEqual(str(self.DoubleTagTest()), "<double-tag>\n</double-tag>")
        self.assertEqual(
            str(self.DoubleTagTest(x=1)),
            """<double-tag x="1">\n</double-tag>""",
        )
        self.assertEqual(
            str(self.DoubleTagTest().__render__(xhtml=True)),
            "<double-tag>\n</double-tag>",
        )
        self.assertEqual(
            str(self.DoubleTagTest(x=1).__render__(xhtml=True)),
            """<double-tag x="1">\n</double-tag>""",
        )

        # test when __render__(pretty=False)
        self.assertEqual(
            str(self.DoubleTagTest().__render__(pretty=False)),
            "<double-tag></double-tag>",
        )
        self.assertEqual(
            str(self.DoubleTagTest(x=1).__render__(pretty=False)),
            """<double-tag x="1"></double-tag>""",
        )
        self.assertEqual(
            str(self.DoubleTagTest().__render__(xhtml=True, pretty=False)),
            "<double-tag></double-tag>",
        )
        self.assertEqual(
            str(self.DoubleTagTest(x=1).__render__(xhtml=True, pretty=False)),
            """<double-tag x="1"></double-tag>""",
        )

    def test_double_tag_with_children(self):
        self.assertEqual(
            str(self.DoubleTagTest(self.DoubleTagTest())),
            str("""<double-tag>\n  <double-tag>\n  </double-tag>\n</double-tag>"""),
        )
        self.assertEqual(
            str(self.DoubleTagTest(self.SingleTagTest())),
            """<double-tag>\n  <single-tag>\n</double-tag>""",
        )


class TestRenderTag(unittest.TestCase):
    """\
        render_tag attribute test:
            checks the various use cases for rendering
    """

    def setUp(self) -> None:
        class RenderTagIsFalse(HTMLElement):
            render_tag = False

            def __checks__(self, element: extension.Tags) -> extension.Tags:
                ...

            def render(self, *args, **kwargs):
                return div(args, **kwargs)

        class RenderTagIsTrue(HTMLElement):
            render_tag = True

            def __checks__(self, element: extension.Tags) -> extension.Tags:
                ...

            def render(self, *args, **kwargs):
                return div(args, **kwargs)

        class FakeRenderTagIsTrue(DoubleTags):
            tagname = "RenderTagIsTrue"

        self.RenderTagIsFalse = RenderTagIsFalse
        self.RenderTagIsTrue = RenderTagIsTrue
        self.FakeRenderTagIsTrue = FakeRenderTagIsTrue

    def test_render_tag(self):
        # test when render_tag = False
        self.assertEqual(str(self.RenderTagIsFalse()), str(div()))
        self.assertEqual(
            str(self.RenderTagIsFalse() & self.RenderTagIsFalse()), str(div() & div())
        )

        # test when render_tag = True
        self.assertEqual(
            str(self.RenderTagIsTrue()),
            str(self.FakeRenderTagIsTrue(div())),
        )


class TestAlpine(unittest.TestCase):
    def setUp(self):
        self.alpine_component = ul(
            li(
                x_text="name",
                x_intersect_enter="opacity-100",
                x_intersect_leave="opacity-100",
                x_transition_enter="opacity-100",
            ),
            x_for="name in names",
            x_data={},
        )
        self.alpine_component_result = """\
<ul x-data='{}' x-for="name in names">
  <li x-intersect:enter="opacity-100" x-intersect:leave="opacity-100" x-text="name" x-transition:enter="opacity-100">
  </li>
</ul>"""

    def test_alpine_component(self):
        self.assertEqual(
            self.alpine_component.__render__(), self.alpine_component_result
        )


class TestJinja(unittest.TestCase):
    def setUp(self):
        self.jinja_block_template = Block(
            "nav",
            nav(
                ul(
                    For(
                        "item in menu_items",
                        li(a(Var("item.name"), href=Var("item.link"))),
                    )
                )
            ),
        )
        self.jinja_block_result = """\
{% block nav %}
  <nav>
    <ul>
      {% for item in menu_items %}
        <li>
          <a href="{{ item.link }}">
            {{ item.name }}
          </a>
        </li>
      {% endfor %}
    </ul>
  </nav>
{% endblock %}"""

        self.jinja_for_if_else_template = For(
            "name in names",
            If(
                "name",
                Block("load", Load("space")),
                Elif("njnsf", p("ksf")),
                Else(section(p("ok", Var("name")))),
            ),
        )

        self.jinja_for_if_else_result = """\
{% for name in names %}
  {% if name %}
    {% block load %}
      {% load space %}
    {% endblock %}
  {% elif njnsf %}
    <p>
      ksf
    </p>
  {% else %}
    <section>
      <p>
        ok
        {{ name }}
      </p>
    </section>
  {% endif %}
{% endfor %}"""
        self.jinja_for_loop_template = For("name in names", li(Var("name")))
        self.jinja_for_loop_result = """\
{% for name in names %}
  <li>
    {{ name }}
  </li>
{% endfor %}"""

    def test_jinja_template(self):
        return self.assertEqual(
            self.jinja_block_template.__render__(), self.jinja_block_result
        )

    def test_jinja_if_else_template(self):
        return self.assertEqual(
            self.jinja_for_if_else_template.__render__(), self.jinja_for_if_else_result
        )

    def test_jinja_for_loop(self):
        self.assertEqual(
            self.jinja_for_loop_template.__render__(), self.jinja_for_loop_result
        )


if __name__ == "__main__":
    unittest.main()
