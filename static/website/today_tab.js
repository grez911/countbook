Vue.component('operations-list', {
    template: `
        <div>
            <div v-for="op in today" v-if="op['show'] == true">
                (( op['name'] )) - (( op['count'] ))
                <button v-on:click="append_record(op['id'])">+</button>
            </div>
        </div>
    `,

    delimiters: ['((', '))'],

    data() {
        return {
            today: '',
            year: new Date().getFullYear(),
            month: new Date().getMonth() + 1,
            day: new Date().getDate()
        };
    },

    mounted: function() {
        bus.$on('websocket_ready', () => 
            ws.send(
                JSON.stringify({
                    operation: 'get_day',
                    params: {
                        year: this.year,
                        month: this.month,
                        day: this.day
                    }
                })
            )
        );
        bus.$on('websocket_message', (response) => {
            if (response['type'] == 'get_day') {
                this.today = response['data'];
            }
        })
    },

    methods: {
        append_record(id) {
            ws.send(
                JSON.stringify({
                    operation: 'append_record',
                    params: {
                        id: id
                    }
                })
            );
        }
    }
});

Vue.component('append-operation', {
    template: `
        <div>
            <input type="text" id="append_operation" v-model="new_operation">
            <button v-on:click="append_operation()">Append</button>
        </div>
    `,

    data() {
        return {
            new_operation: ''
        };
    },

    methods: {
        append_operation() {
            ws.send(
                JSON.stringify({
                    operation: 'append_operation',
                    params: {
                        name: this.new_operation
                    }
                })
            );
            this.new_operation = '';
        }
    }
});
