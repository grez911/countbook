let ws = new WebSocket('ws://' + window.location.host);
let today = new Date();
let year = today.getFullYear();
let month = today.getMonth() + 1;
let day = today.getDate();
let bus = new Vue();

new Vue({
    el: '#root',
    
    mounted: function() {
        ws.onmessage = (e) => {
            response = JSON.parse(e.data);
            bus.$emit('websocket_message', response);
        }
        ws.onopen = () => {
            bus.$emit('websocket_ready');
        }
        if (ws.readyState == WebSocket.OPEN) ws.onopen();
    }
});

/*
            JSON.stringify({
                operation: "get_year",
                params: {
                    year: "2017"
                }
            })

            JSON.stringify({
                operation: "get_month",
                params: {
                    year: "2017",
                    month: "10"
                }
            })

            JSON.stringify({
                operation: "get_today"
            })

            JSON.stringify({
                operation: "append_operation",
                params: {
                    name: "jksghjkfg"
                }
            })

            JSON.stringify({
                operation: "add_operation",
                params: {
                    id: "12"
                }
            })

            JSON.stringify({
                operation: "hide_operation",
                params: {
                    id: "10"
                }
            })

            JSON.stringify({
                operation: "show_operation",
                params: {
                    id: "10"
                }
            })
*/
