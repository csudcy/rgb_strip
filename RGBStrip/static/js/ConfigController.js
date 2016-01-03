angular.module('rgbs')
    .filter('highlight', function() {
        return function (input, query) {
            if (!input) {
                return input;
            }
            var r = RegExp('('+ query + ')', 'gi');
            return input.replace(r, '<span class="highlight">$1</span>');
        }
    })
    .controller('ConfigController', function($scope, $http) {

        function load_constants() {
            $http({
                method: 'GET',
                url: '/constants'
            }).then(
                function successCallback(response) {
                    $scope.colours = response.data.colours;
                    $scope.config_params = response.data.config;
                    console.log($scope.config_params);
                },
                function errorCallback(response) {
                    console.log('Error loading constants:', response);
                }
            );
        }

        $scope.load_config = function() {
            $http({
                method: 'GET',
                url: '/config'
            }).then(
                function successCallback(response) {
                    $scope.config = jsyaml.load(response.data);
                    console.log($scope.config);
                },
                function errorCallback(response) {
                    console.log('Error loading config:', response);
                }
            );
        }

        $scope.save_config = function() {
            console.log('TODO: save_config');
        }

        $scope.config_remove = function(section, index) {
            // Remove the index element from config.section
            $scope.config[section].splice(index, 1);
        }

        $scope.config_add = function(section) {
            // Add an element to config.section
            $scope.config[section].splice(0, 0, {});
        }

        load_constants();
        $scope.load_config();


    });
