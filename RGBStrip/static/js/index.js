"use strict";

let LED_CONFIG = {};
let LEDS;
const LED_WH = 12;

function get_ws_url() {
    let host = window.location.hostname,
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

function config_has_changed(old_config, new_config) {
    return (
        old_config.type !== new_config.type
        ||
        old_config.width !== new_config.width
        ||
        old_config.height !== new_config.height
    );
}

function apply_config(new_config) {
    console.log('Applying new config!', LED_CONFIG, new_config);
    LED_CONFIG = new_config;

    // Create new LEDs in the correct configuration
    let layout;
    if (LED_CONFIG.type == 'rectangle') {
        layout = _get_leds_rectangle(LED_CONFIG);
    } else if (LED_CONFIG.type == 'cone') {
        layout = _get_leds_cone(LED_CONFIG);
    } else {
        alert('Unknown controller type: '+LED_CONFIG.type)
    }

    // Update the DOM
    let led_container = $('#led_container');
    led_container.children().remove();
    led_container.append(layout.leds);
    led_container.css({
        width: layout.width,
        height: layout.height,
    });
    LEDS = layout.leds;
}

function _get_leds_rectangle(LED_CONFIG) {
    let leds = [];
    for (let y=0; y<LED_CONFIG.height; y++) {
        for (let x=0; x<LED_CONFIG.width; x++) {
            leds.push(_make_led(y * LED_WH, x * LED_WH));
        }
    }
    return {
        leds: leds,
        width: LED_CONFIG.width * LED_WH,
        height: LED_CONFIG.height * LED_WH,
    };
}

function _get_leds_cone(LED_CONFIG) {
    console.log(LED_CONFIG);

    if (LED_CONFIG.levels[0] !== 1) {
        alert('First level must have 1 LED!');
        return;
    }

    const level_offset = 2*LED_WH;
    const centre_xy = level_offset * LED_CONFIG.levels.length;

    let leds = [];
    LED_CONFIG.levels.forEach(function(level_count, level_index) {
        const level_radius = level_index * level_offset;
        for (let led_index=0; led_index<level_count; led_index++) {
            const angle = 2 * Math.PI * led_index / level_count;
            const offset_x = Math.sin(angle) * level_radius;
            const offset_y = Math.cos(angle) * level_radius;
            leds.push(_make_led(centre_xy + offset_y, centre_xy + offset_x));
        }
    });
    return {
        leds: leds,
        width: centre_xy*2,
        height: centre_xy*2,
    };
}

function _make_led(top, left) {
    return $('<span></span>')
        .addClass('led')
        .css({
            top: top,
            left: left,
        });
}

function _get_offset(index) {
    return 4 + index * 4;
}

function get_rgba(index, bytes) {
    let offset = _get_offset(index),
        r = bytes[offset + 3],
        g = bytes[offset + 2],
        b = bytes[offset + 1],
        a = ((bytes[offset + 0] && 31) / 31);

    return 'rgba('+r+','+g+','+b+','+a+')';
}

function update_display(data) {
    if (config_has_changed(LED_CONFIG, data.config)) {
        apply_config(data.config);
    }

    // Update the LEDs
    LEDS.forEach(function(led, index) {
        let rgba = get_rgba(index, data.bytes);
        led.css('backgroundColor', rgba);
    });
}

function open_ws() {
    let ws_url = get_ws_url(),
        ws = new WebSocket(ws_url);
    ws.onmessage = function (evt) {
        update_display(JSON.parse(evt.data));
    };
}

function reload_config() {
    // Load the config from the server and show it
    let config_status = $('#config_status');
    config_status.text('Loading...');
    $.ajax(
        '/config'
    ).done(function(data, textStatus, jqXHR) {
        $('#config_input').val(data);
        config_status.text('Loaded!');
    }).fail(function(jqXHR, textStatus, errorThrown) {
        config_status.text('Error loading config!');
    });
}

function save_config() {
    // Save the config from UI to the server
    let config_status = $('#config_status');
    config_status.text('Saving...');
    $.post(
        '/config',
        $('#config_input').val()
    ).done(function(data, textStatus, jqXHR) {
        config_status.text('Saved!');
    }).fail(function(jqXHR, textStatus, errorThrown) {
        config_status.text('Error saving config!');
    });
}

function bind_handlers() {
    $('#reload_config').click(reload_config);
    $('#save_config').click(save_config);
}

function load_constants() {
    $.ajax(
        '/constants'
    ).done(function(data, textStatus, jqXHR) {
        $('#constants pre').text(JSON.stringify(data, undefined, 2));
    }).fail(function(jqXHR, textStatus, errorThrown) {
        alert('Error loading constants!');
    });
}

function main() {
    open_ws();
    bind_handlers();
    reload_config();
    load_constants();

}

$(document).ready(main);
