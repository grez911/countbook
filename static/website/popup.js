"use strict";

Vue.component('popup', {
    template: `
        <div class="modal" v-bind:class="{ 'is-active': show }">
            <div class="modal-background"></div>
            <div class="modal-card">
                <header class="modal-card-head">
                    <p class="modal-card-title">(( title ))</p>
                    <button class="delete" aria-label="close" v-on:click="close()"></button>
                </header>
                <section class="modal-card-body">
                    (( text ))
                </section>
                <footer class="modal-card-foot">
                    <button class="button is-danger" v-if="type === 'delete'">Delete</button>
                    <button class="button" v-if="type === 'delete'" v-on:click="close()">Cancel</button>
                    <button class="button is-primary" v-if="type === 'error'" v-on:click="close()">OK</button>
                </footer>
            </div>
        </div>
    `,

    delimiters: ['((', '))'],

    data() {
        return {
            title: null,
            text: null,
            type: null,
            show: false
        };
    },

    mounted: function() {
        bus.$on('show_popup', (params) => {
            this.show = true;
            this.title = params['title'];
            this.text = params['text'];
            this.type = params['type'];
        })
    },

    methods: {
        close() {
            this.show = false;
        }
    }
});
