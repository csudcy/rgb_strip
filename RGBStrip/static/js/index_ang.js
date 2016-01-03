/*global angular*/
angular.module('rgbs', ['ngWebsocket'])
    .controller('DisplayController', function($scope, $websocket) {
        // Have to store everything on $scope as display.$apply() trigger some ws stuff
        $scope.width = 0;
        $scope.height = 0;
        $scope.leds = [];


        /**************************************\
                    CONFIG MANAGEMENT
        \**************************************/

        function _is_config_changed(width, height) {
            return (
                ($scope.width !== width)
                || ($scope.height !== height)
            );
        }

        function _apply_config(width, height) {
            $scope.width = width;
            $scope.height = height;
            $scope.leds = [];
            for (var y=0; y<height; y++) {
                var led_row = [];
                for (var x=0; x<width; x++) {
                    led_row.push({colour: 'rgba(0,0,0,1)'});
                }
                $scope.leds.push(led_row);
            }
        }


        /**************************************\
                    BYTE TO RGB
        \**************************************/

        function _get_offset(index) {
            return 4 + index * 4;
        }

        function _get_index(reverse_x, reverse_y, x, y) {
            if (reverse_x) {
                x = $scope.width - x - 1;
            }
            if (reverse_y) {
                y = $scope.height - y - 1;
            }
            return (y * $scope.width) + (y % 2 === 0 ? x : $scope.width - x - 1);
        }

        function _get_rgba(index, bytes) {
            var offset = _get_offset(index),
                r = bytes[offset + 3],
                g = bytes[offset + 2],
                b = bytes[offset + 1],
                a = ((bytes[offset + 0] && 31) / 31);

            return 'rgba('+r+','+g+','+b+','+a+')';
        }

        function _get_rgba_xy(reverse_x, reverse_y, x, y, bytes) {
            var index = _get_index(reverse_x, reverse_y, x, y);
            return _get_rgba(index, bytes);
        }

        function _update_leds(reverse_x, reverse_y, bytes) {
            for (var y=0; y<$scope.height; y++) {
                for (var x=0; x<$scope.width; x++) {
                    $scope.leds[y][x].colour = _get_rgba_xy(reverse_x, reverse_y, x, y, bytes);
                }
            }
        }


        /**************************************\
                    WEBSOCKET
        \**************************************/

        function _get_ws_url() {
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

        var ws = $websocket.$new(_get_ws_url());

        ws.$on('$open', function () {
            console.log('WebSocket Open');
            $scope.width = 10;
        });

        ws.$on('$message', function (data) {
            //console.log('Websocket message', data);

            // Check if the LED layout has changed
            if (_is_config_changed(data.config.width, data.config.height)) {
                _apply_config(data.config.width, data.config.height);
            }

            // Update the LEDs to their latest colour
            _update_leds(
                data.config.reverse_x,
                data.config.reverse_y,
                data.bytes
            );

            // Since this happens outside of angulars control, we need to manually tell angular to update the UI
            $scope.$apply();
        });

        ws.$on('$close', function () {
            console.log('WebSocket close');
        });

    });
