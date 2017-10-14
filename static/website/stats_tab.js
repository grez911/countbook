Vue.component('stats', {
    template: `
        <div>
            <canvas id="mychart" ref="mychart" width="400" height="150"></canvas>
        </div>
    `,

    delimiters: ['((', '))'],

    data() {
        return {
            myChart: null,
            stats: null
        };
    },

    mounted: function() {
        bus.$on('websocket_message', (response) => {
            if (response['type'] == 'get_month') {
                this.parseStats(response['data']);
                this.createChart();
            }
            if (response['type'] == 'get_day') {
                ws.send(
                    JSON.stringify({
                        operation: 'get_month',
                        params: {
                            year: year,
                            month: month
                        }
                    })
                )
            }
        })
    },

    methods: {
        createChart: function () {
            let self = this;
            myChart = null;
            myChart = new Chart(self.$refs.mychart.getContext('2d'), {
                type: 'bar',
                data: self.stats,
                options: {
                    title:{
                        display: true,
                        text: month
                    },
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
            for (let day in raw_stats[0]['stats']) {
                this.stats['labels'].push(day);
            }
            raw_stats.forEach((op) => {
                let cur_dataset = {
                    label: op['name'],
                    backgroundColor: 'rgba(255, 99, 132, 0.4)',
                    data: []
                };
                for (let day in op['stats']) {
                    cur_dataset['data'].push(op['stats'][day]);
                };
                this.stats['datasets'].push(cur_dataset);
            });
        }
    }
});
