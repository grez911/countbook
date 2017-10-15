"use strict";

Vue.component('today', {
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
            <div class="field has-addons">
                <div class="control">
                    <input class="input" type="text" id="append_operation" v-model="new_operation" placeholder="A new item" v-on:keyup.enter="appendOperation()">
                </div>
                <div class="control">
                    <a class="button" v-on:click="appendOperation()">
                        Append
                    </a>
                </div>
            </div>
        </div>
    `,

    delimiters: ['((', '))'],

    data() {
        return {
            today: '',
            year: new Date().getFullYear(),
            month: new Date().getMonth() + 1,
            day: new Date().getDate(),
            new_operation: ''
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
            if (response['type'] === 'get_day') {
                this.today = response['data'];
            }
        })
    },

    methods: {
        delOperation(id) {
            bus.$emit('show_popup', {
                'title': 'Warning',
                'text': 'Do you really want to delete the item with all associated records?',
                'type': 'delete',
                'id': id
            });
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
        },

        appendOperation() {
            let stop = false;
            if (this.new_operation === '') {
                bus.$emit('show_popup', {
                    'title': 'Error',
                    'text': 'Please, enter a name.',
                    'type': 'error'
                });
                stop = true;
            }
            this.today.forEach((op) => {
                if (this.new_operation === op['name']) {
                    bus.$emit('show_popup', {
                        'title': 'Error',
                        'text': 'The item already exists. Please, enter a different name.',
                        'type': 'error'
                    });
                    stop = true;
                }
            });
            if (stop === true) return;
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
