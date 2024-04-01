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
    // If type has changed, definitely need to reload
    if (old_config.type !== new_config.type) return true;

    if (old_config.type == 'rectangle') {
        return (
            old_config.width !== new_config.width
            ||
            old_config.height !== new_config.height
            ||
            old_config.reverse_x !== new_config.reverse_x
            ||
            old_config.reverse_y !== new_config.reverse_y
        );
    } else if (old_config.type == 'cone') {
        return (
            // Cone controllers
            old_config.extra_leds !== new_config.extra_leds
            ||
            old_config.reverse !== new_config.reverse
            ||
            old_config.levels.toString() !== new_config.levels.toString()
        );
    } else if (old_config.type == 'boards') {
        return (
            old_config.boards_wide !== new_config.boards_wide
            ||
            old_config.boards_high !== new_config.boards_high
        );
    } else {
        throw new Error(`Unknown controller type: ${old_config.type}`);
    }
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
    } else if (LED_CONFIG.type == 'boards') {
        const RECT_CONFIG = {
            height: LED_CONFIG.boards_high * 8,
            width: LED_CONFIG.boards_wide * 32,
            reverse_x: false,
            reverse_y: false,
        }
        layout = _get_leds_rectangle(RECT_CONFIG);
    } else {
        throw new Error(`Unknown controller type: ${LED_CONFIG.type}`);
    }

    // Update the DOM
    const led_container = $('#led_container');
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
            let ax=x, ay=y;

            // Account for reverse configs
            if (LED_CONFIG.reverse_x) {
                ax = LED_CONFIG.width - ax - 1;
            }
            if (LED_CONFIG.reverse_y) {
                ay = LED_CONFIG.height - ay - 1;
            }

            // Account for "snaking" of LED string
            if (ay % 2 == 1) {
                ax = LED_CONFIG.width - ax - 1;
            }

            leds.push(_make_led(ay * LED_WH, ax * LED_WH));
        }
    }
    return {
        leds: leds,
        width: LED_CONFIG.width * LED_WH,
        height: LED_CONFIG.height * LED_WH,
    };
}

function _get_leds_cone(LED_CONFIG) {
    const level_offset = 2*LED_WH;
    let centre_xy = level_offset * LED_CONFIG.levels.length;
    let centre_offset = 0;

    if (LED_CONFIG.levels[0] !== 1) {
        // Add a fake center with a single LED
        centre_xy += level_offset;
        centre_offset = level_offset;
    }

    let leds = [];
    LED_CONFIG.levels.forEach(function(level_count, level_index) {
        const level_radius = (level_index * level_offset) + centre_offset;
        for (let led_index=0; led_index<level_count; led_index++) {
            const angle = 2 * Math.PI * led_index / level_count;
            const offset_x = Math.sin(angle) * level_radius;
            const offset_y = Math.cos(angle) * level_radius;
            leds.push(_make_led(centre_xy + offset_y, centre_xy + offset_x));
        }
    });

    // Hidden "extra" LEDs
    for (let index=0; index<LED_CONFIG.extra_leds; index++) {
        leds.push(_make_led(0, index*LED_WH));
    }

    if (LED_CONFIG.reverse) {
        leds.reverse();
    }

    return {
        leds: leds,
        width: centre_xy*2,
        height: centre_xy*2,
    };
}

function _make_led(top, left) {
    return $(`<span class="led" style="top: ${top}px; left: ${left}px;"></span>`);
}

function get_rgba(pixel, alpha) {
    return `rgba(${pixel[0]},${pixel[1]},${pixel[2]},${0.5 + alpha / 62})`;
}

function update_display(data) {
    if (config_has_changed(LED_CONFIG, data.config)) {
        apply_config(data.config);
    }

    // Update the LEDs
    LEDS.forEach(function(led, index) {
        const rgba = get_rgba(data.pixels[index], data.alpha);
        led.css('backgroundColor', rgba);
    });
}

function open_ws() {
    const ws_url = get_ws_url(),
        ws = new WebSocket(ws_url);
    ws.onmessage = function (evt) {
        update_display(JSON.parse(evt.data));
    };
}

function reload_config() {
    // Load the config from the server and show it
    const config_status = $('#config_status');
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
    const config_status = $('#config_status');
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

function show_config_help() {
    $('#config_help').toggle();
}

function bind_handlers() {
    $('#show_config_help').click(show_config_help);
    $('#reload_config').click(reload_config);
    $('#save_config').click(save_config);
}

function load_constants() {
    $.ajax(
        '/constants'
    ).done(function(data, textStatus, jqXHR) {
        $('#config_help pre').text(JSON.stringify(data, undefined, 2));
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
