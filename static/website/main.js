"use strict";

let ws = new ReconnectingWebSocket('ws://' + window.location.host);
let bus = new Vue();

new Vue({
    el: '#root',
    
    mounted: function() {
        ws.onmessage = (e) => {
            let response = JSON.parse(e.data);
            bus.$emit('websocket_message', response);
        }
        ws.onopen = () => {
            bus.$emit('websocket_ready');
        }
        if (ws.readyState == WebSocket.OPEN) ws.onopen();
    }
});
