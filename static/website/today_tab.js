"use strict";

Vue.component('operations-list', {
    template: `
        <div>
            <div v-for="op in today" v-if="op['show'] == true">
                <a v-on:click="delOperation(op['id'])">
                    <i class="fa fa-trash-o" aria-hidden="true"></i>
                </a>
                (( op['name'] )) - (( op['count'] ))
                <a v-on:click="appendRecord(op['id'])">
                    <i class="fa fa-plus-circle" aria-hidden="true"></i>
                </a>
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
                    type: 'get_day',
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
        delOperation(id) {
            ws.send(
                JSON.stringify({
                    type: 'del_operation',
                    params: {
                        id: id
                    }
                })
            );
        },

        appendRecord(id) {
            ws.send(
                JSON.stringify({
                    type: 'append_record',
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
        <div class="field has-addons">
            <div class="control">
                <input class="input" type="text" id="append_operation" v-model="new_operation" placeholder="A new item">
            </div>
            <div class="control">
                <a class="button" v-on:click="appendOperation()">
                    Append
                </a>
            </div>
        </div>
    `,

    data() {
        return {
            new_operation: ''
        };
    },

    methods: {
        appendOperation() {
            ws.send(
                JSON.stringify({
                    type: 'append_operation',
                    params: {
                        name: this.new_operation
                    }
                })
            );
            this.new_operation = '';
        }
    }
});
