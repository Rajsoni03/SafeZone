var options = {
    chart: {
        height: 387,
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
        offsetY: 30
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
        height: 350,
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
    series: [44, 55, 13, 43, 22],
    chart: {
        width: 380,
        type: 'pie',
    },
    labels: ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'],
    responsive: [{
        breakpoint: 480,
        options: {
            chart: {
                width: 200
            },
            legend: {
                position: 'bottom'
            }
        }
    }]
};

var pichart = new ApexCharts(document.querySelector("#pichart"), options);
pichart.render();