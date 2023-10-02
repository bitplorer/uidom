import asyncio
import typing as t
import unittest
from dataclasses import dataclass
from textwrap import dedent

import toml

from uidom import Document, __version__
from uidom.alpinejs import DataSet
from uidom.dom import *
from uidom.dom.src.dom_tag import attr
from uidom.web_io._events import BaseEventManager


class TestVersion(unittest.TestCase):
    def setUp(self) -> None:
        self.version = toml.load("pyproject.toml")["tool"]["poetry"]["version"]

    def test_version(self):
        self.assertEqual(__version__, self.version)


class TestContext(unittest.TestCase):
    def setUp(self):
        def subcontext(*args):
            with div("sub context") as _subcontext:
                _subcontext.add(*args)
            return _subcontext

        self.subcontext = subcontext

    def test_context_child(self):
        with div("context") as context:
            self.subcontext(div("inside subcontext"))

        self.assertEqual(
            context.__render__(),
            dedent(
                """\
                <div>
                  context
                  <div>
                    sub context
                    <div>
                      inside subcontext
                    </div>
                  </div>
                </div>"""
            ),
        )


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
            render_tag = False

            def __checks__(self, element):
                ...

            def render(self, *args, **kwargs):
                return div(), div()

        class ChildAsEntryWithoutRenderTag(Component):
            render_tag = False

            def render(self, *args, **kwargs):
                # when only one html-element is returned then it becomes the entry
                # point and we can set attributes and add element to it like normal
                return "<div></div>"

        class SelfAsEntryWithoutRenderTag(Component):
            render_tag = False

            def render(self, *args, **kwargs):
                # when more than one html-element is returned then it **DOESN'T** become
                # the entry point and we CAN'T set attributes and add element to it like normal
                # we can only append element to it.
                return "<p></p><a></a>"

        class SelfAsEntryWithRenderTagMoreElement(Component):
            render_tag = True
            tagname = "self-entry"

            def __checks__(self, element):
                ...

            def render(self, *args, **kwargs):
                return "<p></p><a></a>"

        class SelfAsEntryWithRenderTagReturnsOneElement(Component):
            render_tag = True
            tagname = "self-entry"

            def __checks__(self, element):
                ...

            def render(self, *args, **kwargs):
                return "<zzz></zzz>"

        self.RenderReturnsNone = RenderReturnsNone
        self.RenderReturnsEllipses = RenderReturnsEllipses
        self.RenderReturnsMoreThanOneElement = RenderReturnsMoreThanOneElement
        self.ChildAsEntryWithoutRenderTag = ChildAsEntryWithoutRenderTag
        self.SelfAsEntryWithoutRenderTag = SelfAsEntryWithoutRenderTag
        self.SelfAsEntryWithRenderTagReturnsOneElement = (
            SelfAsEntryWithRenderTagReturnsOneElement
        )
        self.SelfAsEntryWithRenderTagMoreElement = SelfAsEntryWithRenderTagMoreElement

    def test_render_returns_fails(self):
        with self.assertRaises(ValueError):
            self.RenderReturnsNone()

        with self.assertRaises(ValueError):
            self.RenderReturnsEllipses()

        returns_more_than_one_element = self.RenderReturnsMoreThanOneElement()
        self.assertEqual(
            returns_more_than_one_element.__render__(), "<div>\n</div>\n<div>\n</div>"
        )
        child_entry_without_render_tag = self.ChildAsEntryWithoutRenderTag()
        child_entry_without_render_tag.add(div())
        child_entry_without_render_tag["class"] = "xyz"
        self.assertEqual(
            child_entry_without_render_tag.__render__(),
            """\
<div class="xyz">
  <div>
  </div>
</div>""",
        )
        self_entry_without_render_tag = self.SelfAsEntryWithoutRenderTag()
        self_entry_without_render_tag.add(p())
        self_entry_without_render_tag["class"] = "xyz"  # this will have no effect
        self.assertEqual(
            self_entry_without_render_tag.__render__(),
            """\
<p>
</p>
<a>
</a>
<p>
</p>""",
        )

        self_entry_with_render_tag_returns_one_element = (
            self.SelfAsEntryWithRenderTagReturnsOneElement()
        )
        self_entry_with_render_tag_returns_one_element.add(div())
        self_entry_with_render_tag_returns_one_element["class"] = "xyz"
        self_entry_with_render_tag_returns_one_element["id"] = "#some_id"
        self.assertEqual(
            self_entry_with_render_tag_returns_one_element.__render__(),
            """\
<self-entry class="xyz" id="#some_id">
  <zzz>
  </zzz>
  <div>
  </div>
</self-entry>""",
        )
        self_entry_with_render_tag_returns_more_element = (
            self.SelfAsEntryWithRenderTagMoreElement()
        )
        self_entry_with_render_tag_returns_more_element["class"] = "xyz"
        self_entry_with_render_tag_returns_more_element.add(div())
        self.assertEqual(
            self_entry_with_render_tag_returns_more_element.__render__(),
            """\
<self-entry class="xyz">
  <p>
  </p>
  <a>
  </a>
  <div>
  </div>
</self-entry>""",
        )


