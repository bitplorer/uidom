# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from dataclasses import dataclass, field, make_dataclass

from demosite.api import api
from uidom.dom import *


class chartjs(Component):
    def render(self):
        return string_to_element(
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
