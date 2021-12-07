
var options = {
    chart: {
        height: 335,
        type: 'radialBar',
    },
    plotOptions: {
        radialBar: {
            dataLabels: {
                name: {
                    fontSize: '22px',
                },
                value: {
                    fontSize: '16px',
                },
                total: {
                    show: true,
                    label: 'Total',
                    formatter: function(w) {
                        // By default this function returns the average of all series. The below is just an example to show the use of custom formatter function
                        return 249
                    }
                },
            },
            offsetX: -100,
            offsetY: 0
        }
    },
    stroke: {
        lineCap: 'round'
    },
    series: [44, 55, 67, 83],
    labels: ['Corona', 'Depute', 'Bananas', 'Berries'],
    legend: {
        show: true,
        floating: true,
        position: 'right',
        offsetX: 70,
        offsetY: 0
    },
};

var radialBarBottom = new ApexCharts(document.querySelector("#radialBarBottom"), options);
radialBarBottom.render();



var options = {
    series: [{
        data: [
            [1327359600000, 30.95],
            [1327446000000, 31.34],
            [1328569200000, 32.28],
            [1328655600000, 32.10],
            [1334268000000, 33.18],
            [1355353200000, 35.53],
            [1355439600000, 37.56],
            [1355698800000, 37.42],
            [1355785200000, 37.49],
            [1355871600000, 38.09],
            [1355958000000, 37.87],
            [1356044400000, 37.71],
            [1356303600000, 37.53],
            [1356476400000, 37.55],
            [1356562800000, 37.30],
            [1358377200000, 37.73],
            [1358463600000, 37.98],
            [1358809200000, 37.95],
            [1359586800000, 37.83],
            [1359673200000, 38.34],
        ]
    }],
    chart: {
        id: 'area-datetime',
        type: 'area',
        height: 300,
        zoom: {
            autoScaleYaxis: true
        }
    },
    dataLabels: {
        enabled: false
    },
    markers: {
        size: 0,
        style: 'hollow',
    },
    xaxis: {
        type: 'datetime',
        min: new Date('01 Sep 2012').getTime(),
        tickAmount: 6,
    },
    tooltip: {
        x: {
            format: 'dd MMM yyyy'
        }
    },
    fill: {
        type: 'gradient',
        gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.7,
            opacityTo: 0.9,
            stops: [0, 100]
        }
    },
};

var chart = new ApexCharts(document.querySelector("#line-adwords"), options);
chart.render();




var options = {
    chart: {
        height: 315,
        type: 'pie',
    },
    plotOptions: {
        pie: {
            offsetX: -50,
            offsetY: 0
        }
    },
    legend: {
        offsetX: 70,
        offsetY: 0
    },
    series: [44, 55, 13, 43, 22],
    labels: ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'],
    responsive: [{
        breakpoint: 480,
        options: {
            chart: {
                width: 200
            },
        }
    }]
};

var pichart = new ApexCharts(document.querySelector("#pi-chart"), options);
pichart.render();


var options = {
    series: [{
        name: 'PRODUCT A',
        data: [44, 55, 41, 67, 22, 43, 23]
    }, {
        name: 'PRODUCT B',
        data: [13, 23, 20, 8, 13, 27, 79]
    }, {
        name: 'PRODUCT C',
        data: [11, 17, 15, 15, 21, 14, 11]
    }, {
        name: 'PRODUCT D',
        data: [21, 7, 25, 13, 22, 8, 20]
    }],
    chart: {
        type: 'bar',
        height: 300,
        stacked: true,
        toolbar: {
            show: true
        },
        zoom: {
            enabled: true
        }
    },
    responsive: [{
        breakpoint: 480,
        options: {
            legend: {
                position: 'bottom',
                offsetX: -10,
                offsetY: 0
            }
        }
    }],
    plotOptions: {
        bar: {
            horizontal: false,
            borderRadius: 10
        },
    },
    xaxis: {
        type: 'days',
        categories: ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday'
        ],
    },
    legend: {
        position: 'right',
        offsetY: 40
    },
    fill: {
        opacity: 1
    }
};

var dayColumns = new ApexCharts(document.querySelector("#dayColumns"), options);
dayColumns.render();