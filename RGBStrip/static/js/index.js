console.log('Hello!');

function get_ws_url() {
    console.log('get_ws_url');
    var host = window.location.hostname,
        port = window.location.port,
        ws_url = '';
    if (window.location.protocol == 'https:') {
        ws_url += 'wss';
    } else {
        ws_url += 'ws';
    }
    ws_url += '://' + host;
    if (port) {
        ws_url += ':' + port;
    }
    ws_url += '/ws';

    return ws_url;
}

function _has_changed(old_config, new_config) {
    return (
        old_config.width !== new_config.width
        ||
        old_config.height !== new_config.height
        ||
        old_config.reverse_x !== new_config.reverse_x
        ||
        old_config.reverse_y !== new_config.reverse_y
    );
}

function _apply_config(new_config) {
    console.log('Applying new config!', led_config, new_config);
    led_config = new_config;

    var led_container = document.getElementById('led_container');

    // Remove everything previously created
    while (led_container.firstChild) {
        led_container.removeChild(led_container.firstChild);
    }
    leds = [];

    // Add new LEDs in the correct configuration
    for (var y=0; y<led_config.height; y++) {
        // Add a row container
        var row_container = document.createElement('span');
        row_container.classList.add('row_container');
        led_container.appendChild(row_container);

        var led_row = [];
        for (var x=0; x<led_config.width; x++) {
            // Add an LED
            var led = document.createElement('span');
            led.classList.add('led');
            row_container.appendChild(led);
            led_row.push(led);
        }
        leds.push(led_row);
    }
}



function _get_offset(index) {
    return 4 + index * 4;
}

function _get_index(x, y) {
    if (led_config.reverse_x) {
        x = led_config.width - x - 1;
    }
    if (led_config.reverse_y) {
        y = led_config.height - y - 1;
    }
    return (y * led_config.width) + (y % 2 === 0 ? x : led_config.width - x - 1);
}

function get_rgba(index, bytes) {
    var offset = _get_offset(index);
    var rgba = (
        'rgba(' + bytes[offset + 3]
        + ',' + bytes[offset + 2]
        + ',' + bytes[offset + 1]
        + ',' + ((bytes[offset + 0] && 31) / 31)
        + ')'
    );
    if (rgba == 'rgba(0,0,0,1)') {
        return 'white';
    }
    return rgba;
}

function get_rgba_xy(x, y, bytes) {
    var index = _get_index(x, y);
    return get_rgba(index, bytes);
}



var led_config = {}, leds;
function update_display(data) {
    if (_has_changed(led_config, data.config)) {
        _apply_config(data.config);
    }

    // Update the LEDs
    for (var y=0; y<led_config.height; y++) {
        for (var x=0; x<led_config.width; x++) {
            var rgba = get_rgba_xy(x, y, data.bytes);
            leds[y][x].style.backgroundColor = rgba;
        }
    }
}

function open_ws() {
    var message_count=0,
        ws_url = get_ws_url(),
        ws = new WebSocket(ws_url);
    ws.onopen = function() {
        console.log('onopen');
    };
    ws.onmessage = function (evt) {
        message_count += 1;
        // console.log('onmessage');
        // document.getElementById('ws_count').innerHTML = message_count;
        // document.getElementById('ws_msg').innerHTML = evt.data;
        update_display(JSON.parse(evt.data));
    };
}

function bind_handlers() {
    document.getElementById('reload_config');
    document.getElementById('save_config');
}

function main() {
    console.log('main');
    open_ws();
    bind_handlers();
}

document.addEventListener('DOMContentLoaded', main);
