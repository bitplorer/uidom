# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from fastapi.responses import JSONResponse

from uidom.dom import *

from ..api import api


class chart2(ReactiveComponent):
    def render(self):
        return raw(
            """
<!DOCTYPE html>
<html>
<head>
    <title>Chart.js Example</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/alpinejs@3.12.0/dist/cdn.min.js" defer=None rel="prefetch"></script>
</head>
<body>
    <div id="my-element" x-data="{ name: 'John', age: 30 }">
  <p>Name: <span x-text="name"></span></p>
  <p>Age: <span x-text="age"></span></p>
  <button x-on:click="updateData()">Update data</button>
</div>

<script>
  document.addEventListener("alpine:init", () => {
    let myAlpineInstance = Alpine.init(document.querySelector("#my-element"));
    
    window.updateData = function() {
      let data = Alpine.$data(myAlpineInstance);
      data.name = 'Jane';
      data.age = 25;
    }
  });
</script>

    <div x-data="{ data: [] }" x-init="fetchChartData()">
        <canvas id="myChart"></canvas>
    </div>

    <script>
        function fetchChartData() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('myChart').getContext('2d');
            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'My Dataset',
                        data: data.values,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });

            setInterval(() => {
                fetch('/data')
                    .then(response => response.json())
                    .then(data => {
                        chart.data.labels = data.labels;
                        chart.data.datasets[0].data = data.data;
                        chart.update();
                    });
            }, 5000);
        });
}
    </script>
</body>
</html>
            """
        )


import random

random_data = lambda: random.randrange(0, 255, 4)


@api.get("/data")
def get_data():
    data = [random_data() for _ in range(6)]
    labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
    return JSONResponse({"labels": labels, "data": data})


@api.get("/chart2")
async def chart_2():
    return chart2()
