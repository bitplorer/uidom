# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from demosite.api import api
from demosite.document import document
from uidom.alpinejs.dataset import DataSet, dataset_pressed, dataset_ripple
from uidom.dom import *


def data_ripple(className="", **kwargs):
    with DataSet() as _ripple:
        dataset_ripple()
        dataset_pressed()
        attr(
            className="""
            relative w-24 h-10 rounded border border-gray-300 transform transition
            [&>[data-ripple=true]]:absolute
            [&>[data-ripple=true]]:rounded-full
            [&>[data-ripple=true]]:pointer-events-none
            [&>[data-ripple=true]]:bg-rose-400
            [&>[data-ripple=true]]:animate-pulse
            %s
            """
            % className,
            **kwargs,
        )
    return _ripple


class Button(Component):
    def render(self, *args, className="", asElement=None, **kwargs):
        with data_ripple(
            className=f"overflow-hidden m-2 p-2 {className}",
            **kwargs,
        ) as ripple_btn:
            button(*args) if asElement is None else asElement(*args)
        return ripple_btn


@api.get("/ripple")
def ripp():
    with document() as doc:
        Button(
            "Hello",
            # x_bind_data_ripple_light="true",
            # asElement=a,
            className="""
            bg-rose-500 text-pink-100 items-center 
            text-center rounded-lg bg-opacity-80 font-oswald 
            leading-tight""",
        )
    return doc


class side_menu(Component):
    def render(self, menus=[]):
        with div(className="flex") as side:
            with div(className="w-1/4 min-h-screen bg-rose-600"):
                comment("Side Menu Content")
                with ul(className="py-4"):
                    for i, name in enumerate(menus):
                        if i == 0:
                            with li(
                                className="mb-2 px-4 py-2 bg-white text-gray-800 mt-2"
                            ):
                                a(name, href="#", className="block")
                        else:
                            with li(className="mb-2 px-4 py-2 bg-white text-gray-800"):
                                a(name, href="#", className="block")

            with div(className="w-3/4 min-h-screen bg-gray-100"):
                comment("Main Content")
                h1("Main Content", className="text-2xl font-bold mt-8 ml-8")
        return side


@api.get("/side_menu")
def side():
    return document(side_menu(menus=["Home", "About", "Services", "Contact"]))


class chartjs(Component):
    def render(self):
        return defHTML(
            """
<div>
  <canvas id="myChart"></canvas>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<script>
  const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
</script>
 
        """
        )


@api.get("/canvas")
def charting():
    return chartjs()


class after_load_data_refresh(object):
    # https://stackoverflow.com/a/63233817
    # Code to trigger a custom event, you'll need to fill in the payload.

    def render(self):
        raw(
            """
<button x-on:click="$dispatch("item-load")">
<div x-data=" items() " x-on:items-load.window="items = $event.detail.items">
    <template x-for=" item in items " :key=" item ">
        <div x-text=" item.name "></div>
    </template>
</div>


<script>
let event = new CustomEvent("items-load", {
  detail: {
    items: []
  }
});
window.dispatchEvent(event);
</script>
            
            """
        )


if __name__ == "__main__":
    print(side_menu())
