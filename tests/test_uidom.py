import asyncio
import unittest
from dataclasses import dataclass

import toml

from uidom import __version__
from uidom.dom import *
from uidom.web_io._events import EventsManager


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
            str(self.DoubleTagTest(x=1)), """<double-tag x="1">\n</double-tag>"""
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
            """<double-tag>\n  <double-tag>\n  </double-tag>\n</double-tag>""",
        )
        self.assertEqual(
            str(self.DoubleTagTest(self.SingleTagTest())),
            """<double-tag>\n  <single-tag>\n</double-tag>""",
        )


class TestComponentCheck(unittest.TestCase):
    """`__check__` method tests:"""

    def setUp(self):
        class ComponentCheckRaiseError(Component):
            def __checks__(self, element):
                raise ValueError()

            def render(self, *args, **kwargs):
                return div(args, **kwargs)

        self.ComponentCheckRaiseError = ComponentCheckRaiseError

    def test_check(self):
        with self.assertRaises(ValueError):
            self.ComponentCheckRaiseError()


class TestRenderTag(unittest.TestCase):
    """\
        `render_tag` attribute test:
            checks the various use cases for rendering
    """

    def setUp(self) -> None:
        class ComponentRenderTagIsFalse(Component):
            render_tag = False

            def __checks__(self, element):
                ...

            def render(self, *args, **kwargs):
                return div(args, **kwargs)

        class ComponentRenderTagIsTrue(Component):
            render_tag = True

            def __checks__(self, element):
                ...

            def render(self, *args, **kwargs):
                return div(args, **kwargs)

        class FakeComponentRenderTagIsTrue(DoubleTags):
            tagname = "ComponentRenderTagIsTrue"

        self.ComponentRenderTagIsFalse = ComponentRenderTagIsFalse
        self.ComponentRenderTagIsTrue = ComponentRenderTagIsTrue
        self.FakeComponentRenderTagIsTrue = FakeComponentRenderTagIsTrue

    def test_render_tag(self):
        # test when render_tag = False
        self.assertEqual(str(self.ComponentRenderTagIsFalse()), str(div()))
        self.assertEqual(
            str(self.ComponentRenderTagIsFalse() & self.ComponentRenderTagIsFalse()),
            str(div() & div()),
        )

        # test when render_tag = True
        self.assertEqual(
            str(self.ComponentRenderTagIsTrue()),
            str(self.FakeComponentRenderTagIsTrue(div())),
        )


class TestComponentRenderReturns(unittest.TestCase):
    """Tests what Component return from `render` method"""

    def setUp(self) -> None:
        class RenderReturnsNone(Component):
            render_tag = True

            def __checks__(self, element):
                ...

            def render(self, *args, **kwargs):
                return

        class RenderReturnsEllipses(Component):
            render_tag = True

            def __checks__(self, element):
                ...

            def render(self, *args, **kwargs):
                return ...

        class RenderReturnsMoreThanOneElement(Component):
            render_tag = True

            def __checks__(self, element):
                ...

            def render(self, *args, **kwargs):
                return div(), div()

        self.RenderReturnsNone = RenderReturnsNone
        self.RenderReturnsEllipses = RenderReturnsEllipses
        self.RenderReturnsMoreThanOneElement = RenderReturnsMoreThanOneElement

    def test_render_returns_fails(self):
        with self.assertRaises(ValueError):
            self.RenderReturnsNone()

        with self.assertRaises(ValueError):
            self.RenderReturnsEllipses()

        with self.assertRaises(ValueError):
            self.RenderReturnsMoreThanOneElement()


class TestStates(unittest.TestCase):
    def setUp(self):
        @dataclass(eq=False)
        class StateElement(ReactiveComponent):
            a: int

            def __post_init__(self):
                super(StateElement, self).__init__(a=self.a)

            def render(self, a):  # type: ignore[override]
                return p(a=a)

        self.StateElement = StateElement

    def test_states_mutation_updates_dictionary(self):
        state_elem = self.StateElement(a=2)
        self.assertEqual(state_elem.to_dict(), {"a": 2})
        state_elem.a += 1
        self.assertEqual(state_elem.to_dict(), {"a": 3})

    def test_states_mutation_rerenders_element(self):
        state_elem = self.StateElement(a=2)
        self.assertEqual(str(state_elem), """<p a="2">\n</p>""")
        state_elem.a += 1
        self.assertEqual(str(state_elem), """<p a="3">\n</p>""")

    def test_states_mutation_with_parent_child(self):
        with div("state parent") as parent:
            with self.StateElement(a=2) as state_elem:
                child = div("state child")

        self.assertEqual(state_elem.parent, parent)
        self.assertEqual(child.parent, state_elem)

        self.assertEqual(
            parent.__render__(),
            """\
<div>
  state parent
  <p a="2">
    <div>
      state child
    </div>
  </p>
</div>""",
        )

        self.assertEqual(
            state_elem.__render__(),
            """\
<p a="2">
  <div>
    state child
  </div>
</p>""",
        )

        state_elem.a += 1
        self.assertEqual(state_elem.parent, parent)
        self.assertEqual(child.parent, state_elem)

        self.assertEqual(
            parent.__render__(),
            """\
<div>
  state parent
  <p a="3">
    <div>
      state child
    </div>
  </p>
</div>""",
        )

        self.assertEqual(
            state_elem.__render__(),
            """\
<p a="3">
  <div>
    state child
  </div>
</p>""",
        )


class TestAndOperatorWithTags(unittest.TestCase):
    def setUp(self):
        class IsInlinedTag(Component):
            is_inline = True

            def render(self, *args, **kwargs):
                return p(*args, **kwargs)

        class IsNotInlinedTag(Component):
            is_inline = False

            def render(self, *args, **kwargs):
                return p(*args, **kwargs)

        self.IsInlinedTag = IsInlinedTag
        self.IsNotInlinedTag = IsNotInlinedTag

    def test_and_operator_with_tags(self):
        self.assertEqual(
            (self.IsInlinedTag() & self.IsNotInlinedTag()).__render__(),
            str(p(__inline=True) & p()),
        )
        self.assertEqual(
            (self.IsNotInlinedTag() & self.IsInlinedTag()).__render__(),
            str(p() & p(__inline=True)),
        )


class TestAlpine(unittest.TestCase):
    def setUp(self):
        with ul() as alpine_component:
            with template(x_for="name in names", x_data={}):
                li(
                    x_text="name",
                    x_intersect_enter="opacity-100",
                    x_intersect_leave="opacity-100",
                    x_transition_enter="opacity-100",
                )
        self.alpine_component = alpine_component
        self.alpine_component_result = """\
<ul>
  <template x-data='{}' x-for="name in names">
    <li x-intersect:enter="opacity-100" x-intersect:leave="opacity-100" x-text="name" x-transition:enter="opacity-100">
    </li>
  </template>
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


class TestEventManager(unittest.TestCase):
    def setUp(self) -> None:
        click_events = EventsManager()

        class ClickCounter:
            def __init__(self):
                self.clicks = 0

            @click_events.on_receive("increment")
            def increment(self, count):
                self.clicks += count
                return self.clicks

            def to_dict(self):
                return {
                    "clicks": self.clicks,
                }

        self.counter = ClickCounter()
        self.click_events = click_events

    def test_click_events(self):
        async def main():
            for callback in self.click_events.receive_events["increment"]:
                await callback(self.counter, count=3)
                self.assertEqual(self.counter.clicks, 3)

            for calbk in self.click_events["increment"]:
                print(calbk)

        asyncio.run(main())


if __name__ == "__main__":
    unittest.main()
