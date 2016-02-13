var app = angular
    .module("app", ["ui.router", "jqwidgets"])
    .config(function ($stateProvider, $urlRouterProvider) {
        app.stateProvider = $stateProvider;
    })
    .run(function ($http) {

        $http({
            method: 'POST',
            url: '/Config/GetRoutes'
        }).success(function (data, status) {

            for (i in data.routes) {

                app.stateProvider.state(data.routes[i].name, {
                    url: "/" + data.routes[i].name,
                    templateUrl: data.routes[i].url,
                    controller: 'sectionController'
                });
            }
        });

    })
;

app.controller('sectionController', function ($scope, $http) {

    var source =
    {
        datatype: "json",
        datafields: [
            { name: 'Id', type: 'int' },
            { name: 'FirstName', type: 'string' },
            { name: 'LastName', type: 'string' }
        ],
        id: 'id',
        type: 'POST',
        url: '/Person/GetListData'
    };

    var dataAdapter = new $.jqx.dataAdapter(source);

    $scope.gridSettings =
    {
        width: 850,
        source: dataAdapter,
        columnsresize: true,
        columns: [
            { text: 'FirstName', datafield: 'FirstName', width: '10%' },
            { text: 'LastName', datafield: 'LastName', width: '10%' }
        ]
    };
});