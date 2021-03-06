"use strict";

Vue.component('stats', {
    template: `
        <div>
            <div class="month has-text-centered">
                <a v-on:click="prevMonth()"><i class="fa fa-chevron-left" aria-hidden="true"></i></a>
                    &nbsp;(( months[month] )) - (( year ))&nbsp;
                <a v-on:click="nextMonth()"><i class="fa fa-chevron-right" aria-hidden="true"></i></a>
            </div>
            <div id="chart">
                <canvas id="mychart" ref="mychart" width="400" height="180"></canvas>
            </div>
        </div>
    `,

    delimiters: ['((', '))'],

    data() {
        return {
            myChart: null,
            stats: null,
            year: new Date().getFullYear(),
            month: new Date().getMonth(),
            months: [
                'January',
                'February',
                'March',
                'April',
                'May',
                'June',
                'July',
                'August',
                'September',
                'October',
                'November',
                'December'
            ]
        };
    },

    mounted: function() {
        bus.$on('websocket_message', (response) => {
            if (response['type'] == 'get_month') {
                this.parseStats(response['data']);
                this.createChart();
            }
            if (response['type'] == 'get_day') {
                this.getStats();
            }
        })
    },

    methods: {
        getStats: function() {
            ws.send(
                JSON.stringify({
                    type: 'get_month',
                    params: {
                        year: this.year,
                        month: this.month + 1
                    }
                })
            )
        },

        prevMonth: function () {
            if (this.month > 0) {
                this.month--;
            } else {
                this.month = 11;
                this.year--;
            }
            this.getStats();
        },

        nextMonth: function () {
            if (this.month < 11) {
                this.month++;
            } else {
                this.month = 0;
                this.year++;
            }
            this.getStats();
        },

        createChart: function () {
            let self = this;
            try {
                this.myChart.destroy();
            } 
            catch (e) {}
            this.myChart = new Chart(self.$refs.mychart.getContext('2d'), {
                type: 'bar',
                data: self.stats,
                options: {
                    tooltips: {
                        mode: 'index',
                        intersect: false
                    },
                    responsive: true,
                    scales: {
                        xAxes: [{
                            stacked: true,
                        }],
                        yAxes: [{
                            stacked: true,
                            ticks: {
                                beginAtZero:true
                            }
                        }]
                    }
                }
            })
        },

        parseStats: function(raw_stats) {
            this.stats = {
                'labels': [],
                'datasets': []
            };
            if (raw_stats.length == 0) {
                return;
            }
            for (let day in raw_stats[0]['stats']) {
                this.stats['labels'].push(day);
            }
            let palet = palette(['tol', 'qualitative'], raw_stats.length);
            let i = 0;
            raw_stats.forEach((op) => {
                let cur_dataset = {
                    label: op['name'],
                    backgroundColor: '#' + palet[i],
                    data: []
                };
                for (let day in op['stats']) {
                    cur_dataset['data'].push(op['stats'][day]);
                };
                this.stats['datasets'].push(cur_dataset);
                i++;
            });
        }
    }
});