class TestStates(unittest.TestCase):
    def setUp(self):
        @dataclass(eq=False)
        class StateElement(ReactiveComponent):
            a: int

            def __post_init__(self):
                super(StateElement, self).__init__(a=self.a)

            def render(self, a):  # type: ignore[override]
                return p(a=a)

        self.document = Document()
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

    def test_state_with_document(self):
        with self.document() as doc:
            with div():
                state_elem = self.StateElement(1)
        state_elem.a += 1
        state_elem += "Hello Mom"
        state_elem += MarkdownElement("*Hello World*")
        result = """\
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui" name="viewport">
  </head>
  <body>
    <div>
      <p a="2">
        Hello Mom
        <p>
          <em>
            Hello World
          </em>
        </p>
      </p>
    </div>
  </body>
</html>"""
        self.assertEqual(doc.__render__(), result)

    def test_states_mutation_with_parent_child(self):
        with div("state parent") as parent:
            with self.StateElement(a=2) as state_elem:
                child = div("state child")

        self.assertEqual(state_elem.parent, parent)
        self.assertIn(state_elem, parent)
        self.assertEqual(child.parent, state_elem)
        self.assertIn(child, state_elem)
        self.assertNotIn(div("state child"), state_elem)
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
        self.assertIn(state_elem, parent)
        self.assertEqual(child.parent, state_elem)
        self.assertIn(child, state_elem)
        self.assertNotIn(div("state child"), state_elem)

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


