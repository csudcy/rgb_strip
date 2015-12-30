function get_ws_url() {
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

function config_has_changed(old_config, new_config) {
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

function apply_config(new_config) {
    console.log('Applying new config!', led_config, new_config);
    led_config = new_config;

    var led_container = $('#led_container');

    // Remove everything previously created
    led_container.children().remove();
    leds = [];

    // Add new LEDs in the correct configuration
    for (var y=0; y<led_config.height; y++) {
        // Add a row container
        var row_container = $('<span></span>')
            .addClass('row_container')
            .appendTo(led_container);

        var led_row = [];
        for (var x=0; x<led_config.width; x++) {
            // Add an LED
            var led = $('<span></span>')
                .addClass('led')
                .appendTo(row_container);

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
    if (config_has_changed(led_config, data.config)) {
        apply_config(data.config);
    }

    // Update the LEDs
    for (var y=0; y<led_config.height; y++) {
        for (var x=0; x<led_config.width; x++) {
            var rgba = get_rgba_xy(x, y, data.bytes);
            leds[y][x].css('backgroundColor', rgba);
        }
    }
}

function open_ws() {
    var ws_url = get_ws_url(),
        ws = new WebSocket(ws_url);
    ws.onmessage = function (evt) {
        update_display(JSON.parse(evt.data));
    };
}

function reload_config() {
    // Load the config from the server and show it
    var config_status = $('#config_status');
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
    var config_status = $('#config_status');
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

var constants;
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
