# Copyright (c) 2023 UiDOM
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import datetime
from dataclasses import dataclass

from fastapi import APIRouter

from demosite.document import document
from uidom.dom import *
from uidom.routing import HTMLRoute, StreamingRoute
from uidom.slots import x_slot

__all__ = ["x_chart", "chart_router"]

chart_router = APIRouter(route_class=StreamingRoute, tags=["Charts"])


class PriceChartTemplate(XComponent):
    
    def render(self, tag_name):
        with template(x_component=tag_name) as _chart:
            html_string_to_element(
                """
        <div class="flex items-center justify-center p-4 bg-stone-600" x-data="{...productTicker(), ...$el.parentElement.data()}" x_effect="console.log(productTicker());">
    <div class="w-full overflow-hidden rounded shadow-xl md:flex" style="max-width:900px">
        <div class="flex items-center w-full px-5 pt-8 pb-4 text-white md:w-1/2 bg-slate-500">
            <canvas x-bind:id="chartid" class="w-full"></canvas>
        </div>
        <div class="flex items-center w-full p-10 text-gray-600 bg-gray-100 md:w-1/2" x-data="renderChart" x-init="renderChart">
            <div class="w-full">
                <h3 class="text-lg font-semibold leading-tight text-gray-800" x-text="productname"></h3>
                <h6 class="mb-2 text-sm leading-tight"><span x-text="sellername"></span>&nbsp;&nbsp;-&nbsp;&nbsp;<span class="text-[#456782]" x-text="date"></h6>
                <div class="flex items-end w-full mb-6">
                    <span class="block text-3xl leading-none text-gray-800" x-text="price.current.comma_formatter()">0</span>
                    <span class="block ml-4 text-sm leading-5 text-green-500" x-text="`${price.current-price.open<0?'▼':'▲'} ${(price.current-price.open).toFixed(3)} (${(((price.current/price.open)*100)-100).toFixed(3)}%)`"></span>
                </div>
                <div class="flex w-full text-xs">
                    <div class="flex w-5/12">
                        <div class="flex-1 pr-3 font-semibold text-left">Open</div>
                        <div class="flex-1 px-3 text-right" x-text="price.open.toFixed(3)">0</div>
                    </div>
                    <div class="flex w-7/12">
                        <div class="flex-1 px-3 font-semibold text-left whitespace-nowrap">Retail Sales</div>
                        <div class="flex-1 pl-3 text-right" x-text="price.sales.m_formatter()">0</div>
                    </div>
                </div>
                <div class="flex w-full text-xs">
                    <div class="flex w-5/12">
                        <div class="flex-1 pr-3 font-semibold text-left">High</div>
                        <div class="px-3 text-right" x-text="price.high.toFixed(3)">0</div>
                    </div>
                    <div class="flex w-7/12">
                        <div class="flex-1 px-3 font-semibold text-left">P/E ratio</div>
                        <div class="pl-3 text-right" x-text="price.ratio.toFixed(2)">0</div>
                    </div>
                </div>
                <div class="flex w-full text-xs">
                    <div class="flex w-5/12">
                        <div class="flex-1 pr-3 font-semibold text-left">Low</div>
                        <div class="px-3 text-right" x-text="price.low.toFixed(3)">0</div>
                    </div>
                    <div class="flex w-7/12">
                        <div class="flex-1 px-3 font-semibold text-left">Price Change</div>
                        <div class="pl-3 text-right" x-text="`${price.change}%`">0%</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
        """
            )

        return _chart

x_chart_script = script(
            raw(
                """
    Number.prototype.m_formatter = function() {
    return this > 999999 ? (this / 1000000).toFixed(1) + 'M' : (this > 9999 ? (this / 100000).toFixed(1) + 'L': (this > 999 ? (this / 1000).toFixed(1) + 'K': this))
};
    Number.prototype.comma_formatter = function() {
    return this.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}
let productTicker = function(){
    return {
        productname: 'Gold',
        sellername: 'Prakash Jewellers',
        date: 'Aug 2nd 4:00pm AEST',
        chartid: 'chart',
        price: {
            current: 2.320,
            open: 2.230,
            low: 2.215,
            high: 2.325,
            sales: 93765011,
            ratio: 20.10,
            change: 1.67
        },
        chartdata: {
            labels: ['10:00','','','','12:00','','','','2:00','','','','4:00'],
            data: [2.23,2.215,2.22,2.25,2.245,2.27,2.28,2.29,2.3,2.29,2.325,2.325,2.32],
        },
        renderChart: function(){
            let c = false;

            Chart.helpers.each(Chart.instances, function(instance) {
                if (instance.chart.canvas.id == this.chartid) {
                    c = instance;
                }
            });

            if(c) {
                c.destroy();
            }

            let ctx = document.getElementById(this.chartid).getContext('2d');

            let chart = new Chart(ctx, {
                type: "line",
                data: {
                    labels: this.chartdata.labels,
                    datasets: [
                        {
                            label: '',
                            backgroundColor: "rgba(255, 60, 80, 0.1)",
                            borderColor: "rgba(255, 255, 255, 1)",
                            pointBackgroundColor: "rgba(255, 255, 255, 1)",
                            data: this.chartdata.data,
                        },
                    ],
                },
                layout: {
                    padding: {
                        right: 10
                    }
                },
                options: {
                    legend: {
                        display: false,
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                fontColor: "rgba(255, 255, 255, 1)",
                            },
                            gridLines: {
                                display: false,
                            },
                        }],
                        xAxes: [{
                            ticks: {
                                fontColor: "rgba(255, 255, 255, 1)",
                            },
                            gridLines: {
                                color: "rgba(255, 255, 255, .2)",
                                borderDash: [5, 5],
                                zeroLineColor: "rgba(255, 255, 255, .6)",
                                zeroLineBorderDash: [5, 5]
                            },
                        }]
                    }
                }
            });
        }
    }
}
"""
            )
        )

x_chart = PriceChartTemplate(tag_name="chart")

@chart_router.get("/chart")
async def chartbox():
    return document(
        x_chart(
            productname="Silver",
            sellername="Hiranya Jewellers",
            date=datetime.datetime.now().strftime("%H:%M, %b %d, %Y IST"),
            price={
                "current": 71000,
                "open": 70000,
                "high": 75000,
                "low": 60000,
                "sales": 3000000,
                "change": "0",
            },
            chartdata={"labels": ["Jan", "Feb"], "data": ["50000", "2000"]},
            chartid="chart1",
            id="silver-price-chart",
        ),
        x_chart,
        x_chart_script
        # x_slot
    )