class TestMarkdown(unittest.TestCase):
    def setUp(self):
        md_string = """\
# Last year’s snowfall
```python
    def main(): pass
```
```shell 
pip install uidom
```

## The snowfall was above average.
It was followed by a warm spring which caused
flood conditions in many of the nearby rivers.
"""
        parsed_md_string = """\
<h1>
  Last year’s snowfall
</h1>
<pre><code class="language-python">def main(): pass</code></pre>
<pre><code class="language-shell">pip install uidom</code></pre>
<h2>
  The snowfall was above average.
</h2>
<p>
  It was followed by a warm spring which caused
  flood conditions in many of the nearby rivers.
</p>"""

        class MarkdownCheck(MarkdownElement):
            def render(self):
                return md_string

        self.MarkdownCheck = MarkdownCheck
        self.md_string = md_string
        self.parsed_md_string = parsed_md_string

    def test_markdown(self):
        self.assertEqual(self.MarkdownCheck().__render__(), self.parsed_md_string)
        self.assertEqual(
            MarkdownElement(self.md_string).__render__(), self.parsed_md_string
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
        self.assertIn(JinjaBaseTag, nav(ul(self.jinja_for_loop_template)))


class TestEventManager(unittest.TestCase):
    def setUp(self) -> None:
        class ClickEvents(BaseEventManager):
            def on_press(self, event: t.Union[str, t.Callable]) -> t.Callable:
                return self.set_event(activity="click", event_name_or_method=event)

            def on_mouseover(self, event: t.Union[str, t.Callable]):
                return self.set_event(activity="mouse", event_name_or_method=event)

            def on_mousedown(self, event: t.Union[str, t.Callable]) -> t.Callable:
                return self.set_event(activity="mouse", event_name_or_method=event)

            @property
            def mouse_events(self):
                return self.get_events(activity="mouse")

            @property
            def click_events(self):
                return self.get_events(activity="click")

        class ClickCounter:
            events = ClickEvents()

            def __init__(self):
                self.clicks = 0

            @events.on_press("increment")
            def increment(self, count):
                self.clicks += count
                return self.clicks

            @events.on_mouseover
            @events.on_press
            def decrement(self, count):
                if self.clicks - count >= 0:
                    self.clicks -= count
                return self.clicks

            def to_dict(self):
                return {
                    "clicks": self.clicks,
                }

        self.counter = ClickCounter()

    def test_click_events(self):
        async def main():
            for callback in self.counter.events.click_events["increment"]:
                await callback(self.counter, count=3)
                self.assertEqual(self.counter.clicks, 3)

            for callback in self.counter.events.click_events["decrement"]:
                await callback(self.counter, count=2)
                self.assertEqual(self.counter.clicks, 1)

            for callback in self.counter.events.mouse_events["decrement"]:
                await callback(self.counter, count=1)
                self.assertEqual(self.counter.clicks, 0)

        # here only one method is added thats why both list can be equal
        # but its not necessary as any activity in EventManager can add
        #
        self.assertEqual(
            self.counter.events.click_events["increment"],
            self.counter.events["increment"],
        )

        asyncio.run(main())


class TestFragments(unittest.TestCase):
    def setUp(self):
        self.Fragment = Fragment
        self.MergeClassAttribute = MergeClassAttribute
        self.DataSet = DataSet

    def test_fragment(self):
        with self.Fragment() as fragment:
            attr(className="class_a")
            attr(className="class_b")
            div("a", className="old_class_a")
            div("b", className="old_class_b")

        # class_a is overridden by class_b here as class attributes are not merged
        # in Fragments but attributes of child elements of Fragments and Fragments
        # are merged together on child elements nicely.
        # we see class attributes of div's are preserved and new class attributes
        # are merged with old classes.

        self.assertEqual(
            fragment.__render__(),
            dedent(
                """\
                <div class="old_class_a class_b">
                  a
                </div>
                <div class="old_class_b class_b">
                  b
                </div>"""
            ),
        )

        with self.MergeClassAttribute() as merged_class_attr:
            attr(className="class_a")
            attr(className="class_b")
            div("a")
            div("b")

        self.assertEqual(
            merged_class_attr.__render__(),
            dedent(
                """\
                <div class="class_a class_b">
                  a
                </div>
                <div class="class_a class_b">
                  b
                </div>"""
            ),
        )
        # with DataSet class we can merge not only classes on children but also
        # x-data attributes, x-on events and x-transition and more.
        with self.DataSet() as data_set_test:
            attr(className="attr1", x_data="{'attr1_data': 'attr1'}")
            attr(className="attr2", x_data="{'attr2_data': 'attr2'}")
            div("a", className="attr_a", x_data="{'a_data': 'a'}")
            div("b", className="attr_b", x_data="{'b_data': 'b'}")

        self.assertEqual(
            data_set_test.__render__(),
            dedent(
                """\
                <div class="attr_a attr1 attr2" x-data="{'a_data': 'a', 'attr1_data': 'attr1', 'attr2_data': 'attr2'}">
                  a
                </div>
                <div class="attr_b attr1 attr2" x-data="{'b_data': 'b', 'attr1_data': 'attr1', 'attr2_data': 'attr2'}">
                  b
                </div>"""
            ),
        )


# class TestDocumentHead(unittest.TestCase):
#     def setUp(self) -> None:
#         self.document = HtmlDocument

#     def test_head(self):
#         with self.document(ensure_csrf_token=False) as doc:
#             with div() as dv:
#                 x = Head(title("Test Title"))

#         self.assertIn(x, doc)


if __name__ == "__main__":
    unittest.main()
